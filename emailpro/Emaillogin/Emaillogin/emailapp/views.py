from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import Group
from .models import user_datails
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
# from django.urls import reverse
# from django.urls import re_path
# from django.core.mail import EmailMessage
# from .utils import generete_token
# import uuid

User=get_user_model()

@api_view(['POST'])
def Registration(request):
    #email validation 
    if 'email' not in request.data:
        return Response({"status":"empty email"})
    if request.data["email"] == '':
        return Response({"status":"fill email"})
    if User.objects.filter(email=request.data["email"].strip()).exists():
        return Response({"status":"email is allready exist"})

    #firstname validation
    if 'first_name' not in request.data:
        return Response({"status":"empty firstname"})
    if request.data["first_name"].strip() == '':
        return Response({"status":"fill first_name"})

    # #lastname validation

    if 'last_name' not in request.data:
        return Response({"status":"empty firstname"})
    
    if request.data["last_name"].strip() =='':
        return Response({"status":"fill last_name"})

    if request.data["password"].strip() =='':
        return Response({"status":"fill password"})

    id = User.objects.create_user(email=request.data["email"].strip(),password=request.data["password"],first_name=request.data["first_name"],
                            last_name=request.data["last_name"])

    a=user_datails.objects.create(user_id=id, dob=request.data["dob"],bio=request.data["bio"])
    token=Token.objects.get_or_create(user=id)
    token = " ".join([str(x) for x in token]).replace("True",'').strip()
    print(token)
    id.is_active=False 
    id.save()

    email_body='http://127.0.0.1:8000/activate/'+token
    email_subject='Activate your Account',

    #send mail to activate account
    send_mail(
     email_subject,
     email_body,
     'test.softude@gmail.com',
     [request.data["email"]],
     fail_silently=False,
     )
    return Response({"status":"all set",'message':"go to the your emailid and click on the activation link to confirm"})

#Account Activation Api
@api_view(['GET'])
def activate(request, token):
    try:
        tokens = Token.objects.get(key = token)
        user=tokens.user
        if user:
            user.is_active = True
            user.save()
            login(request, user)
            Token.objects.filter(key = token).delete()
            return Response({"status":"all set",'message':"activated"})
        else:
            return Response({"status":"fail",'message':"activation failed"})
    except:
        return Response({"status":"fail",'message':"Token matching query does not exist"})

#User login api
@api_view(['POST'])
def user_login(request):
    try:
        #email validation 
        if 'email' not in request.data:
            return Response({"status":"empty email"})
        if request.data["email"] == '':
            return Response({"status":"fill email"})
        if 'password' not in request.data:
            return Response({"status":"empty password"})            
        if request.data["password"].strip() =='':
            return Response({"status":"fill password"})

        u_email=request.data["email"].strip()
        u_password=request.data["password"].strip()
        user=authenticate( email=u_email , password = u_password )
        if user:    
            login(request, user)
            token=Token.objects.get_or_create(user=user)
            return Response({
                'status':'success',
                'token':str(token)   
            })
        else:
            return Response({
                'status':'fail',
                'message':"invalid credentials"
            })
    except Exception:
        return Response({
            'status':'fail',
            'message':"something went wrong"
        })

#get user data 
@api_view(["GET"])
def get_data(request):
    try:
        token = Token.objects.get(key = request.headers["Authorization"])
        id =token.user_id
        if id:
            userd=User.objects.filter(id=id).values("id","email","first_name","last_name")
            user_data=user_datails.objects.filter(user_id=userd[0]["id"]).values("dob","bio")
            print(user_data)
            data=userd[0]
            for i,j in user_data[0].items():
                data[i]=j
                return Response({
                        'status':'success',
                        'massage':"login" ,
                        'all data':data  
                    })
    except:
        return Response({
                                'status':'fail',
                                'massage':"token does not match"   
                            })
            
    # try:
    #     if uid:
    #         userd=User.objects.filter(id=uid).values("id","email","first_name","last_name")
    #         user_data=user_datails.objects.filter(user_id=userd[0]["id"]).values("dob","bio")
    #         print(user_data)
    #         data=userd[0]
    #         for i,j in user_data[0].items():
    #             data[i]=j
    #        
    #             if request.user.is_authenticated:
    #                 return Response({
    #                         'status':'success',
    #                         'massage':"all data" ,'data':data  
    #                     })
            
    #             return Response({
    #                         'status':'fail',
    #                         'massage':"plz login first"   
    #                     })
            
    # except:
    #     return Response({
    #         'status':'fail',
    #         'message':"this user is not available"
    #     })
        
    #all data 
        
    # userd=User.objects.all().values("id","email","first_name","last_name")
    # user_data=user_datails.objects.all().values("bio",'dob')
  

    # alldata=[]
    # for i in range(len(userd)):
    #     data=userd[i]
    #     alldata.append(data)
    #     for k,v in user_data[i].items():
    #         data[k]=v
    # print(alldata)
    # return Response({
    #             'status':'success',
    #             'message':"all data",
    #             'data':alldata
    #         })




