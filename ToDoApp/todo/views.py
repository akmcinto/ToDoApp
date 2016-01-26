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
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import TodoList, Item
from .forms import NewItemForm, NewListForm

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
