
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import UserRegisterView, CustomLoginView, UserProfileUpdateView  # проверьте правильность путей

urlpatterns = [
    path('', include('catalog.urls')),
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='edit_profile'),
    path('users/', include('users.urls')),  # Подключите users.urls для пользовательских маршрутов
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
