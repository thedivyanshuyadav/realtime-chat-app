import json

from django.shortcuts import redirect,render, HttpResponse
from chat_system.models import *
from django.contrib import messages
from datetime import datetime
from django.conf  import settings
from .forms import *
# Create your views here.

HOST =settings.HOST

chatpage = "chat.html"
homepage = "homepage.html"
loginpage = "login.html"
signuppage = "signup.html"
logoutpage = "logout.html"
my_userid = None

def user_authenticate(email,password):
    try:
        user = User.objects.filter(email=email).first()
        print('Check',user.password,password)
        return user if user.password==password else None
    except:
        return None

def signup_page(request):
    if request.user.is_authenticated:
        print(request.user)
        return redirect('/')
    elif request.method=="POST":
        post_data = request.POST
        email = post_data['email']
        username = post_data['username']
        password = post_data['password']
        user, cret = User.objects.get_or_create(
            email=email,
            password=password,
            username =username,
        )
        print(user,cret)
        if not cret:
            messages.add_message(request,messages.ERROR,"Please enter valid information!!")
        else:
            return redirect('/login/')
    return render(request,signuppage,{"HOST":HOST})

def login_page(request):
    if request.method == "POST":
        post_data = request.POST
        print(post_data,'------------------')
        email = post_data['email']
        password = post_data['password']
        user = user_authenticate(email=email,password=password)
        print(user,email,password)
        if user:
            request.session['id']=user.id
            return redirect('/')
        else:
            messages.add_message(request,messages.ERROR,"Please enter valid information!!")
    return render(request,loginpage,{"HOST":HOST})
def logout_page(request):
    del request.session['id']
    return render(request,logoutpage,{"HOST":HOST})


def home_page(request):
    if 'id' not in request.session: return redirect('/login/')
    context = dict()
    context['HOST']=HOST
    userid = context["userid"] = request.session['id']
    user = getuser(userid)
    context['username'] = user.username
    context['email'] = user.email
    context['userid'] = user.id
    context['profile_pic']=user.profile_pic

    added_user = list()
    all_receiver = list()
    for msg in (Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)).order_by('datetime').reverse():
        if msg.receiver==user and msg.sender.username not in added_user:
            all_receiver.append(msg)
            added_user.append(msg.sender.username)
        elif msg.sender==user and msg.receiver.username not in added_user:
            all_receiver.append(msg)
            added_user.append(msg.receiver.username)

    contacts = Contact.objects.filter(user=user).order_by('contact')
    context['contacts'] = contacts
    context['receivers'] = all_receiver

    context['favourites'] = contacts.filter(favourite=True)
    context['story']=[]
    for cont in contacts:
        story = Story.objects.filter(user=cont.contact).first()
        if story:
            print(story)
            context['story'].append(story)

    story = Story.objects.filter(user=user).values('story').first()
    if story:
        context['story_name'] = story['story']


    return render(request,homepage,context)

def send_message(request):
    userid = request.POST['userid']
    other_userid = request.POST['other_userid']
    message = request.POST['message']
    save_message(userid,other_userid,message)
    return HttpResponse()

def save_message(userid:int,other_userid:int,message:str):

    user = User.objects.filter(id=userid).first()
    other_user=User.objects.filter(id=other_userid).first()
    msg = Message.objects.create(sender=user, receiver=other_user, content=message,datetime=datetime.now())
    msg.save()
    return user.id


def chat_page(request):
    global my_userid
    context = dict()
    context["HOST"] = HOST
    my_userid=context["userid"] = request.session['id']
    if request.method == "POST":
        request.session['other_userid'] = request.POST["other_userid"]

    context["other_userid"] = request.session['other_userid']
    userid = context['userid']
    user = getuser(userid)
    other_userid = context["other_userid"]
    other_user = getuser(other_userid)
    context['username'] = other_user.username
    conversation = Message.objects.filter(sender=user,receiver=other_user) | Message.objects.filter(sender=other_user,receiver=user)
    conversation = conversation.order_by('datetime')
    context['conversation'] = conversation.values('content','sender')


    return render(request,chatpage,context)

def getuser(id):
    return User.objects.filter(id=id).first()



def change_profile_pic(request):
    if request.method == "POST":
        print(request.POST)
        userid = request.session['id']
        if 'pp-inp' not in request.FILES:return HttpResponse()
        file = request.FILES['pp-inp']
        user = User.objects.filter(id=userid).first()
        user.profile_pic = file
        user.save()
    return HttpResponse({user.profile_pic.name:True},content_type='application/json')


def create_story(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        userid = request.session['id']
        if 'story-inp' not in request.FILES: return HttpResponse()

        story = request.FILES['story-inp']
        user = User.objects.filter(id=userid).first()
        story_user = Story.objects.filter(user_id=user.id).first()
        if story_user:
            story_user.story = story
            story_user.datetime = datetime.now()
            story_user.save()
        else:
            story_user = Story.objects.create(user=user,story = story, datetime = datetime.now())
            story_user.save()

    return HttpResponse({story_user.story.name:True},content_type='application/json')