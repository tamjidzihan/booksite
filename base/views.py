from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages


from datetime import datetime
import pyrebase

# Create your views here.


settings_name = "bookSite"

config = {
  "apiKey": "AIzaSyDUqEFZgE0SMDzeERWnfxUR94yQC2hHEyk",
  "authDomain": "bookproject-b0709.firebaseapp.com",
  "databaseURL": "https://bookproject-b0709-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "bookproject-b0709",
  "storageBucket": "bookproject-b0709.appspot.com",
  "messagingSenderId": "650500330497",
  "appId": "1:650500330497:web:023f6bf511184b3b01dc00",
  "measurementId": "G-FTCHXJW7SK"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()




def index(request):
    if ('email' in request.session):
        if('login' in request.session):
            request.session['website_name'] = settings_name
            user_id = request.session.get("localid")
            result = database.child("websites").child(user_id).get()
            reports_pass = []
            counter = 0
            for results in result.each() or  []:
                counter +=1
                report_id = results.key()
                report_details = results.val()

                web_append = {"id_send": counter, "id": report_id, "website_url": report_details['website_url']}

                reports_pass.append(web_append)
            return render(request, 'base/index.html', {"data": reports_pass})
    request.session.flush()
    request.session['website_name'] = settings_name
    return HttpResponseRedirect("/login/")

def loginPage(request):
    if ('email' in request.session):
        if('login' in request.session):
            request.session['website_name'] = settings_name
            return HttpResponseRedirect("/")
    request.session.flush()
    request.session['website_name'] = settings_name
    return render(request, 'base/login.html')


def registerPage(request):
    if ('email' in request.session):
        if('login' in request.session):
            request.session['website_name'] = settings_name
            return HttpResponseRedirect("/")
    request.session.flush()
    request.session['website_name'] = settings_name
    return render(request, 'base/register.html')

# def postsignin(request):
#     if("register_user" in request.POST):
#         full_name = request.POST.get("name").strip()
#         username = request.POST.get("username").strip()
#         email = request.POST.get("email").strip()
#         password = request.POST.get("password").strip()
#         confirmpassword = request.POST.get("confirm_password").strip()
#         ret_val = authe.create_user_with_email_and_password(email, password)
#         now = datetime.now()
#         pass_data = {"full_name": full_name, "username": username, "email": email,"approved": 1, "created_at": datetime.timestamp(now)}
#         database.child('user').child(ret_val['localId']).set(pass_data)
#     return HttpResponseRedirect('/')



def postsignin(request):
    if("register_user" in request.POST):
        full_name = request.POST.get("name").strip()
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        confirmpassword = request.POST.get("confirm_password").strip()
        error = False
        if(password != confirmpassword):
            messages.warning(request, "password not matched")
            print("error:password not matched")
            error = True
        if (len(password) < 8):
            messages.warning(request, "Password is too short")
            print("error:Password is too short")
            error = True
        if (len(full_name) == 0):
            messages.warning(request, "Full name is Empty")
            print("error:Full name is Empty")
            error = True
        if (len(username) == 0):
            messages.warning(request, "Username is Empty")
            print("error:Username is Empty")
            error = True
        if (len(email) == 0):
            messages.warning(request, "Email is Empty")
            print("error:Email is Empty")
            error = True

        if(error == False):
            try:
                print("look good")
                ret_val = authe.create_user_with_email_and_password(email, password)
            except:
                messages.warning(request, "Creds already exists.")
                return HttpResponseRedirect('/register/')
            now = datetime.now()
            pass_data = {"full_name": full_name, "username": username, "email": email,"approved": 1, "created_at": datetime.timestamp(now)}
            database.child('user').child(ret_val['localId']).set(pass_data)
            messages.success(request, "User Created Successfully. Please use creds for login.")
            print("User data passed")
            return HttpResponseRedirect('/register/')

        return HttpResponseRedirect('/register/')

    elif("login" in request.POST):
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            ret_val = authe.sign_in_with_email_and_password(email, password)
        except:
            messages.warning(request, 'Credentials error.')
            return HttpResponseRedirect('/login/')
        user_id  = ret_val['localId']
        try:
            user_info_ret = database.child('user').child(user_id).get()
        except:
            request.session.flush()
            request.session['website_name'] = settings_name
            messages.warning(request, 'Credentials error.')
            return HttpResponseRedirect('/login/')
        user_info = user_info_ret.val()
        if(user_info['approved'] != 0):
            messages.warning(request, "Please wait for approvel from Admin.")
            return HttpResponseRedirect('/login/')
        request.session['login'] = True
        request.session['name'] = user_info["full_name"]
        request.session['email'] = email
        request.session['localid'] = user_id
        return HttpResponseRedirect('/')
    elif("forgetpass" in request.POST):
        email = request.POST.get("email")
        try:
            ret_val = authe.send_password_reset_email(email)
            messages.success(request, 'Please check your mail for resetting password.')
            return HttpResponseRedirect("/")
        except:
            messages.warning(request, 'Credentials error.')
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
