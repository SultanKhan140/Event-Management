from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import  Event
from .serializers import EventSerializer
from users.permissions import IsAdmin, IsOrganizer, IsAttendee
from .pagination import EventPagination
from django.core.mail import send_mail
from django.conf import settings


# Join Event
class JoinEvent(APIView):
    permission_classes = [IsAuthenticated,IsAttendee]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id, is_active=True, is_deleted=False)

            # Check if user is already an attendee
            if request.user in event.attendees.all():
                return Response({"error": "You have already joined this event"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the event has available slots
            if event.attendees.count() < event.max_attendees:
                event.attendees.add(request.user)
                return Response({"message": "Successfully joined the event"}, status=status.HTTP_200_OK)

            return Response({"error": "Event is full"}, status=status.HTTP_400_BAD_REQUEST)

        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

# Event CRUD with Search & Filters
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsOrganizer]
    pagination_class = EventPagination

    def get_queryset(self):
        queryset = Event.objects.filter(is_active = True, is_deleted = False).order_by('-id')
        date = self.request.query_params.get('date')
        location = self.request.query_params.get('location')
        availability = self.request.query_params.get('available')

        if date:
            queryset = queryset.filter(date=date)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if availability == "true":
            queryset = [event for event in queryset if event.available_slots() > 0]

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
