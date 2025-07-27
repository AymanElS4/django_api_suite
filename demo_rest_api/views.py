from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid
# Create your views here.


# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    
class DemoRestApiItem(APIView):
    name = "Demo REST API Item"
    
    def _find_item_by_id(self, item_id):
        """
        Método auxiliar para encontrar un elemento por su ID
        """
        for item in data_list:
            if item.get('id') == item_id:
                return item
        return None
    
    def put(self, request, id):
        """
        PUT - Reemplaza completamente los datos de un elemento
        """
        data = request.data
        
        # Validación: el ID debe estar presente en el cuerpo de la solicitud
        if 'id' not in data:
            return Response({
                'error': 'El campo ID es obligatorio en el cuerpo de la solicitud.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validación: el ID de la URL debe coincidir con el del cuerpo
        if data['id'] != id:
            return Response({
                'error': 'El ID en la URL no coincide con el ID en el cuerpo de la solicitud.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar el elemento existente
        existing_item = self._find_item_by_id(id)
        if not existing_item:
            return Response({
                'error': 'Elemento no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Eliminar el elemento existente de la lista
        data_list.remove(existing_item)
        
        # Crear nuevo elemento con todos los datos del request (reemplazo completo)
        new_item = {
            'id': id,  # Mantener el ID original
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'is_active': data.get('is_active', True)
        }
        
        # Validar campos requeridos
        if not new_item['name'] or not new_item['email']:
            # Restaurar el elemento original si falla la validación
            data_list.append(existing_item)
            return Response({
                'error': 'Los campos name y email son requeridos.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Agregar el nuevo elemento
        data_list.append(new_item)
        
        return Response({
            'message': 'Elemento actualizado completamente.',
            'data': new_item
        }, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        """
        PATCH - Actualiza parcialmente los campos del elemento
        """
        data = request.data
        
        # Buscar el elemento existente
        existing_item = self._find_item_by_id(id)
        if not existing_item:
            return Response({
                'error': 'Elemento no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar solo los campos proporcionados
        updated_fields = []
        
        if 'name' in data:
            existing_item['name'] = data['name']
            updated_fields.append('name')
        
        if 'email' in data:
            existing_item['email'] = data['email']
            updated_fields.append('email')
        
        if 'is_active' in data:
            existing_item['is_active'] = data['is_active']
            updated_fields.append('is_active')
        
        # Validar que al menos un campo fue proporcionado
        if not updated_fields:
            return Response({
                'error': 'Debe proporcionar al menos un campo para actualizar.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que los campos obligatorios no estén vacíos
        if existing_item.get('name', '').strip() == '' or existing_item.get('email', '').strip() == '':
            return Response({
                'error': 'Los campos name y email no pueden estar vacíos.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': f'Elemento actualizado parcialmente. Campos modificados: {", ".join(updated_fields)}',
            'data': existing_item
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        """
        DELETE - Elimina lógicamente un elemento (marca como inactivo)
        """
        # Buscar el elemento existente
        existing_item = self._find_item_by_id(id)
        if not existing_item:
            return Response({
                'error': 'Elemento no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar si ya está eliminado lógicamente
        if not existing_item.get('is_active', True):
            return Response({
                'error': 'El elemento ya está eliminado.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Eliminación lógica: marcar como inactivo
        existing_item['is_active'] = False
        
        return Response({
            'message': 'Elemento eliminado exitosamente.',
            'data': existing_item
        }, status=status.HTTP_200_OK)