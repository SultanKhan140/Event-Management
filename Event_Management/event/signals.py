from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event

@receiver(m2m_changed, sender=Event.attendees.through)
def send_join_event_email(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = model.objects.get(pk=user_id)
            subject = f"Confirmation: You Have Joined {instance.title}"
            message = f"""\
Hi {user.username},

You have successfully joined the event: {instance.title}.

Event Details:
----------------------------------
📅 Date: {instance.date}
⏰ Time: {instance.time}
📍 Location: {instance.location}
----------------------------------

Thank you for joining!

Best Regards,  
🎉 Event Management Team
"""
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
