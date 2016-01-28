"""
   Copyright 2016 Andrea McIntosh

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 """
import datetime
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

from .models import TodoList, Item
from .forms import NewItemForm, NewListForm

# Modified from http://www.tangowithdjango.com/book/chapters/login.html, 2016-01-25
def user_login(request):
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username, password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('todo:viewlists'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('todo/login.html', {}, context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('todo:index'))

def register(request):
    context = RequestContext(request)
    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        if user_form.is_valid():
            # Save the user's form data to the database.
            new_user = user_form.save()
            new_user.set_password(user_form.cleaned_data.get('password1'))
            new_user.save()
            new_user = authenticate(username=user_form.cleaned_data.get('username'), password=user_form.cleaned_data.get('password1'))
            login(request, new_user)
            return HttpResponseRedirect(reverse('todo:viewlists'))
        # Invalid form or forms - mistakes or something else?
        else:
            print (user_form.errors)
    else:
        user_form = UserCreationForm()

    return render_to_response(
            'todo/register.html',
            {'user_form': user_form,},
            context)

@login_required
def new_item(request, pk):
    if request.method == 'POST':
        form = NewItemForm(request.POST or None)
        if form.is_valid():
            newitem = form.save(commit=False)
            newitem.item_text = form.cleaned_data['item_text']
            newitem.creation_date = timezone.now()
            newitem.todo_list = TodoList.objects.get(id=pk)
            newitem.save()
            return HttpResponseRedirect(reverse('todo:detail', kwargs={'pk': pk})) # Redirect after POST
    else:
        form = NewItemForm()

    return render(request, 'todo/newitem.html', {'form': form})

@login_required
def new_list(request):
    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            newlist = form.save(commit=False)
            newlist.item_text = form.cleaned_data['list_title']
            newlist.creation_date = timezone.now()
            newlist.list_user = request.user
            newlist.save()
            return HttpResponseRedirect(reverse('todo:viewlists'))
    else:
        form = NewListForm() 

    return render(request, 'todo/newlist.html', {
        'form': form,
    })

def index_view(request):
    template_name = "todo/index.html"
    return render(request, template_name)

def view_lists(request):
    latest_todo_list = TodoList.objects.filter(list_user=request.user)
    context = {'latest_todo_list': latest_todo_list}
    return render(request, 'todo/viewlists.html', context)

def list_details(request, pk):
    thislist = TodoList.objects.filter(id=pk)
    list_items = Item.objects.filter(todo_list=thislist)
    context = {'list_items': list_items, 'thislist': thislist, 'listid': pk}

    done = request.POST.getlist('check')
    for i in done:
        item = list_items.filter(id=i)
        for instance in item:
            instance.completed = True
            instance.save()
    return render(request, 'todo/detail.html', context)
