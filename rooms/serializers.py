from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from users.serializers import UserSerializer
from .models import Photo, Room
from users.models import User

class RoomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      "id",
      "username",
      "avatar",
    )

class PhotoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Photo
    exclude = ("room",)

class RoomSerializer(serializers.ModelSerializer):

  host = RoomUserSerializer(read_only=True)
  #photos = PhotoSerializer(read_only=True, many=True)
  is_fav = serializers.SerializerMethodField()
  

  class Meta:
    model = Room
    fields = (
      "id",
      "name",
      "address",
      "price",
      "beds",
      "lat",
      "lng",
      "bedrooms",
      "bathrooms",
      "check_in",
      "check_out",
      "instant_book",
      "photos",
      "host",
      "is_fav"
    )

    #exclude = ("modified",)
    #fields = '__all__'
    #read_only_fields = ("user", "id", "created", "updated")

  def validate(self, data):
    if self.instance:
      check_in = data.get('check_in', self.instance.check_in)
      check_out = data.get('check_out', self.instance.check_out)
    else:
      check_in = data.get('check_in')
      check_out = data.get('check_out')
    if check_in == check_out:
      raise serializers.ValidationError("Not enough time between check times")
    return data
  
  def get_is_fav(self, obj):
    request = self.context.get("request")
    if request:
      user = request.user
      if user.is_authenticated:
          return obj in user.favs.all()
    return False
  
  def create(self, validated_data):
    request =  self.context.get("request")
    room = Room.objects.create(**validated_data, host=request.user)
    return room


