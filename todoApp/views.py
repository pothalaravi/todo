# from asyncio import tasks
# from re import T

from dataclasses import dataclass
from turtle import title
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,redirect
# from.models import TodoListitem
import json
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . models import Task
import sweetify
from sweetify.views import SweetifySuccessMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='task'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['task']=context['task'].filter(user=self.request.user)
        context['count']=context['task'].filter(complete=False).count()
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['task']=context['task'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context
        

class TaskListView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = {}
        tasks = Task.objects.filter(user=request.user)
        serialized_tasks = {}
        for task in tasks:
            temp_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "task_date": str(task.task_date),
                    "category": task.category,
                    "completed": task.completed,
                    "created": str(task.created)
                }
            serialized_tasks[task.id] = temp_dict                
            
            task.category = f"{task.category}.gif"
        
        context["tasks"] = tasks
        context["serialized_tasks"] = json.dumps(serialized_tasks)
        
        return render(request, template_name='todoApp/task_list_v2.html', context=context)

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
    templates_name="todoApp/task_detail.html"


class TaskCreate(SweetifySuccessMixin, LoginRequiredMixin,CreateView):
    model = Task
    fields=['title','description','completed', 'task_date', 'category']
    success_message = "Task Added Successfully .!"
    success_url = reverse_lazy('task')
    
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, TemplateView):
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            print(data)
            task_id = kwargs['pk']
            completed = False
            if 'completed' in data:
                completed = data['completed'] == 'true'
                
            Task.objects.filter(id = task_id).update(
                title = data['title'],
                category = data['category'],
                description = data['description'],
                task_date = None if data['task_date'] == '' else data['task_date'],
                completed = completed
            )
            
            sweetify.success(request, "Successfully Updated .!")
        except Exception as err:
            print(err)
            sweetify.error(request, "Error Occured, PLease try again later .!")
            pass
        return redirect("task")
    
    
class TaskDelete(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            task_id = kwargs['pk']
            task_obj = Task.objects.get(id = task_id)
            task_obj.delete()
            sweetify.success(request, 'Successfully Deleted')
        except ObjectDoesNotExist:
            sweetify.warning(request, "No Record Found.!")
        except Exception as err:
            print(err)
            sweetify.error(request, "Error Occured, Please try later.!")
        
        
        return redirect('task')
            
    
class CustomLoginView(LoginView):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('task')
        return render(request, 'todoApp/login.html')
    
    def post(self, request):
        data = request.POST
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('task')
        else:
            sweetify.error(request, "Wrong Credentials..!")
            return redirect('login')
        
        
    
class RegisterPage(FormView):
    template_name="todoApp/register.html"
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('task')
    
    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super (RegisterPage,self).form_valid(form)
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage,self).get(*args,*kwargs)
    


   
    
    
    