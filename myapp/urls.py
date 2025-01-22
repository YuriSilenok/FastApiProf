from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/me/', views.CurrentUserView.as_view(), name='current_user'),
    path('users/me/items/', views.UserItemsView.as_view(), name='user_items'),
    path('users/post/', views.CreateUser.as_view(), name='post'),
]
