from django.urls import path
from . import views
urlpatterns = [
    path('',views.signupPage,name='signupPage'),
    path('login/',views.loginPage,name='loginPage'),
    path('home/',views.home,name='home'),
    path('userLogout/',views.user_logout,name='userLogout'),
    path('adminPage/',views.adminPage,name='adminPage'),
    path('create/',views.create,name='create'),
    path('update/<str:id>',views.update,name='update'),
    path('delete/<str:id>',views.delete,name='delete'),
]