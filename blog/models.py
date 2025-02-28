
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blog_previews/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title  # Метод str, возвращающий заголовок записи

    class Meta:
        verbose_name = 'Блог-запись'
        verbose_name_plural = 'Блог-записи'
