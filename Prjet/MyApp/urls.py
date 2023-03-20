from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('todo/',views.to_do,name='todo'),
    path('todo/completed/',views.todo_completed,name='todo_completed'),
    path('todo/notcompleted/',views.todo_notcompleted,name='todo_notcompleted'),
    path('add_todo',views.add_to_do,name='add_todo'),
    path('user/',views.user_page,name='user_page'),
    path('delete/<int:id>/',views.delete_to_do,name='delete'),
    path('edit/<int:id>/',views.edit_to_do,name='edit'),
    path('register/',views.register,name='register'),
    # path('register/add_pic/',views.add_pic,name='add_pic'),
    path('login/',views.login_User,name='login'),
    path('logout/',views.logout_User,name='logout'),
    path('user/settings/',views.acc_settings,name='acc_settings'),
    path('all_customers/',views.all_customers,name='all_customers'),
    path('all_customers/customer/<str:name>',views.customer,name='customer'),
]
