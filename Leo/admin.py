from django.contrib import admin
# pyrefly: ignore [missing-import]
from .models import Students
# Register your models here.
admin.site.register(Students)