from django.shortcuts import render, redirect
from .forms import ContactForm

# Create your views here.


def new_contact(request):
    print(request.method)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contact/')
        else:
            print(form.errors)
            return redirect('/contact/')
    else:
        return redirect('/contact/')


def contact(request):
    return render(
        request,
        "contact/contact_me.html",
    )
