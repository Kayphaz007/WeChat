from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.http import HttpResponse, HttpResponseRedirect


#basic views...
def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()[0:5]
    comments = Message.objects.all()
    if request.method == 'GET':
        q = request.GET.get('q')
        if q != '' and q != None:
            rooms = Room.objects.filter(
                Q(topic__name__icontains=q) |
                Q(name__icontains=q)|
                Q(description__icontains=q) 
            )
            comments = Message.objects.filter(
                Q(room__topic__name__icontains =q)|
                Q(user__username__icontains=q)
            )
        else:
            rooms = Room.objects.all()
            
    room_count = rooms.count()
            
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'comments': comments}
    return render(request, 'IndexApp/home.html', context)

def rooms(request, pk):
    
    room = Room.objects.get(id =pk)
    comments = room.comments.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == 'POST':
        comment = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        comment.save()
        room.participants.add(request.user)
        return redirect('room', pk)
    
    
    
    context ={'room': room, 'comments': comments, 'participants': participants}
    return render(request, 'IndexApp/rooms.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    comments = user.message_set.all()
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    
    
    context = {'comments': comments, 'rooms': rooms, 'topics': topics, 'user': user}
    return render(request, 'IndexApp/userProfile.html', context)


@login_required(login_url='loginPage')
def room_form(request):
    form = RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.User
        #     room.save()
        return redirect('home')
        
    
    form = RoomForm()
    context = {'form': form, 'topics': topics}
    return render(request, 'IndexApp/room_form.html', context)



#Update or edit comments
@login_required(login_url='loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    if (request.user != room.host):
        return HttpResponse('you are not allowed to update this room')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     temp = form.save(commit=False)
        #     temp.topic = topic
        return redirect('home')            
    
    context = {'form': form, "topics":topics, 'room':room}
    
    return render(request, 'IndexApp/room_form.html', context)

@login_required(login_url='loginPage')
def deleteRoom(request, pk):
    page = 'room'
    room = Room.objects.get(id=pk)
    
    if (request.user != room.host):
        return HttpResponse('you are not allowed to delete this room')
    
    if request.method == 'POST':
        room.delete()
        return redirect('room', pk)
    
    
    context = {'room': room, 'page': page}
    return render(request, 'IndexApp/deleteRoom.html', context)


#Login views
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid username or password')
        
    context = {'page': page}
    return render(request, 'IndexApp/login_registration.html', context)


def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'There was an error registering the User. Please try again later')
            return redirect('regUser')
            
        
    
    
    context = {'page': page, 'form': form}
    return render(request, 'IndexApp/login_registration.html', context)

def logoutPage(request):
    logout(request)
    return redirect('loginPage')
    
#delete comments    
@login_required(login_url='loginPage')
def deleteComment(request, pk):
    page = 'comments'
    comment = Message.objects.get(id=pk)
    
    if (request.user != comment.user):
        return HttpResponse('you are not allowed to delete this room')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('room', pk=comment.room.id)
    
    
    context = {'page': page, 'comment' : comment}
    return render(request, 'IndexApp/deleteRoom.html', context)


@login_required(login_url='loginPage')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile', pk = request.user.id)
    
    
    
    context = {'form': form}
    return render(request, 'IndexApp/update_user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    topics = Topic.objects.filter(name__icontains=q)
    
    context = {'topics': topics, 'rooms': rooms}
    return render(request, 'IndexApp/topics.html', context)


def activityPage(request):
    rooms= Room.objects.all()
    comments = Message.objects.all()
    
    context = {'rooms': rooms, 'comments': comments}
    return render(request, 'IndexApp/activity.html', context)
