from app.services.auth_service import AuthService

class AuthController:

    @staticmethod
    def login(username, password):
        try:
            # Delegamos TODO el proceso al servicio (que ya sabe comparar contraseñas)
            return AuthService.login(username, password)
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def registrar_usuario(nombre, username, password, rol):
        try:
            return AuthService.registrar_usuario(nombre, username, password, rol)
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def validar_token(token):
        try:
            return AuthService.validar_token(token)
        except Exception as e:
            return {'success': False, 'message': str(e)}