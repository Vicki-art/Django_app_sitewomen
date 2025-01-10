"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.decorators.cache import cache_page
from . import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from women.sitemaps import PostSitemap, CategorySitemap


sitemaps = {
    'posts': PostSitemap,
    'cat': CategorySitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('women/', include('women.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('social_auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml/', cache_page(86400)(sitemap), {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Admin panel'
admin.site.index_title = 'Site admin panel'
