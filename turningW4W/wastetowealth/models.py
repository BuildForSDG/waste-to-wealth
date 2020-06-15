from django.db import models

# Create your models here.
class User(AbstractUser):
    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None
