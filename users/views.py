from django.db.models.signals import post_save
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from os import environ

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm  # Importing my own forms for registration. They need to be passed to the templates as context to work
from SezioneSpaccio.models import Sezione, Libro
from users.models import Classe
from .signals import create_profile

# Create your views here.
def register(request):
    # Checking if the request is a POST --> the user as compiled the form and is 
    # making an account
    if request.method == 'POST':
        def get_or_none(model, *args, **kwargs):
            try:
                return model.objects.get(*args, **kwargs)
            except model.DoesNotExist:
                return None

        form = UserRegisterForm(request.POST)

        # Block voltaweb's email addresses
        email = form.data.get('email')

        # Check if the class is valid
        user_class = form.data.get('user_class').upper()

        if user_class == "":
            user_class = 'NESSUNA'
            
        # Checking if they left it blank
        #if user_class == "":
         #   user_class = "Nessuna"
        #else:
        user_class = get_or_none(Classe, name=user_class)        

        if form.is_valid() and 'voltaweb' not in email and user_class != None:
            # Storing the class, nome e cognome for later use in signals, not saved in the model
            form.instance.nome = form.cleaned_data.get('nome').capitalize()
            form.instance.cognome = form.cleaned_data.get('cognome').capitalize()
            form.instance.user_class = user_class
            form.save()
            # Override the post_save signal's firing
            post_save.connect(create_profile, sender=User, weak=False) 

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account creato per {username}. Ora puoi fare il login!')  # Remember to add to the template
            # Redirecting to the login page
            return redirect('/profile/')
        
        elif 'voltaweb' in email:
            messages.warning(request, 'Per favore usa una mail differente da quella scolastica!')
        
        elif user_class == None:
            messages.warning(request, 'Classe non valida!')

    # If it isn't, we just return the empty page
    else:
        # form = UserCreationForm()
        form = UserRegisterForm()
    
    context = {
        'title': 'User Registration', 
        'form': form, 
        'sezioni': Sezione.objects.order_by('name').all()
        }
    return render(request, 'users/register.html', context=context)

@login_required  # Add functionality to an existing function
def profile(request):
    # You should be able to see this page only if you're logged in, thus the decorator
    # If a user is not logged in, it looks for the location /accounts/login/?next=/profile/ by default
    # We can change it in the settings file. The next parameter brings the user to the desired page as
    # soon as they login

    if request.method == 'POST':  # See register method for explanation
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)  # We're going to get a file because of the img update

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your information has been updated!')
            return redirect('/profile/')

    else:
        # Populates the forms with an instance of the current user's information
        u_form = UserUpdateForm(instance=request.user)
        # Populates the forms with an instance of the current profile's information
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'sezioni': Sezione.objects.order_by('name').all(),
    }

    return render(request, 'users/profile.html', context)

class ProfileLibroListView(LoginRequiredMixin, ListView):
    # Will tell our view what model to query to create the list of the elements
    model = Libro

    # Change the template from the default one
    template_name = 'SezioneSpaccio/listaprofilelibri.html'

    # Setting the name of object to loop thru in the template (the one between the {{}})
    context_object_name = 'libri'

    # Objects per page - pagination
    paginate_by = 30

    # Pass extra context
    extra_context = {
        'sezioni': Sezione.objects.order_by('name').all(),
    }

    def dispatch(self, request):
        if request.user.is_authenticated:
            self.profile_libro = request.user.profile
        else:
            messages.warning(request, 'Prima di vedere i tuoi libri, log in o fai un account!')
        return super().dispatch(request)

    def get_queryset(self):  
        return Libro.objects.filter(recapito_mail=self.profile_libro).all()