from django.contrib import admin
from .models import Topic, Room, Message


# Register your models here.

model = {Topic, Room, Message}

for i in model:
    admin.site.register(i)
