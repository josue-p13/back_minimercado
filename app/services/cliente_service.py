"""
Servicio de Clientes
Gestiona la lógica de negocio para Clientes
"""
from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente


class ClienteService:

    @staticmethod
    def agregar_cliente(nombre, telefono=None, email=None):
        """Agrega un nuevo cliente"""
        if not nombre:
            raise Exception("El nombre del cliente es obligatorio")

        cliente = Cliente(
            nombre=nombre,
            telefono=telefono,
            email=email
        )
        return ClienteRepository.crear(cliente)

    @staticmethod
    def actualizar_cliente(id, nombre, telefono=None, email=None):
        """Actualiza la información de un cliente"""
        cliente = ClienteRepository.obtener_por_id(id)
        if not cliente:
            raise Exception("Cliente no encontrado")

        cliente.nombre = nombre
        cliente.telefono = telefono
        cliente.email = email

        ClienteRepository.actualizar(cliente)
        return cliente

    @staticmethod
    def eliminar_cliente(id):
        """Elimina (desactiva) un cliente"""
        cliente = ClienteRepository.obtener_por_id(id)
        if not cliente:
            raise Exception("Cliente no encontrado")

        ClienteRepository.eliminar(id)
        return True

    @staticmethod
    def listar_clientes():
        """Lista todos los clientes"""
        clientes = ClienteRepository.listar()
        return [c.to_dict() for c in clientes]

    @staticmethod
    def buscar_cliente(id):
        """Busca un cliente por ID"""
        cliente = ClienteRepository.obtener_por_id(id)
        if cliente:
            return cliente.to_dict()
        return None
