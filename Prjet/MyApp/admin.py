from django.contrib import admin
from .models import ToDoList,Profile

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Profile)