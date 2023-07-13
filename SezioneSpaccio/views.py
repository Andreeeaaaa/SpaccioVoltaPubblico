import django
from django.contrib.auth.models import AnonymousUser, User
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Import models for db
from . import models
from .forms import EmailForm
from . import email_sender

# Create your views here.
# To filter foreign keys use {attribute_name}__name__contains=''


def home_page(request):
    # Check if the user is authenticated to pass a user specific context argument schedule
    if request.user.is_authenticated:

        context = {
            'title': 'Home Page',
            'sezioni': models.Sezione.objects.order_by('name').all(),
        }

    else:
        context = {
            'title': 'Home Page',
            'sezioni': models.Sezione.objects.order_by('name').all(),
        }

    return render(request, 'SezioneSpaccio/home.html', context)


def redirect_home_page(request):
    return redirect("/")


class LibroListView(ListView):
    # Will tell our view what model to query to create the list of the elements
    model = models.Libro

    # Change the template from the default one
    template_name = 'SezioneSpaccio/listalibri.html'

    # Setting the name of object to loop thru in the template (the one between the {{}})
    context_object_name = 'libri'

    # Objects per page - pagination
    paginate_by = 30

    # Pass extra context
    extra_context = {
        'sezioni': models.Sezione.objects.order_by('name').all(),
    }

    def get_queryset(self):  
        # Override queryset to the db
        libri_x_materia = get_object_or_404(
            models.Sezione, name=self.kwargs.get('materia'))
        return models.Libro.objects.filter(materia=libri_x_materia).all()

class LibroDetailView(DetailView):
    # Will tell our view what model to query to create the list of the elements
    model = models.Libro

    template_name = 'SezioneSpaccio/librodetail.html'
    # Pass extra context
    extra_context = {
        'sezioni': models.Sezione.objects.order_by('name').all(),
    }

    # default context object name 'object' in the template and no ordering.

# Pagina di conferma dell'acquisto
def LibroCompraView(request, pk):
    libro = models.Libro.objects.get(id = pk)

    if request.method == 'POST':
        form = EmailForm(request.POST)

        # Block voltaweb's email addresses
        email_compratore = form.data.get('email')

        if form.is_valid() and 'voltaweb' not in email_compratore:
            email = libro.recapito_mail.user_profile.email
            
            # send email
            message = "Ciao, " + libro.recapito_mail.nome + ",\nUn possibile acquirente ha dimostrato interesse per il il tuo libro: " + libro.name + " (ISBN: "  + str(libro.isbn) + ").\n\nPuoi metterti in contatto tramite questo indirizzo email: " + email_compratore + "\nRicordati di rimuovere il libro dal sito nel caso in cui la vendita andasse a buon fine. Puoi eliminare il libro qui: voltastudenti.it/spaccio/libro/" + str(libro.pk) + "/delete/" + ".\n\nBuona fortuna,\nIl Gruppo Tech del Volta.\n\n\nEmail Automatica, si prega di non rispondere se non per segnalare bug o malfunzionamenti."
            email_sender.send_message(email, 'Sezione Spaccio: Qualcuno è interessato a comprare il tuo libro!', message)

            messages.success(request, "Abbiamo inviato una email con le tue informazioni di contatto al venditore del libro!")
            return redirect('home-page')
        
        elif 'voltaweb' in email_compratore:
            messages.warning(request, 'Per favore usa una mail differente da quella scolastica!')

    else:
        if request.user.is_authenticated:
            form = EmailForm(instance=request.user)
        
        else:
            form = EmailForm()
    
    context = {
        'title': 'Conferma Acquisto',
        'sezioni': models.Sezione.objects.order_by('name').all(),
        'libro': libro,
        'form': form
    }

    return render(request, 'SezioneSpaccio/conferma_acquisto.html', context)


class LibroCreateView(LoginRequiredMixin, CreateView):
    model = models.Libro

    # We need to provide the fields that we want to be in the model
    # The starting date will be added automatically later
    fields = ['name', 'isbn', 'condizioni', 'prezzo', 'materia', 'anno', 'condizioni', "area_digitale"]

    # Pass extra context
    extra_context = {
        'nome': "Aggiungi un Libro!",
        'sezioni': models.Sezione.objects.order_by('name').all()
    }

    # Main Function of the view, can get additional arguments
    def dispatch(self, request):
        if request.user.is_authenticated:
            self.recapito_mail = request.user.profile
        else:
            messages.warning(request, 'Prima di mettere in vendita un libro, log in o fai un account!')
        # Run the new overwritten dispatch function in our class
        return super().dispatch(request)
    
    def form_valid(self, form, request=request):
        form.instance.recapito_mail = self.recapito_mail
        form.instance.save()  # Save the instance to the db so I can add it to the class
        return super().form_valid(form)



# Sezione view to update class' schedules
# In that case, the default template will be in <app>/module_form.html
class LibroUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Libro

    # We need to provide the fields that we want to be in the model
    # The starting date will be added automatically later
    fields = ['name', 'isbn', 'condizioni', 'prezzo', 'materia', 'anno', 'condizioni', "area_digitale"]

    template_name = 'SezioneSpaccio/libro_form.html'

    # Pass extra context
    extra_context = {
        'nome': "Modifica il Libro!",
        'sezioni': models.Sezione.objects.order_by('name').all(),
    }

    # Main Function of the view, can get additional arguments
    def dispatch(self, request, **kwargs):
        user_profile = request.user.profile
        profile = models.Libro.objects.get(pk = kwargs['pk']).recapito_mail
        if user_profile != profile:
            messages.warning(request, 'Non hai il permesso di modificare questo elemento.')
            return reverse('home-page')

        # Run the new overwritten dispatch function in our class
        return super().dispatch(request, kwargs['pk'], request.user.profile)

    def get_success_url(self) -> str:
        # Hopefully it redirects where the request came from
        return reverse('profile-libri')


# Sezione view to delete schedules
# In that case, the default template will be in <app>/schedule_confirm_delete.html
class LibroDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Libro

    # Pass extra context
    extra_context = {
        'sezioni': models.Sezione.objects.order_by('name').all()
    }

    # Main Function of the view, can get additional arguments
    def dispatch(self, request, **kwargs):
        user_profile = request.user.profile
        profile = models.Libro.objects.filter(pk=kwargs['pk']).first().recapito_mail
        if user_profile != profile:
            messages.warning(request, 'Non hai il permesso di eliminare questo elemento.')
            return reverse('home-page')

        # Run the new overwritten dispatch function in our class
        return super().dispatch(request, kwargs['pk'], request.user.profile)

    def get_success_url(self) -> str:
        # Hopefully it redirects where the request came from
        return reverse('profile-libri')
