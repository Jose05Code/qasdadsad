from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Item, SalesItem, InventoryItem  # Import the missing models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

@csrf_exempt
def ItemList(request):
    # Obtén todos los items
    items = Item.objects.all()

    # Crea una lista para almacenar los datos de cada item
    item_data = []
    
    # Itera sobre cada item y obtén su información
    for item in items:
        # Obtén el objeto SalesItem correspondiente
        sales_item = SalesItem.objects.get(item=item)
        # Obtén el objeto InventoryItem correspondiente
        inventory_item = InventoryItem.objects.get(item=item)

        item_info = {
            'name': item.name,
            'price': sales_item.price,
            'picture': item.picture.url,
            'quantity': inventory_item.quantity
        }
        item_data.append(item_info)
    
    # Devuelve los items como una respuesta HTTP en formato JSON
    return JsonResponse({'items': item_data})