# from django.contrib.auth.models import User
import users
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from learning_logs.forms import ProfileForm
from learning_logs.models import Profile
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, EditForm
# from django.views.generic import DetailView


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
            # zalogowanie użytkownika a następnie
            # przekierowanie go na strone główną
            login(request, new_user)
            return redirect('learning_logs:index')

    # Wyswietlanie pustego formularza
    context = { 'form': form}
    return render(request, 'registration/register.html', context)


def edit_settings(request):
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
    return render(request, 'registration/edit_settings.html', context)


def edit_profile(request, pk):
    profile = Profile.objects.get(id= request.user.profile.id)

    if request.method != 'POST':
        # wyswietlanie pustego formularza rejestracji uzytkownika
        form = ProfileForm(instance = request.user.profile)
    else:
        # przetworzenie wypełnionego formularza
        form = ProfileForm(instance = request.user.profile, data=request.POST, files = request.FILES)
        if request.FILES.get('files') != request.user.profile.profile_pic:
            profile.delete()
        else:
            form = ProfileForm(instance = request.user.profile, data = request.POST, files = request.FILES)

        if form.is_valid():
            form.save()
            # przekierowanie na strone główną
            return HttpResponseRedirect(reverse('users:profile',
                                        args=[pk]))

    context = {'form': form, "profile": Profile, 'users': request.user}
    return render(request, 'registration/edit_profile.html', context)


def new_profile(request):
    if request.method != 'POST':
        form = ProfileForm()
    else:
        form = ProfileForm(data = request.POST, files = request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/new_profile.html', context)


def profile(request, pk):
    context = {'users': request.user, "profile": Profile}
    return render(request, 'registration/profile.html', context)


"""

#class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "registration/profile.html"

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['owner_id'])
        context["page_user"] = page_user
        return context
"""

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