#delete user data 
@api_view(['PUT'])
def Update_data(request, uid):
    try:
      
          #firstname validation
        if 'first_name' not in request.data:
            return Response({"status":"fail","message":"empty firstname"})
        if request.data["first_name"].strip() == '':
            return Response({"status":"fail","message":"fill first_name"})

         #lastname validation
        if 'last_name' not in request.data:
            return Response({"status":"fail","message":"empty firstname"})
        if request.data["last_name"].strip()=='':
            return Response({"status":"message","message":"fill last_name"})
    
        #dob validation
        if 'dob' not in request.data:
            return Response({"status":"fail","message":"empty dob"})
        if request.data["dob"].strip()=='':
            return Response({"status":"fail","message":"fill dob"})

        #bio validation
        if 'bio' not in request.data:
            return Response({"status":"fail","message":"empty bio"})
        if request.data["bio"].strip()=='':
            return Response({"status":"fail","message":"fill bio"})
        user=User.objects.filter(id=uid)
        if user.exists():
            User.objects.filter(id=uid).update(first_name=request.data["first_name"],last_name=request.data["last_name"])
            user_datails.objects.filter(user_id=uid).update(bio=request.data["bio"],dob=request.data["dob"])
        
            return Response({"status":"success","message":"update successfully"})
        return Response({"status":"fail","message":"this id is not avalaible"})
    except:
        return Response({"status":"fail","message":"something went wrong"})


#update partially user data
@api_view(["PATCH"])
def Update_data_patch(request,uid):
    myDict = dict(request.data.lists())
    data={}
    userdata={}
    user_dataildata={}
    for i,j in myDict.items():  
        data.update({i:j[0]})
  
    if "bio" in data:
        userdata["bio"]=request.data["bio"]
    if "first_name" in data:
        user_dataildata["first_name"]=request.data["first_name"]
    if "last_name" in data:
        user_dataildata["last_name"]=request.data["last_name"]
    if "dob" in data:
        userdata["dob"]=request.data["dob"]
    if "email" in data:
        user_dataildata["email"]=request.data["email"]      
    #firstname validation
    if 'first_name' not in request.data:
        return Response({"status":"fail","message":"empty firstname"})
    if request.data["first_name"].strip() == '':
        return Response({"status":"fail","message":"fill first_name"})

    #lastname validation
    if 'last_name' not in request.data:
        return Response({"status":"fail","message":"empty firstname"})
    if request.data["last_name"].strip()=='':
        return Response({"status":"message","message":"fill last_name"})

    #dob validation
    if 'dob' not in request.data:
        return Response({"status":"fail","message":"empty dob"})
    if request.data["dob"].strip()=='':
        return Response({"status":"fail","message":"fill dob"})

    #bio validation
    if 'bio' not in request.data:
        return Response({"status":"fail","message":"empty bio"})
    if request.data["bio"].strip()=='':
        return Response({"status":"fail","message":"fill bio"})

    user_datails.objects.filter(user_id=uid).update(**userdata)
    User.objects.filter(id=uid).update(**user_dataildata)
    return Response({"status":"success","message":"update successfully"})


#update user data
@api_view(["DELETE"])
def Delete_data(request,uid):
    try:
        user=User.objects.get(id=uid)
        user_datails.objects.filter(user_id=user).delete()
        user.delete()
        return Response({"status":"success","message":"delete successfully","data":f"user id {uid} has deleted"})    
    except:
        return Response({"status":"fail","message":"this id is not available"})




@api_view(["POST"])
def Reset_password(request):
    
    user= User.objects.get(email= request.data["email"])
    token=Token.objects.get_or_create(user=user
                                      )
    token = " ".join([str(x) for x in token]).replace("True",'').strip()
    email_body='http://127.0.0.1:8000/forget_password/'+token
    email_subject='cleck to reset your password',

    #send mail to activate account
    send_mail(
     email_subject,
     email_body,
     'test.softude@gmail.com',
     [request.data["email"]],
     fail_silently=False,
     )
    return Response({"status":"all set",'message':"go to the your emailid and click on the activation link to confirm"})

@api_view(['GET'])
def Forget_password(request, token):
    try:
        tokens = Token.objects.get(key = token)
        user=tokens.user
        if user:
            user.is_active = True
            user.save()
            login(request, user)
            Token.objects.filter(key = token).delete()
            return Response({"status":"all set",'message':"activated"})
        else:
            return Response({"status":"fail",'message':"activation failed"})
    except:
        return Response({"status":"fail",'message':"Token matching query does not exist"})

@api_view(["POST"])
def logout_user(request):
    # simply delete the token to force a login
    try:
        token = Token.objects.get(key = request.headers["Authorization"])
        token.delete()
        return Response({"status":"success","message":"logout successfull"}) 
    except:
        return Response({"status":"success","message":"this user allready logout"}) 
        

# @api_view(["POST"])
# def logout_user(request):
#     pass
#     print(">>>>>>>>>>>>>>>>>",request.headers["Authorization"])
#     return Response({"status":"fail","message":"this id is not available",'data':request.headers["Authorization"]})
