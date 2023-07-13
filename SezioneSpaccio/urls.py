# URL config module
# It needs to be imported to the main url config of the project
# In DjangoWebApp\DjangoWebApp\urls.py

# In this module we map urls to call functions in
# the views module

from django.urls import path
from . import views
from . import models
from django.shortcuts import redirect


# It's important to spell this correctly, django looks for it
# Array of url patterned obects obtained thru the path function
# First argument = url path
# Second argument = reference the the function in the views module.
# The main urls config module passes here requests chopped before
# the /, thus there's no need to write playground/hello in the first argument.
# Always end the routes with a /

# The part in the <> is sent to the views as akeyword argument
urlpatterns = [
    path("", views.home_page, name='home-page'),
    path("AggiungiLibro/", views.LibroCreateView.as_view(), name='aggiungi-libro'),
    path("libro/<int:pk>/", views.LibroDetailView.as_view(), name='libro-detail-page'),
    path("libro/<int:pk>/compra", views.LibroCompraView, name='compra-libro'),
    path("libro/<int:pk>/update/", views.LibroUpdateView.as_view(), name='libro-update'),
    path("libro/<int:pk>/delete/", views.LibroDeleteView.as_view(), name='libro-delete'),
    path("<materia>/", views.LibroListView.as_view(), name='libro-list-page'),
]
