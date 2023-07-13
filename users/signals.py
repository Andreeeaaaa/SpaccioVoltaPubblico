from django.db.models.signals import post_save  # The signal, gets fired after an object is saved
from django.contrib.auth.models import User  # The sender, sends the signal
from django.dispatch import receiver  # Receives the signal fired

from .models import Profile, Classe

# Each time a user is created it makes a profile
# When a user is saved, it sends the post_save signal, received by the function create_profile
# that takes the sender, instance of the sender (of the user), created boolean to see if the user was 
# created.
@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):  #kwargs accepts any keyword argument at the end of the function
    # Creates the same instance of the user as a profile
    if created:
        # Superusers are created thru console so they dont have a class
        if instance.is_superuser:
            classe = Classe.objects.first()
            nome = instance.username
            cognome = ''
            Profile.objects.create(user_profile=instance, classe=classe, nome=nome, cognome=cognome)

        else:
            classe = instance.user_class
            nome = instance.nome
            cognome = instance.cognome
            Profile.objects.create(user_profile=instance, classe=classe, nome=nome, cognome=cognome)


# Saves the profile in the database when the user is saved
@receiver(signal=post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # I access the profile attribute of the user instance and save it

# For that to work you need to import the signal file into the apps.py file of this app
# in a function ready that takes the class as an arg
