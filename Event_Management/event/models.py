from django.db import models
from django.conf import settings
from users.models import CustomUser

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_createdby', null=True, on_delete=models.PROTECT)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
       abstract = True

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()

class Event(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.CharField(max_length=12)
    time = models.TimeField()
    max_attendees = models.PositiveIntegerField()
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="events")
    attendees = models.ManyToManyField(CustomUser, related_name="joined_events", blank=True)

    @property
    def available_slots(self):
        return self.max_attendees - self.attendees.count()

    class Meta:
        db_table = "tbl_event_mst"
