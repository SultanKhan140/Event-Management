from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

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

class CustomUser(AbstractUser):
    role_ref = models.ForeignKey('RoleMst', on_delete=models.PROTECT, blank=True, null=True)
    groups = models.ManyToManyField(Group,related_name="custom_user_groups",blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    class Meta:
        db_table = "tbl_user_mst"


class RoleMst(BaseModel):
    role_name = models.CharField(max_length=255)
    role_description = models.TextField()

    class Meta:
        db_table = "tbl_role_mst"
