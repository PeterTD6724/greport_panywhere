from django.shortcuts import render,redirect
import pyrebase
from firebase import firebase
import os
import os.path
from django.contrib import auth
import time
from datetime import datetime
from datetime import timezone
import datetime
import pytz
from django.http import HttpResponse
from django.contrib import messages
from google.oauth2 import service_account
from dotenv import load_dotenv
from functools import wraps


load_dotenv()

configFirebase = { 
    
    "apiKey": os.getenv("apiKey.google@api.service.com"),
    "databaseURL": os.getenv("databaseURL.google@api.service.com"),  
    "authDomain": os.getenv("authDomain.google@api.service.com"),
    "projectId": os.getenv("projectId.google@api.service.com"),
    "storageBucket": os.getenv("storageBucket.google@api.service.com"),
    "messagingSenderId": os.getenv("messagingSenderId.google@api.service.com"),
    "serviceAccount": os.getenv("FserviceAccount.google@api.service.com"),
    "appId": os.getenv("measurementId.google@api.service.com")
}


firebase = pyrebase.initialize_app(configFirebase)
authe = firebase.auth()
database = firebase.database()
# auth = firebase.auth()
storage = firebase.storage()


def home(request):
    return render(request, 'whitefreport/main.html')

def signin(request):
    return render(request, 'whitefreport/signin.html')

# def login_required(f):
#     @wraps(f)
#     def wrap(request, *args, **kwargs):
#         idtoken = request.session.get('uid')
#         if idtoken:
#             try:
#                 # Check if the token is still valid
#                 authe.get_account_info(idtoken)
#                 return f(request, *args, **kwargs)
#             except:
#                 # If the token is invalid or expired, redirect to login
#                 messages.error(request, "Session expired. Please log in again.")
#                 return redirect('signin')
#         else:
#             # If no session is found, redirect to login
#             messages.error(request, "You must be logged in to view this page.")
#             return redirect('signin')
#     return wrap

def login_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        idtoken = request.session.get('uid')
        if idtoken:
            try:
                # Check if the token is still valid
                authe.get_account_info(idtoken)
                print("Token valid, proceeding to view.")
                return f(request, *args, **kwargs)
            except:
                # If the token is invalid or expired, redirect to login
                print("Token invalid, redirecting to signin.")
                messages.error(request, "Session expired. Please log in again.")
                return redirect('signin')
        else:
            # If no session is found, redirect to login
            print("No session found, redirecting to signin.")
            messages.error(request, "You must be logged in to view this page.")
            return redirect('signin')
    return wrap


@login_required
def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:    
        user = authe.sign_in_with_email_and_password(email, passw)
    # except:
    #     message=("invalid credentials")
    #     return render(request, 'whitefreport/main.html', {'messg':message})
        print(user['localId'])
      
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        
        idtoken = request.session["uid"]
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        # print(user['idToken'])
       
        name = database.child('users').child(a).child('details').child('name').get().val()
        messages.success(request, "You are successfully logged in as User:")
        print(name)    
        return render(request, 'whitefreport/welcome.html', {'e':name})
               
    except:
        message=("Invalid credentials, or no internet connection")
        return render(request, 'whitefreport/signin.html', {'messg':message})
      
def logout(request):
    # auth.logout(request)
    try:
      del request.session['uid']
    except KeyError: 
        pass
    return render (request, "whitefreport/signin.html") 

def signUp(request):
    return render(request, 'whitefreport/signup.html')

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        # authe.send_email_verification(user['idToken'])
    except:
        message = "Credentials are not properly set" 
        return render(request, 'whitefreport/signup.html', {'messg':message})
    uid = user['localId']

    data = {"name":name,"status":email}
    
    database.child("users").child(uid).child("details").set(data)
    return render(request, "whitefreport/main.html")

@login_required
def create(request):
    idtoken = request.session["uid"]
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request, 'whitefreport/create.html',{'e':name})

def post_create(request):
    tz = pytz.timezone('Europe/London')
    time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis)) 
    make = request.POST.get('make')
    task = request.POST.get('task')
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    url = request.POST.get('url')
  
    try:
        idtoken = request.session["uid"]
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        print("info"+str(a))
        data = {
            "make": make,
            "task": task,
            "work": work,
            "progress": progress,
            "url": url
            }
            
        database.child('users').child(a).child('reports').child(millis).set(data)
        messages.success(request, "Report successfully submited! ")
        name = database.child('users').child(a).child('details').child('name').get().val()
        return render(request,"whitefreport/welcome.html",{'e':name})
    except KeyError:
        message=("Oooops! User logged out Please Sign in again")
        return render(request, 'whitefreport/signin.html', {'messg':message})

@login_required   
def check(request):
    idtoken = request.session.get('uid')
    
    if not idtoken:
        return redirect('signin')  # Redirect to login if no session
    try:
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']
        name = database.child('users').child(a).child('details').child('name').get().val()
        timestamps = database.child('users').child(a).child('reports').shallow().get().val()
        if not timestamps:
            return render(request, "whitefreport/check.html", {"message": "You still haven't added data to your database",'e': name,'uid': a})
        list_time = sorted(timestamps, reverse=True)
        make = []
        task = []
        work = []
        date = []
        for i in list_time:
            mak = database.child('users').child(a).child('reports').child(i).child('make').get().val()
            tsk = database.child('users').child(a).child('reports').child(i).child('task').get().val()
            wor = database.child('users').child(a).child('reports').child(i).child('work').get().val()
            dat = datetime.datetime.fromtimestamp(float(i)).strftime('%a %d %b %y / %H:%M')
            make.append(mak)
            task.append(tsk)
            work.append(wor)
            date.append(dat)
        comb_list = zip(list_time, date, work, task, make)
        return render(request, 'whitefreport/check.html', {'comb_list':comb_list, 'e':name, 'uid': a})
    except TypeError:
        return render(request, "whitefreport/check.html", {'message': "You still do not have any data in your database.",'e': name,'uid': a})
    except Exception as e:
        return render(request, "whitefreport/check.html", {'message': f"An error occured{str(e)}",'e': name,'uid': a})

def post_check(request):
    time = request.GET.get(str('z'))
    if time is None or time == '':
       
        return HttpResponse("Parameter 'z' is missing or empty", status=400)
    
    try:
        i = float(time)
    except ValueError:
        return HttpResponse("Parameter 'z' is not a valid number", status=400)

    idtoken = request.session["uid"]
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    make = database.child('users').child(a).child('reports').child(time).child('make').get().val()
    task = database.child('users').child(a).child('reports').child(time).child('task').get().val()
    work = database.child('users').child(a).child('reports').child(time).child('work').get().val()
    progress = database.child('users').child(a).child('reports').child(time).child('progress').get().val()
    img_url = database.child('users').child(a).child('reports').child(time).child('url').get().val()
    item_id = database.child('users').child(a).child('reports').child(time).get().key()
    print(img_url)
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%A %d - %B -  %Y / %H:%M')
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,"whitefreport/post_check.html",{'hr':make, 't':task,'w':work,'p':progress, 'd':dat, 'e':name, 'i':img_url, 'm':item_id, 'uid':a})


