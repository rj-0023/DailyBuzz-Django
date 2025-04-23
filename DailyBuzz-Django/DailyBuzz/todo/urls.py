from django.urls import path,include   
from . import views
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

router = DefaultRouter()
router.register(r'api/tasks', TodoViewSet, basename='todo')

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create", views.create_task, name="create_task"),
    path("tasks/update/<int:id>", views.update_task, name="update_task"),
    path("tasks/delete/<int:id>", views.delete_task, name="delete_task"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("", include(router.urls)),
    
]



