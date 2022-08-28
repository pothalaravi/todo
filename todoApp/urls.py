from django.urls import path,include
# from todoApp.views import *
from.views import CustomLoginView, RegisterPage, TaskDelete, TaskList,TaskDetail,TaskCreate,TaskUpdate, TaskListView
from django.contrib.auth.views import LogoutView
urlpatterns =[
    path('',TaskListView.as_view(),name="task"),
    path('task-create/', TaskCreate.as_view(),name="task-create"),
    path('login/',CustomLoginView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(next_page='login'),name="Logout"),
    path('register/', RegisterPage.as_view(),name="register"),
    path('task/<int:pk>/',TaskDetail.as_view(), name="tasks_detail"),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name="tasks-update"),
    path('task-delete/<int:pk>/',TaskDelete.as_view(), name="tasks-delete"),
]   