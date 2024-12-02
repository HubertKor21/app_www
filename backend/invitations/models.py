from django.apps import apps
from django.db import models
from django.db.models import Sum
import uuid

class Family(models.Model):
    name = models.CharField(max_length=150)
    created_by = models.ForeignKey('accounts.CustomUserModel', null=True, on_delete=models.CASCADE,related_name='fam')

    # We define the ForeignKey field directly here, not as a @property
    members = models.ManyToManyField('accounts.CustomUserModel', related_name='families' , blank=True)

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()
    

class Invite(models.Model):
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='invites')

    def get_user_model(self):
        CustomUserModel = apps.get_model('accounts', 'CustomUserModel')
        return CustomUserModel

    @property
    def invited_by(self):
        CustomUserModel = self.get_user_model()
        return models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='sent_invites')

    def __str__(self):
        return f'Invite to {self.family.name} for {self.email}'
