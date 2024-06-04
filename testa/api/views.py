from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Item
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import SalesItem, InventoryItem

@csrf_exempt
def item_pictures(request, name):
    # Obtén el item por nombre o devuelve un error 404 si no se encuentra
    item = get_object_or_404(Item, name=name)

    # Accede a la imagen del item
    picture = item.picture

    # Abre la imagen en modo binario
    img = picture.open('rb')

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
        try:
            # Obtén el objeto SalesItem correspondiente
            sales_item = SalesItem.objects.get(item=item)
            # Obtén el objeto InventoryItem correspondiente
            inventory_item = InventoryItem.objects.get(item=item)

            item_info = {
                'name': item.name,
                'price': sales_item.price,
                'picture': f'https://django-alpha-eosin.vercel.app/item_picture/{item.name}/',
                'quantity': inventory_item.quantity,
            }
            item_data.append(item_info)
        except (SalesItem.DoesNotExist, InventoryItem.DoesNotExist):
            continue
    
    # Devuelve los items como una respuesta HTTP en formato JSON
    return JsonResponse({'items': item_data})
