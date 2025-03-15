from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id','title','description','location','date','time','max_attendees','organizer','attendees','available_slots')
    

    def get_available_slots(self, obj):
        return obj.available_slots

    def validate_max_attendees(self, value):
        if value < 1:
            raise serializers.ValidationError("Maximum attendees must be at least 1.")
        return value
    
    def create(self, validated_data):
        # Ensure available_slots is initialized to max_attendees
        max_attendees = validated_data.get('max_attendees', 1)
        event = Event.objects.create(**validated_data)
        # event.available_slots = max_attendees  # Ensure available_slots = max_attendees
        event.save()
        return event
