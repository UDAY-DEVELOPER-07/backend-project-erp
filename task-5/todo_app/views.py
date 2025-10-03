from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import TODOS
from .functions import check_regex
from .constants import stringcheck, pass_check, data_fields, Post_data_fileds, field_check
import json


def SignUp(request):
    if request.method == 'POST':
        if(request.body == b''):
            return JsonResponse({"msg" : "Please Use the proper json format to send the data"}, status = 400)
        data = json.loads(request.body)
        if (data_fields  in list(data.keys())):
            return JsonResponse(
                {
                    "msg" : "Please give me all the required fields"
                }, 
                status = 400
                )
        if ((check_regex(stringcheck, data.get('username')) is None ) or (check_regex(pass_check, data.get('password')) is None)):
            return JsonResponse(
                {
                    "msg" : "Use valid pattern Password  (Make sure you are giving all the required field)"
                }, 
                status = 400
            )
        user, created = User.objects.get_or_create(username=data.get('username'))
        user.set_password(data.get('password'))
        user.save()
        if(created): return JsonResponse({"msg" : "User Created Successfully"}, status = 201)
        if(user): return JsonResponse({"msg" : "User already exists"},status = 409)
    else:return JsonResponse({"msg":"Invalid Method"}, status = 405) 

def SignIn(request):
    if request.method == 'POST':
        if(request.body == b''):
            return JsonResponse({"msg" : "Please Use the proper json format to send the data"}, status = 400)
        data = json.loads(request.body)
        if (data_fields  in list(data.keys())):
            return JsonResponse({"msg" : "Please give me all the required fields"}, status = 400)
        if request.user.is_authenticated:
                return JsonResponse({"msg":"Already Logged In "}, status = 409) 
        user = authenticate(username = data.get('username') , password = data.get('password'))
        if user is not None:  
            login(request, user)
            return JsonResponse({"msg":"Logged In Successfully"}, status = 200) 
        else:
            return JsonResponse({"msg":"Wrong Credentials"}, status = 401)
    else:return JsonResponse({"msg":"Invalid Method"},status = 405) 

def SignOut(request):
    if request.method == 'DELETE': 
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"msg":"Log Out"}, status = 200) 
        return JsonResponse({"msg":"No Active User"}, status = 401)
    else:return JsonResponse({"msg":"Invalid Method"}, status = 405)     

def view_todos(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            data = TODOS.objects.filter(user = request.user).exclude(is_deleted = True).values('title', 'description', 'id')
        else:
            return JsonResponse({"msg" : "No user is Logged In Currently"}, status = 401)
        return JsonResponse(list(data), safe=False)
    else:return JsonResponse({"msg":"Invalid Method"}, status = 405)

def del_todos(request, id):
    if request.method == 'DELETE':
        if not request.user.is_authenticated:
            return JsonResponse({"msg" : "Please Log In"}, status = 401)
        if(TODOS.objects.filter(user = request.user, id = id).exists() == False) :
            return JsonResponse({"msg" : "Data does not exist for the current user"} ,status = 400)
        else:
            del_instance = TODOS.objects.get(user = request.user, id = id)
        if  del_instance.is_deleted == True:
            return JsonResponse({"msg" : "Nothing to delete"}, status = 200)
        else:
            del_instance.is_deleted = True
            del_instance.save()
        return JsonResponse({"msg" : "Deleted Successfully"}, status = 200)
    else:return JsonResponse({"msg":"Invalid Method"}, status = 405)

def update_todos(request, id):
    if request.method == 'PUT':
        if request.body == b'':
            return JsonResponse({"msg" : "Please some data and it should be in json format"}, status = 400)
        if not request.user.is_authenticated:
            return JsonResponse({"msg" : "Please Log In"}, status = 401)
        data = json.loads(request.body)
        if(len(data.values()) == 0):
            return JsonResponse({"msg" : "Please provide required data"}, status = 400)
        update_field = list(data.keys())
        if(Post_data_fileds not in update_field):
            return JsonResponse({"msg" : "Please give all the required fields"}, status = 400)
        todo_instance = TODOS(id = id, user = request.user)
        todo_instance.title = data.get('title')
        todo_instance.description = data.get('description')
        todo_instance.save(force_update=True, update_fields = update_field)
        return JsonResponse({"msg" : "Updated Successfully"}, status = 200)
    else:return JsonResponse({"msg":"Invalid Method"}, status = 405)

def create_todos(request):
    if request.method == 'POST':
        if request.body == b'':
            return JsonResponse({"msg" : "Please some data and it should be in json format"}, status = 400)
        if not request.user.is_authenticated:
            return JsonResponse({"msg" : "Please Log In"}, status = 401)
        data = json.loads(request.body)
        if not (list(data.keys()) == Post_data_fileds):
            return JsonResponse({"msg" : "Please give me all the required fields"}, status = 400)
        if((check_regex(field_check, data.get('title')) is None) or (check_regex(field_check, data.get('description')) is None)):
            return JsonResponse({"msg" : "Please provide required data"}, status = 400)
        TODOS.objects.create(
            title = data.get('title'), 
            description = data.get('description'), 
            user = request.user
        )
        return JsonResponse({"msg" : "Todo created Successfully"}, status = 201)
    else:return JsonResponse({"msg":"Invalid Method"}, status = 405)

def completed(request, id):
    if request.method == 'PATCH':
        if request.body == b'':
            return JsonResponse({"msg" : "Please some data and it should be in json format"}, status = 400)
        if not request.user.is_authenticated:
            return JsonResponse({"msg" : "Please Log In"}, status = 401)
        todo_instance = TODOS.objects.get(id = id ,user = request.user)
        if(todo_instance.marked == True):
            return JsonResponse({"msg":"Already Completed"}, status = 409)
        else:
            todo_instance.marked = True
            todo_instance.save()
            return JsonResponse({"msg" : "Marked Completed"}, status = 200)
    else:return JsonResponse({"msg":"Invalid Method"}, status = 405)
