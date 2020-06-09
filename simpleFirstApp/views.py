from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.html import escape
import subprocess
import json

from io import StringIO, BytesIO

from simpleDjangoProject.settings import EMAIL_HOST_USER
from .models import Students, Teachers, Courses, StudentSubjects, Subjects
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
roomlist=[]
def ShowChatHome(request):
    return render(request,"chat_home.html")

def ShowChatPage(request,room_name,person_name):
    return render(request,"chat_screen.html",{'room_name':room_name,'person_name':person_name})
    #return HttpResponse("Chat page "+room_name+""+person_name)


def Details(request):


    #print(request.POST)
    text=request.POST.get('l2')
    text1=request.POST.get('l3')
    #print(text)
    inputtext=request.POST.get('l4')
    print(inputtext)
    if len(inputtext)==0:
        pass
    else:
        fh2=open('input_file','w+')
        fh2.write(inputtext)
        fh2.close()
    file_=open('log.txt','w+')
    # print(text,text1)
    if text1=='Language' or len(text)==0:
        res = {'result':'No output'}
        return JsonResponse(res)

    elif text1=='C':
            fh=open('C1.c','w+')
            fh.write(text)
            fh.close()
            subprocess.run('cat input_file | make C1 >& output1.txt',shell=True,stdout=file_)
            subprocess.run('cat input_file | ./C1 >& output.txt',shell=True,stdout=file_)
            file_.close()
            fh=open('output1.txt','r+')
            k1=fh.read()
            fh.truncate(0)
            fh.close()
            fh1=open('output.txt','r+')
            k=fh1.read()
            fh1.truncate(0)
            fh1.close()
            # print(k)
            if len(k1)>20:
                res = {'result':k1[20:]}
            else:
                res = {'result':k}
            return JsonResponse(res)
            
            
    elif text1=='CPP':
            fh=open('Cpp1.cpp','w+')
            fh.write(text)
            fh.close()
            subprocess.run('cat input_file | make Cpp1 >& output1.txt',shell=True,stdout=file_)
            subprocess.run('cat input_file | ./Cpp1 >& output.txt',shell=True,stdout=file_)
            file_.close()
            fh=open('output1.txt','r+')
            k1=fh.read()
            fh.truncate(0)
            fh.close()
            fh1=open('output.txt','r+')
            k=fh1.read()
            fh1.truncate(0)
            fh1.close()
            # print(len(k1))
            if len(k1)>28:
                res = {'result':k1[27:]}
            else:
                res = {'result':k}
            return JsonResponse(res)
            
    elif text1=='Java':
        fh=open('Java1.java','w+')
        fh.write(text)
        fh.close()
        subprocess.run('cat input_file | javac Java1.java >& output1.txt',shell=True,stdout=file_)
        subprocess.run('cat input_file | java Java1 >& output.txt',shell=True,stdout=file_)
        file_.close()
        fh=open('output1.txt','r+')
        k1=fh.read()
        fh.truncate(0)
        fh.close()
        fh=open('output.txt','r+')
        k=fh.read()
        fh.truncate(0)
        fh.close()
        # print(len(k1))
        if len(k1)!=0 :
            res={'result':k1}
        else:
            res = {'result':k}
        return JsonResponse(res)
        

    elif text1=="Python":
        fh=open('p1.py','w+')
        fh.write(text)
        fh.close()
        subprocess.run('cat input_file | python3 p1.py >& output.txt',shell=True,stdout=file_)
        file_.close()
        fh=open('output.txt','r+')
        k=fh.read()
        fh.truncate(0)
        fh.close()
        res = {'result':k}
        return HttpResponse(json.dumps(res), content_type="application/json")







    # text=request.POST.get('l2')
    # file_=open('log.txt','w+')
    # fh=open('p1.py','w+')
    # fh.write(text)
    # fh.close()
    # subprocess.run('cat input_file | python3 p1.py >& output.txt',shell=True,stdout=file_)
    # file_.close()
    # fh=open('output.txt','r+')
    # k=fh.read()
    # fh.truncate(0)
    # fh.close()
    # res = {'result':k}
    # return HttpResponse(json.dumps(res), content_type="application/json")