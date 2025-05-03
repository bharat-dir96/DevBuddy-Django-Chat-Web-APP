from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
# Create your views here.

# rooms =[
#     {'id': 1, 'name':'Lets Learn Python'},
#     {'id': 2, 'name':'Design with me'},
#     {'id': 3, 'name':'Frontend Developers'},
# ]

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)                         #Checks if the user exists
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, email=email, password=password)     #authenticate user by authenticating the username & password. If the value matches, then returns the user object with all its values.

        if user != None:
            login(request, user)                                               #This will create a user session on the browser.
            messages.success(request, f'Success!! Welcome {user.username}')
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist.")

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, "You are logged out.")
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, f'Registration Successful!! Welcome {user.username}')
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration.")

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |           #__icontains matches any value that contains the empty string, and every string contains the empty string. 
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
        )      

    room_count = rooms.count()

    topics = Topic.objects.all()[0:5]

    room_messages = Message.objects.filter(room__topic__name__icontains=q)

    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all()         #Retrive all the child objects(of class message) of specified room. 
    
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        messages.success(request, 'Message Posted')
        return redirect('room', pk=room.id)


    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)                  #Retrieving the user respects to the id passed.

    topics = Topic.objects.all()                    #Retrieving all topics
    rooms = user.room_set.all()                     #Retrieving all rooms hosted by a partiular user.
    room_messages = user.message_set.all()          #Retrieving all the messages posted by a particular user.

    context = {'user':user, 'topics':topics, 'rooms':rooms, 'room_messages':room_messages}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)       #This will get the value of topic and store it in topic variable,
                                                                            # if it finds the value in Topic Model then created is false
                                                                            # and if it didn't find the value then the value is created and stored in Topic Model

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        messages.success(request, 'Success!! Room is created successfully.')
        return redirect('home')

    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)                          # For form to be Prefilled, we need to pass the room instance.
    topics = Topic.objects.all()

    if request.user != room.host:                           # Checks if the logged In User is the host of that room or not.
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)       #This will get the value of topic and store it in topic variable,
                                                                            # if it finds the value in Topic Model then created is false
                                                                            # and if it didn't find the value then the value is created and stored in Topic Model

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        messages.success(request, 'Success!! Room info is updated.')
        return redirect('home')    

    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:                           # Checks if the logged In User is the host of that room or not.
        return HttpResponse("You are not allowed here!!")
    
    if request.method == 'POST':
        room.delete()
        messages.info(request, 'Your Room is deleted.')
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:                           # Checks if the logged In User is the owner of that message or not.
        return HttpResponse("You are not allowed here!!")
    
    if request.method == 'POST':
        message.delete()
        messages.info(request, 'Your Message is deleted.')
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username}'s info is updated.")
            return redirect('user-profile', pk=user.id)


    context = {'form':form}
    return render(request, 'base/update_user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})