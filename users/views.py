from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from articles.models import Article
from django.views.generic import DetailView, UpdateView, DeleteView

User = get_user_model()

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_articles'] = Article.objects.filter(author = self.request.user)
        context['following'] = self.request.user.following.all()
        return context

    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'edit_profile.html'
    fields = ['username', 'email', 'photo']

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user_profile')

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'confirm_user_delete.html'
    success_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user

class AboutUserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'about_user.html'

    def get_object(self):
        return self.request.user

def subscribe(request, user_id):
    if request.method == 'POST':
        followed = get_object_or_404(User, pk=user_id)
        request.user.following.add(followed)
        return redirect(request.META.get('HTTP_REFERER'))

def unsubscribe(request, user_id):
    if request.method == 'POST':
        followed = get_object_or_404(User, pk=user_id)
        request.user.following.remove(followed)
        return redirect(request.META.get('HTTP_REFERER'))
