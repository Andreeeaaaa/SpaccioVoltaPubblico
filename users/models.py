from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.template.defaultfilters import slugify

# Creating a profile user model that has a 1 to 1 relationship
# with the user model created by django. Remember to run the migrations for the changes to take effect.
# Now we can access the attributes of the Profile class directly from the user (thanks to the 1 to 1)
# ex. AndreqL.profile.user_class  

# Remember to set the null=True if the value is gonna be null at any point 
class Classe(models.Model):
    name = models.CharField(max_length=11, default=1)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Classe, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user_profile = models.OneToOneField(User, on_delete = models.CASCADE) # If the user is deleted, the profile is deleted (not viceversa)
    def get_default():  # Only way to respect contraints and serialize the db
        return Classe.objects.get(name='Nessuna')

    classe = models.ForeignKey(Classe, default=get_default, on_delete=models.PROTECT) # It accepts methods that get called upon event
    nome = models.CharField(max_length=40)
    cognome = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f'{self.user_profile.username} Profile'
