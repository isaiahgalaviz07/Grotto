from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# 
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)


# 
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("Room", pk=room.id)

    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, 'base/room.html', context)

#
def userProfile(request, pk):
    user = User.objects.get(id=pk)

    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {"user": user, "rooms": rooms, 
               "room_messages": room_messages, "topics": topics}
    return render(request, 'base/profile.html', context)

#
@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user, 
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description")
        )

        return redirect("Home")

    context = {"form": form, "topics": topics}
    return render(request, 'base/room_form.html', context)


#
@login_required(login_url='Login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You cannot edit this room!')

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("Home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


#
@login_required(login_url='Login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You cannot delete this room!')

    if request.method == "POST":
        room.delete()
        return redirect("Home")
    
    return render(request, "base/delete.html", {"obj":room})


#
@login_required(login_url='Login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You cannot delete this message!')

    if request.method == "POST":
        message.delete()
        return redirect("Home")
    
    return render(request, "base/delete.html", {"obj":message})


#
def loginPage(request):
    page = 'Login'

    if request.user.is_authenticated:
        return redirect("Home")

    if request.method == "POST":
        email = request.POST.get("Email").lower()
        password = request.POST.get("Password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("Home")
        else:
            messages.error(request, "User OR password does not exist.")

    context = {'page': page}
    return render(request, "base/login_register.html", context)


#
def logoutUser(request):
    logout(request)
    return redirect("Home")

#
def registerPage(request):
    page = "Register"
    form = MyUserCreationForm()
    context = {"page": page, "form": form}

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("Home")
        else:
            messages.error(request, "Password is either too short,\n or the name or email is already taken!")

    return render(request, "base/login_register.html", context)

#
@login_required(login_url='Login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("User Profile", pk=user.id)

    return render(request, "base/update_user.html", {"form": form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {"topics": topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {"room_messages": room_messages})