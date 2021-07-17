import pyrebase
from datetime import datetime
import json

firebaseConfig = {
    "apiKey": "AIzaSyAm26Gt0wVh52-thqdD1IYuOoo_PZNpV60",
    "authDomain": "boon-88b7e.firebaseapp.com",
    "projectId": "boon-88b7e",
    "databaseURL":"https://boon-88b7e-default-rtdb.firebaseio.com/",
    "storageBucket": "boon-88b7e.appspot.com",
    "messagingSenderId": "529552714708",
    "appId": "1:529552714708:web:c55cafd072a17d5a8e4441",
    "measurementId": "G-QMX3M7NG3Z",
  }

firebase = pyrebase.initialize_app(firebaseConfig)



class Fire:
    def __init__(self,**kwargs):
        self.auth=firebase.auth()
        self.storage=firebase.storage()
        # auth.sign_in_with_email_and_password(email,password)
        self.db=firebase.database()
        self.id=kwargs["id"]
        self.username=kwargs["username"]
        self.name=kwargs["name"]
        self.email=kwargs["email"]
        self.date_joined=kwargs["date_joined"]
        self.uid=self.email.replace("@","").replace(".","")

    def create_user(self):
        if(not self.db.child("users").get().val()):
            self.db.set({"users":"","id_mapping":"","total_users":0})


        if(self.uid not in self.db.child("users").get().val()):
            total_users=self.db.child("total_users").get().val()
            self.db.child("total_users").set(total_users+1)
            self.db.child(f"users/{self.uid}").set({
                "id": self.id,
                "uid": self.uid,
                "username": self.username,
                "contacts":{
                    "admin":0,
                },
                "profile_pic":"https://firebasestorage.googleapis.com/v0/b/boon-88b7e.appspot.com/o/profile-pics%2Fnone.png?alt=media&token=b5c2785c-8187-4930-9b4c-84903f6ac71f",
                "name": self.name,
                "email":self.email,
                "date_joined":self.date_joined
            })
            self.db.child(f"id_mapping/{self.id}").set(self.uid)







    def valid_uid(self,uid):
        if(uid in self.db.child("users").get().val()):
            return True
        else:return False

    def add_contact(self,to_uid):
        if(not self.valid_uid(to_uid)):return False
        else:
            all_contacts=self.db.child(f"users/{self.uid}/contacts").get().val()
            if(self.uid not in self.db.child(f"users/{to_uid}/contacts").get().val()):
                friend=0
                self.db.child(f"users/{to_uid}/contacts/{self.uid}").set(friend)
            all_contacts[to_uid]=1
            self.db.child(f"users/{self.uid}/contacts").set(all_contacts)
            return True


    def send_message(self,to_uid,message):
        if(not self.valid_uid(to_uid)):return False

        if (not self.db.child("inbox").get().val()):
            self.db.child("inbox").set("")
        last_message_id=self.db.child(f"inbox/{to_uid}/{self.uid}/last_message_id").get().val()
        if(not last_message_id):
            last_message_id=0
        self.db.child(f"inbox/{to_uid}/{self.uid}/last_message_id").set(last_message_id+1)
        self.db.child(f"inbox/{self.uid}/{to_uid}/last_message_id").set(last_message_id + 1)
        ct=datetime.now().timestamp()
        msg_id=self.db.child(f"inbox/{to_uid}/{self.uid}").push({
            "message_id":last_message_id+1,
            "message":message,
            "read":False,
            "sent_by":self.uid,
            "datetime":ct,
            "deleted":False,
        })
        msg_id=msg_id['name']
        self.db.child(f"inbox/{self.uid}/{to_uid}/{msg_id}").set({
            "message_id": last_message_id + 1,
            "message": message,
            "read": False,
            "sent_by": self.uid,
            "datetime": ct,
            "deleted": False,
        })
        return True

    def email_to_uid(self,email):
        return email.replace("@","").replace(".","")

    def uid_to_id(self,uid):
        return self.db.child(f"users/{uid}/id").get().val()

    def uid_to_name(self,uid):
        return self.db.child(f"users/{uid}/name").get().val()

    def profile_pic(self,uid):
        return self.db.child(f"users/{uid}/profile_pic").get().val()

    def last_message(self,uid):
        last_msg_id=self.db.child(f"inbox/{self.uid}/{uid}/last_message_id").get().val()

    def id_to_uid(self,id):
        return self.db.child(f"id_mapping/{id}").get().val()

    def friends(self,uid):
        return self.db.child(f"users/{self.uid}/contacts/{uid}").get().val()

    def get_inbox(self):
        if(not self.db.child(f"inbox/{self.uid}").get().val()):return []
        return [[uid,self.uid_to_id(uid),self.uid_to_name(uid),self.profile_pic(uid),self.friends(uid)] for uid in self.db.child(f"inbox/{self.uid}").get().val().keys()]


    def get_chats(self,id):
        to_uid=self.id_to_uid(id)
        all_chats=self.db.child(f"inbox/{self.uid}/{to_uid}").get().val()
        if(not all_chats):
            return []
        all_chats.pop("last_message_id")
        return list(dict(all_chats).values())

    def send_message_id(self,id,message):
        to_uid=self.id_to_uid(id)
        self.send_message(to_uid,message)
        return True

    def get_contacts(self):
        contacts=self.db.child(f"users/{self.uid}/contacts").get().val()
        return contacts

    def changeProfilePic(self,image_url):
        self.db.child(f"users/{self.uid}/profile_pic").set(image_url)
        return
