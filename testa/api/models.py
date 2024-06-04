from django.db import models
import boto3
from django.conf import settings

def get_upload_to(instance, filename):
    # Obtiene la extensión del archivo
    extension = filename.split('.')[-1]

    # Crea el nuevo nombre del archivo
    new_filename = '{}.{}'.format(instance.name, extension)

    # Retorna la ruta completa del archivo
    return 'item_pictures/{}'.format(new_filename)

class Item(models.Model):
    name = models.CharField(max_length=100)
    sku = models.IntegerField(unique=True)
    gtin = models.IntegerField(unique=True)
    picture = models.ImageField(upload_to=get_upload_to, blank=True)


    def delete(self, *args, **kwargs):
        # Crea un cliente de S3
        s3 = boto3.client('s3')

        # Obtiene el nombre del archivo de la imagen
        picture_name = self.picture.name

        # Elimina el archivo de S3
        s3.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=picture_name,
        )

        # Llama al método delete original
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_delivery = models.DateField()
    next_order = models.DateField()
    masc = models.IntegerField()  # Minimum acceptable stock count
    case_pack = models.IntegerField()  # Number of items in a case

    def __str__(self):
        return str(self.item)

class SalesItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.item)

class OfferItem(models.Model):
    OFFER_TYPES = [
        ('BOGO', 'Buy One Get One'),
        ('BTGO', 'Buy Two Get One'),
        ('B3GO', 'Buy Three Get One'),
        ('FAD', 'Free After Discount')
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    offertype = models.CharField(max_length=4, choices=OFFER_TYPES)  # Offer type
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.item)

class Location(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    aisle = models.IntegerField()
    family = models.CharField(max_length=100)
    shelf = models.IntegerField()
    position = models.IntegerField()
    facings = models.IntegerField()  # Number of facings

    def __str__(self):
        return str(self.item)