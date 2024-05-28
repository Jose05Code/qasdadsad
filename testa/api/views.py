from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Item
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_picture(request, name):
    # Obtén el item por nombre o devuelve un error 404 si no se encuentra
    item = get_object_or_404(Item, name=name)

    # Accede a la imagen del item
    picture = item.picture

    # Abre la imagen en modo binario
    img = open(picture.path, 'rb')

    # Devuelve la imagen como una respuesta HTTP
    return FileResponse(img)