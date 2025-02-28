from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save()

        # Отправка поздравительного письма при достижении 100 просмотров
        if obj.view_count == 100:
            send_mail(
                'Поздравляем!',
                f'Статья "{obj.title}" достигла 100 просмотров!',
                'uskat2@yandex.ru',
                ['uskat2@yandex.ru'],
                fail_silently=False,
            )

        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse('post_detail',
                       kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
