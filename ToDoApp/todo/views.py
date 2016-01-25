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
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from .models import TodoList, Item
from .forms import NewItemForm

def get_new_item(request, kwargs):
    if request.method == 'POST': # If the form has been submitted...
        form = NewItemForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            nitemtext = form.cleaned_data['new_item']
            nitem = Item(item_text=nitemtext, creation_date=datetime.datetime.now(), todo_list=TodoList.objects.get(id=kwargs['pk']))
            nitem.save()

            return HttpResponseRedirect('/detail/') # Redirect after POST
    else:
        form = NewItemForm() # An unbound form

    return render_to_response('detail.html', {
        'form': form,
    })

class IndexView(generic.ListView):
    template_name = "todo/index.html"
    context_object_name = 'latest_todo_list'

    def get_queryset(self):
        return TodoList.objects.order_by('-list_title')[:5]

class DetailView(generic.DetailView):
    model = TodoList
    template_name = 'todo/detail.html'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        get_new_item(request, kwargs)
        return self.render_to_response(context)
