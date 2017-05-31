# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'belt_app/index.html')

def register_process(request):
    if request.method == "POST":
        postData = {
            'first_name' : request.POST['first_name'],
            'last_name' : request.POST['last_name'],
            'email' : request.POST['email'],
            'password' : request.POST['password'],
            'confirm_password' : request.POST['confirm_password']
        }
        #validate and add user
        user = User.objects.add_user(postData)
        if user[0]:
            request.session['login'] = user[1].id
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')

        #if user created
        if user[0] == True:
            request.session['login'] = user[1].id
            return redirect('/')
        #if user was not created
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')

def login(request):
    if request.method == "POST":
        postData = {
            'email' : request.POST['email'],
            'password' : request.POST['password']
        }
        #check for user and login
        user = User.objects.login_user(postData)
        #if login was successful
        if user[0]:
            request.session['login'] = user[1]
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Invalid login')
            return redirect('/')