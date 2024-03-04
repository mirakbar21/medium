from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from registration.views import register
from users.views import ProfileView, ProfileUpdateView, ProfileDeleteView, AboutUserView, subscribe, unsubscribe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name = 'registration/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('register/', register, name="register"),
    path('articles/', include('articles.urls')),
    path('reading_lists/', include('library.urls')),
    path('profile/', ProfileView.as_view(), name = 'user_profile'),
    path('profile/edit', ProfileUpdateView.as_view(), name = 'edit_profile'),
    path('profile/delete', ProfileDeleteView.as_view(), name = 'confirm_user_delete'),
    path('profile/about', AboutUserView.as_view(), name = 'about_user'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='user_profile'),
    path('subscribe/<int:user_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)