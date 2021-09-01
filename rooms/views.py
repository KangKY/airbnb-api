#from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Room
from .serializers import RoomSerializer

class ListRoomsView(ListAPIView):
  queryset = Room.objects.all()
  serializer_class = RoomSerializer

class SeeRoomView(RetrieveAPIView):
  queryset = Room.objects.all()
  serializer_class = RoomSerializer
