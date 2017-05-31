# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z]{2,50}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile(r'^.{8,50}$')

# Create your models here.

class UserManager(models.Manager):
    def add_user(self, postData):
        f_n = postData['first_name']
        l_n = postData['last_name']
        eml = postData['email']
        pwd = postData['password']
        c_pwd = postData['confirm_password']

        error = []
        #input validations
        if not NAME_REGEX.match(f_n):
            error.append('First name must be at least 2 characters. Name may only contain letters a-z and A-Z')
        if not NAME_REGEX.match(l_n):
            error.append('Last name must be at least 2 characters. Name may only contain letters a-z and A-Z')
        if not EMAIL_REGEX.match(eml):
            error.append('Invalid email address')
        if not PWD_REGEX.match(pwd):
            error.append('Password must be at least 8 characters')
        if pwd != c_pwd:
            error.append('Passwords do not match!')

        #check that email does not already exist
        if User.objects.filter(email=eml).count():
            error.append('User with that email already exists')
        
        #if no errors, create user
        if len(error) == 0:
            pwd = pwd.encode('utf-8')
            hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            u = User.objects.create(first_name=f_n, last_name=l_n, email=eml, password=hashed_pwd)
            return [True, u]
        #else don't create user, return errors
        else:
            return [False, error]
    def login_user(self, postData):
        eml = postData['email']
        pwd = postData['password'].encode('utf-8')
        #look for match in registered users
        users = User.objects.all()
        for user in users:
            user.password = user.password.encode('utf-8')
            if eml == user.email and bcrypt.hashpw(pwd, user.password) == user.password:
                return [True, user.id]
        return [False, False]
        

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __unicode__(self):
        return 'id: '+str(self.id)