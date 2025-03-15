from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import RegisterUser, LoginUser, UserViewSet

router = SimpleRouter()
router.register(r'user', UserViewSet,basename='user-manage')

   
urlpatterns = [  
    path('', include(router.urls)), 
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
]