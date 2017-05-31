# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Item, Wish
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'belt_app/index.html')

def register_process(request):
    if request.method == "POST":
        postData = {
            'name' : request.POST['name'],
            'username' : request.POST['username'],
            'password' : request.POST['password'],
            'confirm_password' : request.POST['confirm_password'],
            'date' : request.POST['date'],
        }
        #validate and add user
        user = User.objects.add_user(postData)
        #if user added
        if user[0]:
            request.session['login'] = user[1].id
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/main')

        #if user created
        if user[0] == True:
            request.session['login'] = user[1].id
            return redirect('/dashboard')
        #if user was not created
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/main')

def login(request):
    if request.method == "POST":
        postData = {
            'username' : request.POST.get('username', False),
            'password' : request.POST['password']
        }
        #check for user and login
        user = User.objects.login_user(postData)
        #if login was successful
        if user[0]:
            request.session['login'] = user[1]
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Invalid login')
            return redirect('/main')

def dashboard(request):
    user = User.objects.get(pk=request.session['login'])
    #get wishes belonging to user, order by most recently created first
    user_wish_list = Wish.objects.filter(wish_user=user).order_by('-created_at')
    #gather wishes logged in user has in their wishlist
    my_wishes = []
    for wish in user_wish_list:
        readable_date = datetime.strftime(wish.created_at, '%b %d, %Y')
        my_wishes.append((wish, readable_date))
    #gather wishes other users (but not curr user) have in their lists
    #get list of items that curr has wished for
    user_item_list = Item.objects.filter(wish__wish_user=user)
    #exclude wishes containing items in user_item_list
    #order by most recently created first
    others_wish_list = Wish.objects.exclude(wish_item__id__in=user_item_list).order_by('-created_at')
    others_wishes = []
    for wish in others_wish_list:
        readable_date = datetime.strftime(wish.created_at, '%b %d, %Y')
        others_wishes.append((wish, readable_date))

    context = {
        'user' : user,
        'my_wishes': my_wishes,
        'others_wishes' : others_wishes
    }
    return render(request, 'belt_app/dashboard.html', context)

def create_item(request):
    return render(request, 'belt_app/create_item.html')

def create_item_process(request):
    if request.method == "POST":
        postData = {
            'user' : User.objects.get(pk=request.session['login']),
            'item_name' : request.POST['item']
        }
        item = Item.objects.make_item(postData)
        #if item successfully created
        if item[0]:
            messages.add_message(request, messages.INFO, 'Item successfully created!')
            return redirect('/dashboard')
        else:
            errors = item[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/wish_items/create')

def show_wish_item(request, id):
    item = Item.objects.get(pk=id)
    wishes_with_this_item = Wish.objects.filter(wish_item=item)
    context = {
        'item' : item,
        'wishes_with_this_item' : wishes_with_this_item
    }
    return render(request, 'belt_app/show_item.html', context)

#when user clicks Add To My Wishlist on an existing item
def add_item(request, id):
    item = Item.objects.get(pk=id)
    user = User.objects.get(pk=request.session['login'])
    Wish.objects.create(wish_item=item, wish_user=user)
    return redirect('/dashboard')

def remove_wish(request, id):
    Wish.objects.get(pk=id).delete()
    return redirect('/dashboard')

def delete_item(request, id):
    #get item
    item = Item.objects.get(pk=id)
    #delete wishes afilliated with item
    Wish.objects.filter(wish_item__id=id).delete()
    #delete item
    item.delete()
    return redirect('/dashboard')

def logout(request):
    del request.session['login']
    request.session.modified = True
    messages.add_message(request, messages.INFO, "You've been successfully logged out!")
    return redirect('/main')