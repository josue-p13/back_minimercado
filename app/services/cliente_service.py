from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente

class ClienteService:
    
    @staticmethod
    def agregar_cliente(nombre, telefono, email):
        # Aquí podrías validar si el email ya existe, etc.
        nuevo_cliente = Cliente(nombre=nombre, telefono=telefono, email=email)
        return ClienteRepository.crear(nuevo_cliente)
    
    @staticmethod
    def listar_clientes():
        clientes = ClienteRepository.listar()
        return [c.to_dict() for c in clientes]
    
    @staticmethod
    def buscar_cliente(id):
        cliente = ClienteRepository.obtener_por_id(id)
        return cliente.to_dict() if cliente else None
    
    @staticmethod
    def actualizar_cliente(id, nombre, telefono, email):
        cliente_actual = ClienteRepository.obtener_por_id(id)
        if not cliente_actual:
            raise Exception("Cliente no encontrado")
            
        cliente_actual.nombre = nombre
        cliente_actual.telefono = telefono
        cliente_actual.email = email
        
        ClienteRepository.actualizar(cliente_actual)
        return cliente_actual
    
    @staticmethod
    def eliminar_cliente(id):
        if not ClienteRepository.obtener_por_id(id):
            raise Exception("Cliente no encontrado")
        ClienteRepository.eliminar(id)