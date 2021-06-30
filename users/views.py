from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def register(request):
    """Rejestracja nowego uzytkownika"""
    if request.method != 'POST':
        #wyswietlanie pustego formularza rejestracji uzytkownika
        form = UserCreationForm()
    else:
        #przetworzenie wypelnionego formularza
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            #zalogowanie uzytkownika a nastepnie przekierowanie go na strone glowna
            login(request, new_user)
            return redirect('learning_logs:index')

    #Wyswietlanie pustego formularza
    context = { 'form': form}
    return render(request, 'registration/register.html', context)