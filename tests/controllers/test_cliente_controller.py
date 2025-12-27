"""
Pruebas unitarias para ClienteController
"""
import unittest
from unittest.mock import Mock, patch
from app.controllers.cliente_controller import ClienteController


class TestClienteController(unittest.TestCase):
    """Suite de pruebas para ClienteController"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.cliente_data = {
            'id': 1,
            'nombre': 'Cliente Test',
            'telefono': '0999999999',
            'email': 'cliente@test.com',
            'activo': 1
        }

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_agregar_cliente_exito(self, mock_service):
        """Test: Agregar cliente exitosamente"""
        # Arrange
        mock_cliente_obj = Mock()
        mock_cliente_obj.to_dict.return_value = self.cliente_data
        mock_service.agregar_cliente.return_value = mock_cliente_obj

        # Act
        resultado = ClienteController.agregar_cliente(
            'Cliente Test',
            '0999999999',
            'cliente@test.com'
        )

        # Assert
        mock_service.agregar_cliente.assert_called_once_with(
            'Cliente Test',
            '0999999999',
            'cliente@test.com'
        )
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Cliente agregado exitosamente')
        self.assertEqual(resultado['cliente'], self.cliente_data)

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_agregar_cliente_error(self, mock_service):
        """Test: Error al agregar cliente"""
        # Arrange
        mock_service.agregar_cliente.side_effect = Exception("Error de validación")

        # Act
        resultado = ClienteController.agregar_cliente('', None, None)

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Error de validación")

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_actualizar_cliente_exito(self, mock_service):
        """Test: Actualizar cliente exitosamente"""
        # Arrange
        mock_cliente_obj = Mock()
        mock_cliente_obj.to_dict.return_value = self.cliente_data
        mock_service.actualizar_cliente.return_value = mock_cliente_obj

        # Act
        resultado = ClienteController.actualizar_cliente(
            1,
            'Nuevo Nombre',
            '0888888888',
            'nuevo@test.com'
        )

        # Assert
        mock_service.actualizar_cliente.assert_called_once_with(
            1,
            'Nuevo Nombre',
            '0888888888',
            'nuevo@test.com'
        )
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Cliente actualizado exitosamente')
        self.assertEqual(resultado['cliente'], self.cliente_data)

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_actualizar_cliente_error(self, mock_service):
        """Test: Error al actualizar cliente"""
        # Arrange
        mock_service.actualizar_cliente.side_effect = Exception("Cliente no encontrado")

        # Act
        resultado = ClienteController.actualizar_cliente(
            999,
            'A',
            'B',
            'C'
        )

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Cliente no encontrado")

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_eliminar_cliente_exito(self, mock_service):
        """Test: Eliminar cliente exitosamente"""
        # Arrange
        mock_service.eliminar_cliente.return_value = True

        # Act
        resultado = ClienteController.eliminar_cliente(1)

        # Assert
        mock_service.eliminar_cliente.assert_called_once_with(1)
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Cliente eliminado exitosamente')

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_eliminar_cliente_error(self, mock_service):
        """Test: Error al eliminar cliente"""
        # Arrange
        mock_service.eliminar_cliente.side_effect = Exception("No se pudo eliminar")

        # Act
        resultado = ClienteController.eliminar_cliente(1)

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "No se pudo eliminar")

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_listar_clientes_exito(self, mock_service):
        """Test: Listar clientes exitosamente"""
        # Arrange
        mock_service.listar_clientes.return_value = [self.cliente_data]

        # Act
        resultado = ClienteController.listar_clientes()

        # Assert
        mock_service.listar_clientes.assert_called_once()
        self.assertTrue(resultado['success'])
        self.assertEqual(len(resultado['clientes']), 1)

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_listar_clientes_error(self, mock_service):
        """Test: Error al listar clientes"""
        # Arrange
        mock_service.listar_clientes.side_effect = Exception("Error DB")

        # Act
        resultado = ClienteController.listar_clientes()

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Error DB")

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_buscar_cliente_exito(self, mock_service):
        """Test: Buscar cliente existente"""
        # Arrange
        mock_service.buscar_cliente.return_value = self.cliente_data

        # Act
        resultado = ClienteController.buscar_cliente(1)

        # Assert
        mock_service.buscar_cliente.assert_called_once_with(1)
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['cliente'], self.cliente_data)

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_buscar_cliente_no_encontrado(self, mock_service):
        """Test: Buscar cliente que no existe"""
        # Arrange
        mock_service.buscar_cliente.return_value = None

        # Act
        resultado = ClienteController.buscar_cliente(999)

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Cliente no encontrado')

    @patch('app.controllers.cliente_controller.ClienteService')
    def test_buscar_cliente_error(self, mock_service):
        """Test: Error inesperado al buscar cliente"""
        # Arrange
        mock_service.buscar_cliente.side_effect = Exception("Error fatal")

        # Act
        resultado = ClienteController.buscar_cliente(1)

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Error fatal")


if __name__ == '__main__':
    unittest.main()
