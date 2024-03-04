from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Article, Applaud


class IndexView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['following_articles'] = Article.objects.filter(author__followers=user).distinct()
        context['other_articles'] = Article.objects.exclude(author__in=user.following.all())

        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_details.html"


class CreateArticle(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "create_article.html"
    fields = ['title', 'subtitle', 'content', 'category', 'image']

    def form_valid(self, form):
        form.instance.author = User.objects.get(
            id = self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_details', kwargs = {'pk': self.object.pk})


class EditArticle(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "edit_article.html"
    fields = ['title', 'subtitle', 'content', 'category', 'image']
    success_url = reverse_lazy('articles')


class DeleteArticle(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles')
    template_name = 'confirm_delete.html'


def article_applaud(request, article_id):
    article = get_object_or_404(Article, id = article_id)
    applaud_obj, created = Applaud.objects.get_or_create(user = request.user, article = article)
    applaud_obj.count += 1
    applaud_obj.save()
    article.applauds = Applaud.objects.filter(article = article).count()
    article.save()

    return redirect('article_details', pk = article_id)

def query(request):
    query = request.GET.get('query', '')
    articles = Article.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {
        'articles': articles,
        'query': query
    })
