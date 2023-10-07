# from rest_framework.serializers import ModelSerializer,CharField
# from .models import Profile, GameZoneUser
# from django.contrib.auth.hashers import make_password


# class GamezoneUserSerializer(ModelSerializer):
    
#     password =CharField(
#         write_only=True,
#         required=True,
#         help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )
#     class Meta:
#         model=GameZoneUser
#         fields=[
#            'id','username', 'email', 'password', 'profile'
#         ]
#         read_only_fields = ['profile']


#     def create(self, validated_data):
#         validated_data['password']=make_password(validated_data.get("password"))
#         return super().create(validated_data)
    
#     def update(self, instance, validated_data):
#         pass6=validated_data['password']
#         print(pass6)
#         validated_data['password']=make_password(pass6)
#         print( validated_data['password'])
#         return super().update(instance, validated_data)
    
    
    

# class ProfileSeriaLizer(ModelSerializer):
#     class Meta:
#         model=Profile
#         fields=["id", "country", "location", "profile_pic"]
    
   