from django.conf import settings
from django.http import request
from celery_example.tasks import send_email_task
from .image_resize import image_resize
from PIL import Image
from .forms import ScheduledDateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.files.base import ContentFile
from io import BytesIO
from .models import Post
from django.utils import timezone


def home(request):
    return render(request, 'dashboard/home.html')


def about(request):
    return render(request, 'dashboard/about.html', {'title': 'About'})

# TODO optional: infinite scroll
# TODO add link to user profile in user view

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard/home.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_post_list(self):
        posts = Post.objects.all()
        return posts

    def get_queryset(self):
        user = self.request.user
        posts = self.get_post_list()
        
        if user.is_superuser:

            if self.request.GET.get('status'):
                posts = posts.filter(status=self.request.GET['status'])

            sort_by = self.request.GET.get('sort')
            if sort_by == 'date':
                posts = sorted(posts, key=lambda p: p.date_added, reverse=True)

            if sort_by == 'author':
                posts = sorted(
                    posts, key=lambda p: p.author.username, reverse=False)
        
        else:
            posts = posts.filter(status='staged')

        return posts

    def get_context_data(self, **kwargs):
        content_length_int = 50
        content_length = ":"+str(content_length_int)
        kwargs['content_length'] = content_length
        kwargs['content_length_int'] = content_length_int
        kwargs['status'] = [('', 'All')] + list(Post.POST_STATUSES)
        return super().get_context_data(**kwargs)


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard/home.html'
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
        return super().get_context_data(**kwargs)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post

    form_class = modelform_factory(Post, fields=['title', 'handles', 'image', 'content', 'hashtags', 'permission'],
                                   widgets={'handles': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
                                            'hashtags': forms.Textarea(attrs={'rows': 2, 'cols': 15})})

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        if User.is_anonymous:
            return kwargs
        else:
            kwargs['initial'] = {'handles': self.request.user.profile.handle,
                                 'permission': False}
        return kwargs

    def form_valid(self, form):
        if form.instance.permission != True:
            messages.error(self.request, 'No permission given')
            return self.form_invalid(form)
        else:
            form.instance.author = self.request.user
            messages.success(self.request, 'Post Created')
            return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = modelform_factory(Post, fields=['title', 'handles', 'image', 'content', 'hashtags', 'permission'],
                                   widgets={'handles': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
                                            'hashtags': forms.Textarea(attrs={'rows': 2, 'cols': 15})})

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs['initial'] = {'handles': self.request.user.profile.handle,
                             'permission': False}
        return kwargs

    def form_valid(self, form):
        if form.instance.permission != True:
            pk = form.instance.pk
            messages.error(self.request, 'No permission given')
            return self.form_invalid(form)
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


# TODO Fix sidebar on template
# TODO Make timezone aware of user location
# TODO Make image resize accept all file formats for IG
# TODO Schedule Posts View template update
# TODO Complete Posts View template update
# TODO fix nav bar when logged out. Login register buttons


class PostStageListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard/schedule_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(status='unscheduled').order_by('-date_added')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        post_id = request.POST['post']
        post = Post.objects.filter(id=post_id).first()
        post.scheduled_date = timezone.now()
        post.status = 'staged'
        post.save()
        messages.success(
            request, f'Your post has been selected for scheduling.')
        return redirect('post-stage')


class PostScheduledListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard/schedule_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(status='scheduled').order_by('-scheduled_date')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        kwargs['today'] = timezone.localtime(timezone.now())
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.filter(status='scheduled')
        for post in posts:
            # Update status
            post.status = 'complete'
            post.save()
            # Send Email
            media_root = settings.MEDIA_ROOT[:settings.MEDIA_ROOT.rfind('\\')]
            image_location = f'{media_root}{post.image.url}'
            send_date = timezone.localtime(post.scheduled_date)
            send_email_task.apply_async(
                (post.title, post.handles, post.content, post.hashtags, image_location), eta=send_date)
        messages.success(request, f'Your posts have been scheduled.')
        return redirect('post-scheduled')


class PostScheduleListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'dashboard/schedule_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(status='staged').order_by('-scheduled_date')

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
        post = self.form.instance

        # TODO move send email to schedule view
        if form.is_valid():
            post.status = 'scheduled'
            form.save()
            messages.success(
                request, f'Your post has been scheduled.')
            return redirect('post-schedule')
        else:
            kwargs['form'] = form
            messages.warning(request, 'Selected date must not be in the past')
            return redirect('post-schedule')
