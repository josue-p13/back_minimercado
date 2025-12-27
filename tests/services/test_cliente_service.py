"""
Pruebas unitarias para ClienteService
"""
import unittest
from unittest.mock import patch, Mock

from app.services.cliente_service import ClienteService
from app.models.cliente import Cliente


class TestClienteService(unittest.TestCase):

    def setUp(self):
        """Datos base para pruebas"""
        self.cliente = Cliente(
            id=1,
            nombre='Cliente Test',
            telefono='0999999999',
            email='test@email.com',
            activo=1
        )

    @patch('app.services.cliente_service.ClienteRepository')
    def test_agregar_cliente_exito(self, mock_repo):
        """Test: agregar cliente exitosamente"""
        mock_repo.crear.return_value = self.cliente

        resultado = ClienteService.agregar_cliente(
            'Cliente Test',
            '0999999999',
            'test@email.com'
        )

        mock_repo.crear.assert_called_once()
        self.assertEqual(resultado.nombre, 'Cliente Test')

    @patch('app.services.cliente_service.ClienteRepository')
    def test_agregar_cliente_sin_nombre(self, mock_repo):
        """Test: error al agregar cliente sin nombre"""
        with self.assertRaises(Exception) as context:
            ClienteService.agregar_cliente('', '099', 'a@a.com')

        self.assertEqual(str(context.exception), "El nombre del cliente es obligatorio")
        mock_repo.crear.assert_not_called()

    @patch('app.services.cliente_service.ClienteRepository')
    def test_actualizar_cliente_exito(self, mock_repo):
        """Test: actualizar cliente exitosamente"""
        mock_repo.obtener_por_id.return_value = self.cliente

        resultado = ClienteService.actualizar_cliente(
            1,
            'Cliente Actualizado',
            '0888888888',
            'nuevo@email.com'
        )

        mock_repo.obtener_por_id.assert_called_once_with(1)
        mock_repo.actualizar.assert_called_once()
        self.assertEqual(resultado.nombre, 'Cliente Actualizado')

    @patch('app.services.cliente_service.ClienteRepository')
    def test_actualizar_cliente_no_encontrado(self, mock_repo):
        """Test: actualizar cliente inexistente"""
        mock_repo.obtener_por_id.return_value = None

        with self.assertRaises(Exception) as context:
            ClienteService.actualizar_cliente(999, 'X')

        self.assertEqual(str(context.exception), "Cliente no encontrado")

    @patch('app.services.cliente_service.ClienteRepository')
    def test_eliminar_cliente_exito(self, mock_repo):
        """Test: eliminar cliente exitosamente"""
        mock_repo.obtener_por_id.return_value = self.cliente

        resultado = ClienteService.eliminar_cliente(1)

        mock_repo.obtener_por_id.assert_called_once_with(1)
        mock_repo.eliminar.assert_called_once_with(1)
        self.assertTrue(resultado)

    @patch('app.services.cliente_service.ClienteRepository')
    def test_eliminar_cliente_no_encontrado(self, mock_repo):
        """Test: eliminar cliente inexistente"""
        mock_repo.obtener_por_id.return_value = None

        with self.assertRaises(Exception) as context:
            ClienteService.eliminar_cliente(999)

        self.assertEqual(str(context.exception), "Cliente no encontrado")

    @patch('app.services.cliente_service.ClienteRepository')
    def test_listar_clientes(self, mock_repo):
        """Test: listar clientes"""
        mock_repo.listar.return_value = [self.cliente]

        resultado = ClienteService.listar_clientes()

        mock_repo.listar.assert_called_once()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['nombre'], 'Cliente Test')

    @patch('app.services.cliente_service.ClienteRepository')
    def test_buscar_cliente_exito(self, mock_repo):
        """Test: buscar cliente existente"""
        mock_repo.obtener_por_id.return_value = self.cliente

        resultado = ClienteService.buscar_cliente(1)

        mock_repo.obtener_por_id.assert_called_once_with(1)
        self.assertEqual(resultado['nombre'], 'Cliente Test')

    @patch('app.services.cliente_service.ClienteRepository')
    def test_buscar_cliente_no_encontrado(self, mock_repo):
        """Test: buscar cliente inexistente"""
        mock_repo.obtener_por_id.return_value = None

        resultado = ClienteService.buscar_cliente(999)

        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
