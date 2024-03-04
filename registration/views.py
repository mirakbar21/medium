from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
