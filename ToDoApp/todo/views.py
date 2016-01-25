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

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import TodoList
from .forms import NewItemForm

def get_new_item(request):
    items = None
    if request.method == 'POST'
        form = NewItemForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/detail/')
    else:
        form = NewItemForm()
    return render(request, 'todo/detail.html', {'form': form})

class IndexView(generic.ListView):
    template_name = "todo/index.html"
    context_object_name = 'latest_todo_list'

    def get_queryset(self):
        return TodoList.objects.order_by('-list_title')[:5]

class DetailView(generic.DetailView):
    model = TodoList
    template_name = 'todo/detail.html'
