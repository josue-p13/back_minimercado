"""
Controlador de Usuarios
Gestiona las peticiones relacionadas con usuarios (CRUD Admin)
"""
from app.services.usuario_service import UsuarioService

class UsuarioController:
    
    @staticmethod
    def listar_usuarios():
        try:
            usuarios = UsuarioService.listar_usuarios()
            return {'success': True, 'usuarios': usuarios}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def agregar_usuario(nombre, username, password, rol):
        try:
            usuario = UsuarioService.agregar_usuario(nombre, username, password, rol)
            return {
                'success': True, 
                'message': 'Usuario creado exitosamente',
                'usuario': usuario.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def actualizar_usuario(id, nombre, username, password, rol):
        try:
            usuario = UsuarioService.actualizar_usuario(id, nombre, username, password, rol)
            return {
                'success': True, 
                'message': 'Usuario actualizado exitosamente',
                'usuario': usuario.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def eliminar_usuario(id):
        try:
            UsuarioService.eliminar_usuario(id)
            return {'success': True, 'message': 'Usuario eliminado exitosamente'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
            
    @staticmethod
    def buscar_usuario(id):
        try:
            usuario = UsuarioService.buscar_usuario(id)
            if not usuario:
                return {'success': False, 'message': 'Usuario no encontrado'}
            return {'success': True, 'usuario': usuario}
        except Exception as e:
            return {'success': False, 'message': str(e)}