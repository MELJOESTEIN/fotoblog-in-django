from django import forms
from django.contrib.auth.decorators import login_required

from . import models



class PhotoForm(forms.ModelForm):
	class Meta:
		model = models.Photo
		fields = ('image', 'caption')

class BlogForm(forms.ModelForm):
	edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
	class Meta:
		model = models.Blog
		fields = ('title', 'content')

class DeleteBlogForm(forms.Form):
	delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)


def blog_and_photo_upload(request):
	blog_form = BlogForm()
	photo_form = PhotoForm()
	if request.method == 'POST':
		blog_form = BlogForm(request.POST)
		photo_form = PhotoForm(request.POST, request.FILES)
		if all([blog_form.is_valid(), photo_form.is_valid()]):
			blog_form.save()
			photo_form.save()
	context = {
	'blog_form': blog_form,	
	'photo_form': photo_form,
	}
	
	return render(request, 'blog/create_blog_post.html', context=context)

