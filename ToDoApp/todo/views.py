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
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext

from .models import TodoList, Item
from .forms import NewItemForm, NewListForm, UserRegistration

# Modified from http://www.tangowithdjango.com/book/chapters/login.html, 2016-01-25
def user_login(request):
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('todo/login.html', {}, context)

# Modified from http://www.tangowithdjango.com/book/chapters/login.html, 2016-01-25
def register(request):
    context = RequestContext(request)
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_form = UserRegistration(data=request.POST)
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            # Update our variable to tell the template registration was successful.
            registered = True
        # Invalid form or forms - mistakes or something else?
        else:
            print (user_form.errors)
    else:
        user_form = UserRegistration()

    return render_to_response(
            'todo/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

@login_required
def new_item(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = NewItemForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            newitem = form.save(commit=False)
            newitem.item_text = form.cleaned_data['item_text']
            newitem.creation_date = datetime.datetime.now()
            newitem.todo_list = TodoList.objects.get(id=pk)
            newitem.save()
            return HttpResponseRedirect(reverse('todo:detail', kwargs={'pk': pk})) # Redirect after POST
    else:
        form = NewItemForm() # An unbound form

    return render(request, 'todo/newitem.html', {'form': form})

@login_required
def new_list(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewListForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            newlist = form.save(commit=False)
            newlist.item_text = form.cleaned_data['list_title']
            newlist.creation_date = datetime.datetime.now()
            newlist.save()
            return HttpResponseRedirect(reverse('todo:index')) # Redirect after POST
    else:
        form = NewListForm() # An unbound form

    return render(request, 'todo/newlist.html', {
        'form': form,
    })

class IndexView(generic.ListView):
    queryset = TodoList.objects.all
    template_name = "todo/index.html"
    context_object_name = 'latest_todo_list'

class DetailView(generic.DetailView):
    model = TodoList
    template_name = 'todo/detail.html'
