"""DjangoWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Sezione-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static

from users import views as user_views
from django.contrib.auth import views as auth_views

from SezioneSpaccio.models import Sezione

# All of the requests that include /playground/ are
# handled by the playground apps.
# When passing the request, everything before the / is chopped (including playground)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', extra_context={'sezioni': Sezione.objects.all()}), name='log-in'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', extra_context={'sezioni': Sezione.objects.all()}), name='log-out'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/libri', user_views.ProfileLibroListView.as_view(), name='profile-libri'),
    path('__debug__/', include(debug_toolbar.urls)),

    # Password reset routes: reset --> email template (automatic) --> done --> confirm --> complete
    # To send emails you need a reset server (gmail works). Change the values in the settings
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', extra_context={'sezioni': Sezione.objects.all()}), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html',extra_context={'sezioni': Sezione.objects.all()}), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',extra_context={'sezioni': Sezione.objects.all()}), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html', extra_context={'sezioni': Sezione.objects.all()}), name='password_reset_complete'),
    path('spaccio/', include('SezioneSpaccio.urls')),
    path('', include('SezioneSpaccio.urls')),
]


# Add the static file serve solution for development ONLY
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)
