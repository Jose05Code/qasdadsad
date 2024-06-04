from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
import json
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data.get('username')
        password = data.get('password')
        print()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Inicio de sesión exitoso', 'token': str(token.key)})
        else:
            return JsonResponse({'error': 'Nombre de usuario o contraseña incorrectos'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print(auth_header)
        if auth_header is not None:
            token_key = auth_header.split(' ')[1]  # Extract the token from the header
            token = Token.objects.filter(key=token_key).first()
            if token is not None:
                token.delete()
                return JsonResponse({'message': 'Sesión cerrada con éxito'})
            else:
                return JsonResponse({'error': 'Token inválido'}, status=400)
        else:
            return JsonResponse({'error': 'No se proporcionó un token'}, status=400)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            return JsonResponse({'message': 'Usuario creado con éxito'})
        else:
            return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

# Create your views here.