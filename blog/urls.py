from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('photo/upload/', views.photo_upload, name='photo_upload'),
	path('blog/create/', views.blog_and_photos_upload, name='blog_create'),
	path('blog/<int:blog_id>', views.view_blog, name='view_blog'),
	path('blog/<int:blog_id>/edit', views.edit_blog, name='edit_blog'),
	path('photo/upload-multiple/', views.create_multiple_photos,name='create_multiple_photos'),

	]