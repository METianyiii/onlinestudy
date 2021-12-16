from django.urls import path

from app.user import views

urlpatterns = [
    path('login/', views.studentLogin, name='studentLogin'),
    path('studentRegister/', views.studentRegister, name='studentRegister'),
    path('teacherRegister/', views.teacherRegister, name='teacherRegister'),
    path('logout/', views.logout, name='logout'),
]
