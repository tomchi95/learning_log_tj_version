from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, EditForm


# Create your views here.

def register(request):
    # Rejestracja nowego uzytkownika
    if request.method != 'POST':
        # wyswietlanie pustego formularza rejestracji uzytkownika
        form = SignUpForm()
    else:
        # przetworzenie wypełnionego formularza
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # zalogowanie użytkownika a następnie przekierowanie go na strone główną
            login(request, new_user)
            return redirect('learning_logs:index')

    # Wyswietlanie pustego formularza
    context = { 'form': form}
    return render(request, 'registration/register.html', context)


def edit_profile(request):
    # Edycja uzytkownika
    if request.method != 'POST':
        # wyswietlanie pustego formularza rejestracji uzytkownika
        form = EditForm(instance = request.user)
    else:
        # przetworzenie wypełnionego formularza
        form = EditForm(instance = request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # przekierowanie na strone główną
            return redirect('learning_logs:index')

    # Wyswietlanie pustego formularza
    context = {'form': form}
    return render(request, 'registration/edit_profile.html', context)


"""


from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import EditForm, SignUpForm

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registrations/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditForm
    template_name = 'registrations/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

"""