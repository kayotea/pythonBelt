# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z\s]{3,50}$')
USERNAME_REGEX = re.compile(r'[a-zA-Z0-9.+_-]{3,50}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile(r'^.{8,50}$')
DATE_REGEX = re.compile(r'^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')

ITEM_REGEX = re.compile(r'^.{3,50}$')
DEFAULT_USER = 1

# Create your models here.

class UserManager(models.Manager):
    def add_user(self, postData):
        name = postData['name']
        username = postData['username']
        pwd = postData['password']
        c_pwd = postData['confirm_password']
        date_hired = postData['date']
        print date_hired


        error = []
        #input validations
        if not NAME_REGEX.match(name):
            error.append('Name must be at least 3 characters.')
        if not USERNAME_REGEX.match(username):
            error.append('Username must be at least 3 characters.')
        if User.objects.filter(username=username):
            error.append('User with that username already exists')
        if not PWD_REGEX.match(pwd):
            error.append('Password must be at least 8 characters')
        if pwd != c_pwd:
            error.append('Passwords do not match!')
        if not DATE_REGEX.match(date_hired):
            error.append('Invalid date. Please enter a valid date in the format mm/dd/yyyy')
        #check that username does not already exist
        
        #if no errors, create user
        if len(error) == 0:
            pwd = pwd.encode('utf-8')
            hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            u = User.objects.create(name=name, username=username, password=hashed_pwd, hire_date=date_hired)
            return [True, u]
        #else don't create user, return errors
        else:
            return [False, error]

    def login_user(self, postData):
        username = postData['username']
        pwd = postData['password'].encode('utf-8')
        #look for match in registered usersd
        users = User.objects.all()
        for user in users:
            user.password = user.password.encode('utf-8')
            if username == user.username and bcrypt.hashpw(pwd, user.password) == user.password:
                return [True, user.id]
        return [False, False]
        

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    hire_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __unicode__(self):
        return 'id: '+str(self.id)

class ItemManager(models.Manager):
    def make_item(self, postData):
        user = postData['user']
        item_name = postData['item_name']
        error = []
        if not ITEM_REGEX.match(item_name):
            error.append('Item/product name should be at least 3 characters long.')
        if item_name == " " or item_name == "  " or item_name == "   ":
            error.append('No blank entries please!')
        
        #if no validation errors
        if len(error) == 0:
            print "no error"
            item = Item.objects.create(creator=user, item_name=item_name)
            Wish.objects.create(wish_item=item, wish_user=user)
            return [True, True]
        #if ther are validation errors
        else:
            return [False, error]

class Item(models.Model):
    creator = models.ForeignKey(User, default=DEFAULT_USER)
    item_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()

    def __unicode__(self):
        return 'item id:'+str(self.id)

class Wish(models.Model):
    wish_item = models.ForeignKey(Item)
    wish_user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'wish id:'+str(self.id)