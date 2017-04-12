# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rango.models import Category,Page,Comment,Notice,Loan,Product
from rango.forms import CategoryForm
from rango.forms import PageForm,CommentForm,NoticeForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from rango.bing_search import run_query
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os.path
import random
from django.http import StreamingHttpResponse


def index(request):
    return render(request, 'main_index.html')


