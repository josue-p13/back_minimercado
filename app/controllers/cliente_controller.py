from app.services.cliente_service import ClienteService

class ClienteController:
    
    @staticmethod
    def agregar_cliente(nombre, telefono, email):
        try:
            cliente = ClienteService.agregar_cliente(nombre, telefono, email)
            return {
                'success': True,
                'message': 'Cliente registrado exitosamente',
                'cliente': cliente.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def listar_clientes():
        try:
            clientes = ClienteService.listar_clientes()
            return {'success': True, 'clientes': clientes}
        except Exception as e:
            return {'success': False, 'message': str(e)}
            
    @staticmethod
    def buscar_cliente(id):
        try:
            cliente = ClienteService.buscar_cliente(id)
            if not cliente:
                return {'success': False, 'message': 'Cliente no encontrado'}
            return {'success': True, 'cliente': cliente}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def actualizar_cliente(id, nombre, telefono, email):
        try:
            cliente = ClienteService.actualizar_cliente(id, nombre, telefono, email)
            return {
                'success': True,
                'message': 'Cliente actualizado exitosamente',
                'cliente': cliente.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def eliminar_cliente(id):
        try:
            ClienteService.eliminar_cliente(id)
            return {'success': True, 'message': 'Cliente eliminado exitosamente'}
        except Exception as e:
            return {'success': False, 'message': str(e)}