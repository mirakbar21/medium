from django.shortcuts import render
from .models import Article, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def add_comment(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('add_comment', article_id = article.id)
    else:
        form = CommentForm()
        return render(request, 'add_comment.html', {'form': form, 'article': article})
