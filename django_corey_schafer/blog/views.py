from blog.forms import ScheduledDateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db import models

from .models import Post

#TODO Only give access to approved accounts. Maybe in Template layer if guest user is an account.
#TODO Fix Datetime
def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

#TODO optional: infinite scroll
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_added']
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        content_length_int = 50
        content_length = ":"+str(content_length_int)
        kwargs['content_length'] = content_length
        kwargs['content_length_int'] = content_length_int
        print(kwargs)
        return super().get_context_data(**kwargs)

    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_added')

    def get_context_data(self, **kwargs):
        content_length_int = 50
        content_length = ":"+str(content_length_int)
        kwargs['content_length'] = content_length
        kwargs['content_length_int'] = content_length_int
        print(kwargs)
        return super().get_context_data(**kwargs)

class PostDetailView(DetailView):
    model = Post

#TODO Make sure  form does not wipe data if permission is not given
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = modelform_factory(Post, fields=['title', 'handles', 'image', 'content', 'hashtags', 'permission'],
        widgets={'handles': forms.Textarea(attrs={'rows':1, 'cols':15}),
        'hashtags':forms.Textarea(attrs={'rows':2, 'cols':15})})
    
    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['initial'] = {'handles':self.request.user.profile.handle,
                            'permission':False}
        return kwargs
    
    def form_valid(self, form):
        if form.instance.permission != True:
            pk = form.instance.pk
            messages.error(self.request, 'No permission given')
            return redirect('post-create')
        else:
            form.instance.author = self.request.user
            messages.success(self.request, 'Post Created')    
            return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


#TODO Make sure  form does not wipe data if permission is not given
class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = modelform_factory(Post, fields=['title', 'handles', 'image', 'content', 'hashtags', 'permission'],
        widgets={'handles': forms.Textarea(attrs={'rows':1, 'cols':15}),
        'hashtags':forms.Textarea(attrs={'rows':2, 'cols':15})})
    
    
    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs['initial'] = {'handles':self.request.user.profile.handle,
                             'permission':False}
        return kwargs

    def form_valid(self, form):
        if form.instance.permission != True:
            pk = form.instance.pk
            messages.error(self.request, 'No permission given')
            return redirect('post-update', pk)
        else:
            form.instance.author = self.request.user
            messages.success(self.request, 'Post Updated')    
            return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user or self.request.user.is_superuser:
            return True
        else:
            return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user or self.request.user.is_superuser:
            return True
        else:
            return False

#TODO Fix sidebar on template
class PostScheduleListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/schedule_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.all().order_by('-scheduled_date')
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False
    
    def get_context_data(self, **kwargs):
        form = ScheduledDateForm()
        kwargs['form'] = form
        return super().get_context_data(**kwargs)
    
    def post(self, request, *args, **kwargs):
        post_id = request.POST['post']
        post = Post.objects.filter(id=post_id).first()
        self.form = ScheduledDateForm(request.POST, instance=post)
        form = self.form
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your post has been scheduled.')
            return redirect('post-schedule')
        else:
            kwargs['form']=form
            messages.warning(request,'Selected date must not be in the past')
            return redirect('post-schedule')
        
