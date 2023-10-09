from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import DetailView, ListView
from .models import Profile
from .decorators import unauthenticated_user
from blog.models import Post
from django.contrib.auth.models import User, Group


@unauthenticated_user
def register(request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})



class UserProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'users/profile.html'
    context_object_name = 'posts'
    paginate_by = 5
    

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
 

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=user).first()
        return context




@login_required
def follow(request, pk):  
    if request.method == "POST": 
       current_user_profile = request.user.profile
       user_to_follow = Profile.objects.filter(user=pk).first()

       if  current_user_profile.follows.filter(user__username=user_to_follow):
           current_user_profile.follows.remove(user_to_follow)
       else:
           current_user_profile.follows.add(user_to_follow)

       return redirect(user_to_follow)
    else:
        return redirect('blog-home')


@login_required
def EditProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated')
            return redirect('edit-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'p_form': p_form,
        'u_form': u_form
    }
    return render(request, 'users/edit_profile.html', context)


class FollowsListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/follows.html'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super(FollowsListView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=user).first()
        return context


class FollowersListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/followers.html'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super(FollowersListView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=user).first()
        return context

@login_required
def popular_authors(request):
    profile_objects = Profile.objects.all()
    profiles = sorted(profile_objects, key=lambda profile: -profile.number_of_followers())
    return render(request, 'users/popular_authors.html', {'profiles': profiles})