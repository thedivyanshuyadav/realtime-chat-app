from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from chat_system.models import *
from datetime import datetime
from pytz import timezone
from channels.layers import get_channel_layer

tz = timezone('Asia/Kolkata')


class HomeConsumer(AsyncJsonWebsocketConsumer):
    home_session_name = None

    async def connect(self):
        await self.accept()
        print("[Home] Connected!!")

    async def receive_json(self, content, **kwargs):
        print('[home] content :::  ', content)
        if content['command'] == 'join':
            userid = content['userid']
            self.home_session_name = 'home-' + str(userid)
            await self.channel_layer.group_add(
                self.home_session_name,
                self.channel_name
            )
            print(f'[home] {self.home_session_name} session created!!')

        elif content['command'] == 'add-contact':
            userid = content['userid']
            other_user_email = content['other_user_email']
            cont, new, wrong_useremail = await add_contact(userid, other_user_email)
            print(cont,new,wrong_useremail)
            if new or cont is None:
                await self.channel_layer.group_send(
                    self.home_session_name,
                    {
                        'type': 'contact_message',
                        'contact': cont,
                        'new': new,
                        'wrong_useremail': wrong_useremail,
                    }
                )
        elif content['command'] == 'refresh_dp':
            userid = content['userid']
            dp_path = content['dp_path']
            print(content)
            await refresh_all_dp(self, userid, dp_path)

        elif content['command']=='create-story':
            story_path = content['story']
            userid = content['userid']
            await refresh_all_story(self,userid,story_path)




    async def contact_message(self, data):
        cont = data['contact']
        wrong_email = data['wrong_useremail']
        if wrong_email:
            await self.send_json({
                'wrong_useremail': data['wrong_useremail'],
            })
        else:
            await self.send_json({
                'c_id': cont.id,
                'c_username': cont.username,
                'c_profile_pic': cont.profile_pic.name,
                'contact_added': data['new'],
                'wrong_useremail': not data['wrong_useremail'],
            })

    async def add_new_message(self, data):
        message = data['new_message']
        userid = data['userid']
        other_userid = data['other_userid']
        already, other_user = await check_presence(userid, other_userid)
        await self.send_json({
            'new_message': True,
            'message': message,
            'already': already,
            'other_userid': other_userid,
            'other_username': other_user.username,
            'other_useremail': other_user.email,
            'other_profile_pic': other_user.profile_pic.name,

        })

    async def refresh_dp(self, data):
        data['refresh_dp'] = True
        await self.send_json(data)

    async def refresh_story(self,data):
        data['refresh_story'] = True
        await self.send_json(data)


@sync_to_async
def refresh_all_dp(inst, userid, dp_path):
    contacts = Contact.objects.filter(contact=userid) | Contact.objects.filter(user=userid)
    print(inst)
    for cont in contacts:
        contact_id = cont.user.id
        print("contact  ---  ", contact_id)
        if contact_id == userid: contact_id = cont.contact.id
        contact_home_session_name = 'home-' + str(contact_id)
        async_to_sync(group_send)(inst, contact_home_session_name, userid, dp_path)
        print(contact_home_session_name)
    print()

@sync_to_async
def refresh_all_story(inst,userid,story_path):
    contacts = Contact.objects.filter(contact=userid) | Contact.objects.filter(user=userid)
    print(inst)
    for cont in contacts:
        contact_id = cont.user.id
        if contact_id == userid: contact_id = cont.contact.id
        contact_home_session_name = 'home-' + str(contact_id)
        async_to_sync(story_send)(inst, contact_home_session_name, userid, story_path)
        print(contact_home_session_name)


async def group_send(inst, contact_home_session_name, userid, dp_path):
    await inst.channel_layer.group_send(
        contact_home_session_name,
        {
            'type': 'refresh_dp',
            'contact_id': userid,
            'dp_path': dp_path,
        }
    )


async def story_send(inst, contact_home_session_name, userid, story_path):
    await inst.channel_layer.group_send(
        contact_home_session_name,
        {
            'type': 'refresh_story',
            'contact_id': userid,
            'story_path': story_path,
        }
    )


@sync_to_async
def add_contact(userid: int, other_user_email: str):
    wrong_useremail = False
    user = User.objects.filter(id=userid).first()
    other_user = User.objects.filter(email=other_user_email).first()
    if not other_user or user.id == other_user.id: return None, False, True
    cont, new = Contact.objects.get_or_create(user=user, contact=other_user)
    return other_user, new, wrong_useremail


@sync_to_async
def check_presence(userid, other_userid):
    user = User.objects.filter(id=userid).first()
    other_user = User.objects.filter(id=other_userid).first()
    messages = Message.objects.filter(sender=user, receiver=other_user)
    return (True, user) if messages else (False, user)


channel_group = dict()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    chat_session_name = None

    async def connect(self):
        await self.accept()
        print("[Chat] Connected!!")

    async def receive_json(self, content, **kwargs):
        if content['command'] == 'join':
            userid = content['userid']
            other_userid = content['other_userid']
            self.chat_session_name = str(min(userid, other_userid)) + '-' + str(max(userid, other_userid))

            await self.channel_layer.group_add(
                self.chat_session_name,
                self.channel_name,
            )
            print(f"{userid} joined @ ", self.chat_session_name)

        elif content['command'] == 'send':
            userid, other_userid = content['userid'], content['other_userid']
            userid, other_userid = int(userid), int(other_userid)
            message = content['message']
            other_home_name = 'home-' + str(other_userid)

            await self.channel_layer.group_send(
                other_home_name,
                {
                    'type': 'add_new_message',
                    'userid': other_userid,
                    'other_userid': userid,
                    'new_message': message,
                }
            )
            await self.channel_layer.group_send(
                self.chat_session_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'userid': userid,
                    'other_userid': other_userid,
                }
            )

            print("[GROUPS] ::::    ", self.channel_layer.groups)

    async def disconnect(self, code):
        pass

    async def chat_message(self, data):
        message = data['message']
        userid = data['userid']
        other_userid = data['other_userid']
        await self.send_json({
            'userid': userid,
            'message': message,
        })
        print('[chat] message saved!!', channel_group)
