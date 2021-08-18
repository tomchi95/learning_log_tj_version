from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def check_topic_owner(request, topic_id):
    # upewniamy sie czy temat należy do bieżącego użytkownika
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404


# Utwórz swoje widoki
def index(request):
    """Strona główna dla aplikacji Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Wyświetlanie wszystkich tematów."""
    topics = Topic.objects.order_by('date_added')
    # wyświetla tylko tematy dla zalogowanego użytkownika
    # topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Wyświetla pojedynczy temat i wszystkie powiązane z nim wpisy"""
    topic = Topic.objects.get(id=topic_id)

    entries = topic.entry_set.order_by('-data_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != 'POST' :
        # nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = TopicForm()
    else:
        # przekazano dane za pomocą zadania POST, należy je przetworzyć
        form = TopicForm(request.POST, request.FILES)

        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # return redirect('learning_logs:topics')
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    # Wyświetlanie pustego formularza
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Dodaj nowego wpisu dla określonego tematu."""
    topic = Topic.objects.get(id = topic_id)

    check_topic_owner(request, topic.id)

    if request.method != 'POST' :
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = EntryForm()
    else:
        # przekazano dane za pomocą zadania POST, należy je przetworzyć
        form = EntryForm(data = request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # return redirect('learning_logs:topic', topic_id=topic_id)
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))

    # wyświetlanie pustego formularza
    context = { 'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edycja istniejącego wpisu"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST' :
        # zadanie początkowe, wypełnienie formularza aktualna trescia wpisu
        form = EntryForm(instance = entry)
    else:
        # przekazano dane za pomocą zadania POST, należy je przetworzyć
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            # return redirect('learning_logs:topic', topic_id = topic.id)
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic.id]))

    context = {'entry' : entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def edit_topic(request, topic_id):
    """Edycja istniejącego tematu"""
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST' :
        # zadanie początkowe, wypełnienie formularza aktualna trescia wpisu
        form = TopicForm(instance = topic)
    else:
        # przekazano dane za pomocą zadania POST, należy je przetworzyć
        form = TopicForm(data = request.POST, files = request.FILES, instance = topic)

        # usuniecie obrazka z serwera jeżeli nastepuje zmiana lub usuniecie obrazka
        if request.FILES.get('files') != topic.header_image:
            topic.delete()
        else:
            form = TopicForm(data = request.POST, files = request.FILES, instance = topic)
        
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            # return redirect('learning_logs:topic', topic_id = topic.id)
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic.id]))

    context = { 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)


@login_required
def remove_entry(request, entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST' :
        # zadanie początkowe, wypełnienie formularza aktualna trescia wpisu
        form = EntryForm(instance=entry)
    else:
        # przekazano dane za pomocą zadania POST, należy je przetworzyć
        form = EntryForm(instance=entry)
        entry.delete()
        # return redirect('learning_logs:topic', topic_id = topic.id)
        return HttpResponseRedirect(reverse('learning_logs:topic',
                                    args=[topic.id]))

    context = {'entry' : entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/remove_entry.html', context)


@login_required
def remove_topic(request, topic_id):

    topic = Topic.objects.get(id = topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST' :
        # zadanie początkowe, wypełnienie formularza aktualna trescia wpisu
        form = TopicForm(instance=topic)
    else:
        # przekazano dane za pomocą zadania POST, należy je przetworzyć
        form = TopicForm(instance=topic)
        topic.delete()
        # return redirect('learning_logs:topic', topic_id = topic.id)
        return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/remove_topic.html', context)
