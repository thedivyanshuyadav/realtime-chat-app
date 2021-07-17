import json
import os.path

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .fire_handler import Fire
from django.http import JsonResponse
from django.conf import settings
import io
from PIL import Image

def login(request):
    if(request.user.is_authenticated):return redirect(home)
    return render(request, "login.html")

@csrf_exempt
@login_required(login_url='/')
def home(request):
    kwargs = {
        "name": request.user.get_full_name(),
        "username": request.user.get_username(),
        "email": request.user.email,
        "date_joined": request.user.date_joined.timestamp(),
        "id": request.user.pk,
    }
    f = Fire(**kwargs)
    request.session['active_user'] = kwargs
    f.create_user()
    return render(request, "home.html", kwargs)


@csrf_exempt
@login_required(login_url='/')
def get_inbox(request):
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    res = f.get_inbox()
    for i in range(len(res)):
        last_node = f.db.child(f"inbox/{f.uid}/{res[i][0]}/").order_by_key().limit_to_last(2).get().val()
        last_message_detail = [val for key, val in last_node.items()][0]
        res[i].append(last_message_detail)
        res[i].append(f.uid)
    return JsonResponse(res, safe=False)


@login_required(login_url='/')
@csrf_exempt
def chat(request, id,friend):
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    context = dict()
    context['id']=id
    context['myUid'] = f.uid
    context['c_name']=f.uid_to_name(f.id_to_uid(id))
    context['c_pp']=f.profile_pic(f.id_to_uid(id))
    all_chats = f.get_chats(id)
    window = 100
    request.session['allmsgrecieved'] = 0
    if (window > len(all_chats)):
        request.session['allmsgrecieved'] = 1
        window = len(all_chats) - 1
    request.session['remained-msg'] = all_chats[:-window]
    context['allchats'] = all_chats[-window:]
    context['friend']=friend
    return render(request, "chat.html", context)


@login_required(login_url='/')
@csrf_exempt
def get_remained_msg(request):
    window = 40
    remained = request.session['remained-msg']
    if (window > len(remained)): window = len(remained) - 1
    extra = remained[-window:]
    request.session['remained-msg'] = remained[:-window]
    context = dict()
    context['extra'] = extra

    if (len(remained[:-window]) == 0): request.session['allmsgrecieved'] = 1
    context['allmsgrecieved'] = request.session['allmsgrecieved']

    return JsonResponse(context, safe=False)


@login_required(login_url='/')
@csrf_exempt
def sendMessage(request, id,friend):
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    message = request.POST.get('message')
    f.send_message_id(id, message)
    return HttpResponse()

@login_required(login_url='/')
@csrf_exempt
def get_contacts(request):
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    friends=f.get_contacts()
    contact=dict()
    friends=dict(friends)
    for c_uid in friends:
        if(friends[c_uid]):
            contact[c_uid]=dict()
            contact[c_uid]['id']=f.uid_to_id(c_uid)
            contact[c_uid]['name']=f.uid_to_name(c_uid)
            contact[c_uid]['profile_pic']=f.profile_pic(c_uid)
            contact[c_uid]['friend']=friends[c_uid]
    return JsonResponse(contact,safe=False)

@login_required(login_url='/')
@csrf_exempt
def get_settings(request):
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    profile_pic=f.profile_pic(f.uid)
    name=f.uid_to_name(f.uid)
    context=dict()
    context['profile_pic']=profile_pic
    context['name']=name
    return JsonResponse(context,safe=False)

@login_required(login_url='/')
@csrf_exempt
def save_contact_from_id(request,id):
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    c_uid=f.id_to_uid(id)
    f.add_contact(c_uid)
    return HttpResponse()

@login_required(login_url='/')
@csrf_exempt
def save_contact_from_email(request):
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    email=request.POST.get("email")
    c_uid=f.email_to_uid(email)
    added=f.add_contact(c_uid)
    return JsonResponse({"added":added},safe=False)

@csrf_exempt
def change_dp(request):
    print(1)
    kwargs = request.session['active_user']
    f = Fire(**kwargs)
    print(2)
    im_b64=request.FILES.get('image')
    img = Image.open(io.BytesIO(im_b64.read()))
    print(3,img)
    filepath=f.uid+".png"
    img.save(filepath)
    print(4)
    img_url=f.storage.child("profile-pics/"+f.uid+".png").put(filepath)
    img_url = f.storage.child("profile-pics/"+f.uid+".png").get_url(img_url['downloadTokens'])
    print(5)
    f.changeProfilePic(img_url)
    os.remove(filepath)
    print(6)
    return JsonResponse({"image_url":img_url},safe=False)