from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm


def home_view(request):
    return render(request, 'home.html')


def register_view(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            messages.success(
                request,
                f'Congratulations, {form.cleaned_data["full_name"]}! You have successfully registered for the conference!🎉'
            )

            return redirect('home')

    else:
        form = RegistrationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )
