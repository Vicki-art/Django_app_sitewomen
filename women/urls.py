from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')


urlpatterns = [
    path('', views.MainPage.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPost.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('categories/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.ShowTagPostlist.as_view(), name='tag'),
    path('edit/<slug:post_slug>', views.UpdatePost.as_view(), name='edit_page'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete_page')
]


