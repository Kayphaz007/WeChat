from rest_framework.decorators import api_view
from rest_framework.response import Response
from IndexApp.models import Room
from .serializer import RoomSerializer, UserSerializer
from IndexApp.api import serializer
from django.contrib.auth.models import User



@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/users',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)