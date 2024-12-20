from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from . import models
from . import forms
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator



@login_required
def follow_users(request):
	form = forms.FollowUserForm(instance=request.user)
	if request.method == 'POST':
		form = forms.FollowUserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('home')
	return render(request, 'blog/follow_users_form.html', {'form': form})


@login_required
def home(request):
	blogs = models.Blog.objects.filter(
		Q(contributors__in=request.user.follows.all()) | Q(starred=True))

	photos = models.Photo.objects.filter(uploader__in=request.user.follows.all()).exclude(blog__in=blogs)
	blogs_and_photos = sorted(chain(blogs, photos), key=lambda instance: instance.date_created, reverse=True)

	paginator = Paginator(blogs_and_photos, 3) # Show 6 photos per page

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'page_obj': page_obj
	}


	context = {
		'blogs_and_photos': blogs_and_photos
	}
	return render(request, 'blog/home.html', context=context)


@login_required
@permission_required('blog.add_photo', raise_exception=True)
def photo_upload(request):
	form = forms.PhotoForm()
	if request.method == 'POST':
		form = forms.PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			photo = form.save(commit=False)
			# set the uploader to the user before saving the model
			photo.uploader = request.user
			# now we can save the model
			photo.save()
			return redirect('home')
	return render(request, 'blog/photo_upload.html', {'form': form})


@login_required
def create_multiple_photos(request):
	PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
	formset = PhotoFormSet()
	if request.method == 'POST':
		formset = PhotoFormSet(request.POST, request.FILES)
		if formset.is_valid():
			for form in formset:
				if form.cleaned_data:
					photo = form.save(commit=False)
					photo.uploader = request.user
					photo.save()
				return redirect('home')

	return render(request, 'blog/create_multiple_photos.html',{'formset': formset})


@login_required
def blog_and_photos_upload(request):
	blog_form = forms.BlogForm()
	photo_form = forms.PhotoForm()
	if request.method == 'POST':
		blog_form = forms.BlogForm(request.POST)
		photo_form = forms.PhotoForm(request.POST, request.FILES)
		if all([blog_form.is_valid(), photo_form.is_valid()]):
			photo = photo_form.save(commit=False)
			# set the uploader to the user before saving the model
			photo.uploader = request.user
			# now we can save the model
			photo.save()
			blog = blog_form.save(commit=False)
			blog.author = request.user
			blog.photo = photo
			blog.save()
			blog.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
			
		return redirect('home')

	context = {
	'blog_form': blog_form,
	'photo_form': photo_form
	}

	return render(request, 'blog/create_blog_post.html', context=context)

@login_required
def edit_blog(request, blog_id):
	blog = get_object_or_404(models.Blog, id=blog_id)
	edit_form = forms.BlogForm(instance=blog)
	delete_form = forms.DeleteBlogForm()
	if request.method == 'POST':
		if 'edit_blog' in request.POST:
			edit_form = forms.BlogForm(request.POST, instance=blog)
			if edit_form.is_valid():
				edit_form.save()
				return redirect('home')
			if 'delete_blog' in request.POST:
				delete_form = forms.DeleteBlogForm(request.POST)
				if delete_form.is_valid():
					blog.delete()
					return redirect('home')
	context = {
		'edit_form': edit_form,
		'delete_form': delete_form
	}
	return render(request, 'blog/edit_blog.html', context=context)



@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Photo, id=blog_id)
    return render(request, 'blog/view_blog.html', context={'blog': blog})
