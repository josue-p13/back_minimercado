"""
Servicio de Proveedores
Gestiona la lógica de negocio para Proveedores
"""
from app.repositories.proveedor_repository import ProveedorRepository
from app.models.proveedor import Proveedor

class ProveedorService:
    
    @staticmethod
    def agregar_proveedor(nombre, telefono, direccion):
        """Agrega un nuevo proveedor"""
        if not nombre:
            raise Exception("El nombre del proveedor es obligatorio")
        
        proveedor = Proveedor(
            nombre=nombre,
            telefono=telefono,
            direccion=direccion
        )
        return ProveedorRepository.crear(proveedor)
    
    @staticmethod
    def actualizar_proveedor(id, nombre, telefono, direccion):
        """Actualiza la información de un proveedor"""
        proveedor = ProveedorRepository.obtener_por_id(id)
        if not proveedor:
            raise Exception("Proveedor no encontrado")
        
        proveedor.nombre = nombre
        proveedor.telefono = telefono
        proveedor.direccion = direccion
        ProveedorRepository.actualizar(proveedor)
        return proveedor
    
    @staticmethod
    def eliminar_proveedor(id):
        """Elimina (desactiva) un proveedor"""
        proveedor = ProveedorRepository.obtener_por_id(id)
        if not proveedor:
            raise Exception("Proveedor no encontrado")
            
        ProveedorRepository.eliminar(id)
        return True

    @staticmethod
    def listar_proveedores():
        """Lista todos los proveedores"""
        proveedores = ProveedorRepository.listar()
        return [p.to_dict() for p in proveedores]
    
    @staticmethod
    def buscar_proveedor(id):
        """Busca un proveedor por ID"""
        proveedor = ProveedorRepository.obtener_por_id(id)
        if proveedor:
            return proveedor.to_dict()
        return None