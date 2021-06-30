from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def check_topic_owner(request, topic_id):
        #upewniamy sie czy temat nalezy do biezacego uzytkownika
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404



# Create your views here.
def index(request):
    """Strona główna dla aplikacji Learning Log."""
    return render(request, 'learning_logs/index.html')



def topics(request):
    """Wyświetlanie wszystkich tematów."""
    topics = Topic.objects.order_by('date_added')
    #wyswietla tylko tematy dla zalogowanego uzytkownika
    #topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)



def topic(request, topic_id):
    """Wyswietla pojedynczy temat i wszystkie powiazane z nim wpisy"""
    topic = Topic.objects.get(id=topic_id)

    entries = topic.entry_set.order_by('data_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)



@login_required
def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != 'POST' :
        #nie przekazano zadnych danych, nalezy utworzyc pusty formularz
        form = TopicForm()
    else:
        #przekazano dane za pomoca zadania POST, nalezy je przetworzyc
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    #Wyswietlanie pustego formularza
    context = {'form': form} 
    return render(request, 'learning_logs/new_topic.html', context)



@login_required
def new_entry(request, topic_id):
    """Dodaj nowego wpisu dla określonego tematu."""
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(request, topic.id)

    if request.method != 'POST' :
        #Nie przekazano zadnych danych, nalezy utworzyc pusty formularz
        form= EntryForm()
    else:
        #przekazano dane za pomoca zadania POST, nalezy je przetworzyc
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    #wyswietlanie pustego formularza
    context = { 'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)



@login_required
def edit_entry(request, entry_id):
    """Edycja istniejacego wpisu"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    check_topic_owner(request,topic.id)

    if request.method != 'POST' :
        #zadanie poczatkowe, wypelnienie formularza aktualna trescia wpisu
        form= EntryForm(instance=entry)
    else:
        #przekazano dane za pomoca zadania POST, nalezy je przetworzyc
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)

    context = {'entry' : entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)