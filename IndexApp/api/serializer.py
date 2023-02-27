from rest_framework.serializers import ModelSerializer
from IndexApp.models import Room
from django.contrib.auth.models import User

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'