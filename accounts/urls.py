from django.urls import path
from . import views

urlpatterns=[
    path('users/', views.GamezoneUserViewset.as_view(), name="listusers" ),
    path('users/<int:pk>/', views.RetrieveUSerView.as_view(), name="listuser" ),
    path('users/<int:pk>/remove/', views.DestroyUserView.as_view(), name="delete_user"),
    path('users/<int:pk>/edit/', views.UpdateUserView.as_view(), name="update_user"),
    path('profile/<int:id>/', views.ProfileView.as_view({"get":"retrieve",
                                                         "post":"create",
                                                         "patch": "edit_profile"}), name="getprofile" )
]
