from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from articles.models import Article
from library.forms import ReadingListSelectionForm
from library.models import ReadingList

User = get_user_model()

class ReadingListIndexView(LoginRequiredMixin, ListView):
    model = ReadingList
    template_name = 'reading_lists.html'

    def get_queryset(self):
        return ReadingList.objects.filter(owner = self.request.user)


class ReadingListDetailView(LoginRequiredMixin, DetailView):
    model = ReadingList
    template_name = 'reading_list_details.html'

    def get_queryset(self):
        return ReadingList.objects.filter(owner = self.request.user)


class CreateReadingList(LoginRequiredMixin, CreateView):
    model = ReadingList
    template_name = 'create_reading_list.html'
    fields = ['name']
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EditReadingList(LoginRequiredMixin, UpdateView):
    model = ReadingList
    template_name = 'edit_reading_list.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('reading_list_details', kwargs = {'pk': self.object.pk})

class DeleteReadingList(LoginRequiredMixin, DeleteView):
    model = ReadingList
    success_url = reverse_lazy('articles')
    template_name = 'confirm_reading_list_delete.html'

@login_required
def add_to_saved(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ReadingListSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            reading_list_id = form.cleaned_data['reading_lists']
            for list_id in reading_list_id:
                reading_list = ReadingList.objects.get(id = list_id, owner = request.user)
                reading_list.articles.add(article)
            messages.success(request, "Story saved successfully!")
            return redirect('articles')
    else:
        form = ReadingListSelectionForm(user=request.user)
    return render(request, 'add_to_saved.html', {'form': form})


def remove_from_reading_list(request, reading_list_id, article_id):
    reading_list = get_object_or_404(ReadingList, id = reading_list_id, owner = request.user)
    article = get_object_or_404(Article, id = article_id)
    reading_list.articles.remove(article)
    messages.info(request, "article was removed successfully!")
    return redirect('reading_list_details', pk = reading_list_id)
