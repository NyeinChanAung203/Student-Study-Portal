from django.shortcuts import render,get_object_or_404,redirect
from .models import Notes,Homework,Todo
from .forms import NotesForm,HomeworkForm,DashboardForm,TodoForm,ConversionForm,ConversionLengthForm,ConversionMassForm,UserRegistrationForm
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import requests
import wikipedia

# Create your views here.

def home(request):
    return render(request,'dashboard/home.html',{})

@login_required
def notes(request):
    notes = Notes.objects.filter(user=request.user)
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request,'Note added successfully')
    
    form = NotesForm()
    context = {
        'notes':notes,
        'form':form
    }
    return render(request,'dashboard/notes.html',context)

@login_required
def deleteNote(request,pk=None):
    note = get_object_or_404(Notes,pk=pk)
    note.delete()
    return redirect('notes')


class NoteDetailView(LoginRequiredMixin,generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'

@login_required
def homeWork(request):
    homeworks = Homework.objects.filter(user=request.user)
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        print(request.POST.get('is_finished'))
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = form.save(commit=False)
            homework.user = request.user
            homework.is_finished = finished
            homework.save()
            messages.success(request,'Homework Added successfully')
    form = HomeworkForm()
    context = {
        'homeworks':homeworks,
        'form':form
    }
    return render(request,'dashboard/homework.html',context)

@login_required
def update_homework(request,pk):
    homework = get_object_or_404(Homework,pk=pk)
    print(homework.is_finished)
    if homework.is_finished == True:
        homework.is_finished = False
        homework.save()
    else:
        homework.is_finished = True
        homework.save()
    print(homework.is_finished)
    return redirect('homework')

@login_required
def delete_homework(request,pk):
    homework = get_object_or_404(Homework,pk=pk)
    homework.delete()
    return redirect('homework')
    

@login_required
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text')
        videos = VideosSearch(text,limit=20)
        result_list = []
        for i in videos.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    form = DashboardForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/youtube.html',context)

@login_required
def todo(request):
    todos = Todo.objects.filter(user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo')
    form = TodoForm()
    context = {
        'todos':todos,
        'form':form
    }
    return render(request,'dashboard/todo.html',context)

@login_required
def updateTodo(request,pk):
    todo = get_object_or_404(Todo,pk=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def deleteTodo(request,pk):
    todo = get_object_or_404(Todo,pk=pk)
    todo.delete()
    return redirect('todo')

@login_required
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text')
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    form = DashboardForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/books.html',context)

@login_required
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'definition':definition,
                'audio':audio,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request,'dashboard/dictionary.html',context)
    form = DashboardForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/dictionary.html',context)

@login_required
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    form = DashboardForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/wiki.html',context)

@login_required
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)

        # for length
        if request.POST['measurement'] == 'length':
            print('in length')
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            print(request.POST)
            print(form,measurement_form)
            if 'input' in request.POST:
                print('in input')
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard ={int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot ={int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
                print(measurement_form,answer,form)
        #----------

        #for mass
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound ={int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram ={int(input)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:

        form = ConversionForm()
        context = {
            'form':form,
            'input':False
        }
    return render(request,'dashboard/conversion.html',context)

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!!')
            return redirect('login')
    form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(user=request.user,is_finished=False)
    todos = Todo.objects.filter(user=request.user,is_finished=False)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        "homeworks":homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }
    return render(request,'dashboard/profile.html',context)