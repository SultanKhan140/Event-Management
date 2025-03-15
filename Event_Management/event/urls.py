from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import EventViewSet ,JoinEvent

router = SimpleRouter()
router.register(r'events', EventViewSet,basename='events-manage')

urlpatterns = [
    path('', include(router.urls)),
    path('events/<int:event_id>/join/', JoinEvent.as_view(), name="join-event"),
]
