from django.db import models
from django.urls import reverse # Returns the full path as a string
from django.template.defaultfilters import slugify

from PIL import Image

from users.models import Profile

# Create your models here.
# We need to write here what we want to save in our database
# The user model is already present, we can add a field

# Each class is a table in the database
# Each attribute is a different field in the db

# To query information about a foreignkey user the ..._set attribute

class Sezione(models.Model):
    name = models.CharField(max_length=50, default=1)
    # Deprecated se tutto funziona
    # libri_sezione = models.ManyToManyField(Libro)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Sezione, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Libro(models.Model):
    CONDIZIONI = [
        ('Come Nuovo', 'Come Nuovo'),
        ('Buone', 'Buone'),
        ('Decenti', 'Decenti'),
        ('Pessime', 'Pessime'),
    ]

    ANNO = [
        ("5", "5"),
        ("4", "4"),
        ("3", "3"),
        ("2", "2"),
        ("1", "1"),
        ('Biennio', 'Biennio'),
        ('Triennio', 'Triennio')
    ]

    DIGITALE = [
        ("Già Utilizzata", "Già Utilizzata"),
        ("Non Utilizzata", "Non Utilizzata")
    ]

    name = models.CharField(max_length=50, default='nome_libro')
    isbn = models.BigIntegerField(help_text="Non mettere il trattino, solo il numero.")
    condizioni = models.CharField(max_length=15, choices=CONDIZIONI, default='Buone')
    prezzo = models.DecimalField(max_digits=6, decimal_places=2, help_text="Non mettere il simbolo dell'Euro!")
    # foto_libro = models.ImageField(default='default.png', upload_to='foto_libro')
    recapito_mail = models.ForeignKey(Profile, on_delete=models.CASCADE)
    materia = models.ForeignKey(Sezione, on_delete=models.CASCADE)
    anno = models.CharField(max_length=15, choices=ANNO, default="1")
    area_digitale = models.CharField(max_length=15, help_text="E' stata attivata l'area digitale?", choices=DIGITALE, default="Già Utilizzata") 

    def __str__(self) -> str:
        return str(self.name)

    # Called when a new Libro object is created in the schedules-create page
    # Basically redirects to the appropriate class page after a schedule is added
    def get_absolute_url(self):
        return reverse('libro-detail-page', kwargs={'pk': self.id})
    
    # Method that gets run after our model is saved, it overrides the default one
    def save(self, * args, **kwarg):
        self.name = self.name.capitalize()
        # runs the save method of our parent class. It saves the stuff.
        super().save(*args, **kwarg)
        # img = Image.open(self.foto_libro.path) # Opens the img of the current instance using its path

        # if img.height > 600 or img.width > 600:  # If either the h or w of the current img is greater than 300
        #     output_size = (620, 620)  # tuple of our max sizes
        #     img.thumbnail(output_size)  # resizes
        #     img.save(self.foto_libro.path)  # overwrites the previous img