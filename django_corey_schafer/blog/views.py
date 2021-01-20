from blog.forms import ScheduledDateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from .models import Post

# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_added']
    paginate_by = 5

    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_added')


class PostDetailView(DetailView):
    model = Post



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','image', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        #!!!!!!!!!!!!!!! Passed request.FILES into the form
        #!!!!! This is not a default for CreateView. BullShittttt
        #? Now it works without? why? Maybe since request removed from form_valid
        return super().form_valid(form)
    
    #* This is from the UserPassesTestMixin.
    #* Only allows the view to be accessed if the test is passed
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        else:
            return False

class PostScheduleListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/schedule_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

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
            return render(request, 'schedule_posts.html', {'form':form})