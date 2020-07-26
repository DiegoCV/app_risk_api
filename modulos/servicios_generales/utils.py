import jwt
from .models import Gerente

SECRET_KEY = 'js1@l0sovv%ub(9w-t+0zvm-68ty$%4e#2sns(r1)dev*^hbqd'

def decodificar_jwt_token(request):
    authorization_heaader = request.headers.get('Authorization')
    access_token = authorization_heaader.split(' ')[1]
    decoded_payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
    return decoded_payload

def get_gerente_by_username(request):
	gerente_usuario = decodificar_jwt_token(request)["username"]
	return Gerente.objects.get(gerente_usuario = gerente_usuario)

def get_gerente_by_id(request):
	gerente_id = decodificar_jwt_token(request)["gerente_id"]
	return Gerente.objects.get(gerente_id = gerente_id)

def get_gerente_id(request):
	gerente_id = decodificar_jwt_token(request)["gerente_id"]
	return Gerente.objects.get(gerente_id = gerente_id)