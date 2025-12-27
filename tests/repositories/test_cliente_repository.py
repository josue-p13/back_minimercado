"""
Pruebas unitarias para ClienteRepository
"""
import unittest
import sqlite3
from unittest.mock import patch

from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente


class TestClienteRepository(unittest.TestCase):

    def setUp(self):
        """Configura una base SQLite en memoria antes de cada test"""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE cliente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                activo INTEGER NOT NULL
            )
        """)
        self.conn.commit()

        self.cliente = Cliente(
            id=None,
            nombre='Cliente Test',
            telefono='0999999999',
            email='test@email.com',
            activo=1
        )

    def tearDown(self):
        self.conn.close()

    def _mock_get_connection(self):
        """Devuelve la conexión en memoria"""
        return self.conn

    @patch('app.repositories.cliente_repository.get_connection')
    def test_crear_cliente(self, mock_conn):
        """Test: crear cliente"""
        mock_conn.side_effect = self._mock_get_connection

        cliente_creado = ClienteRepository.crear(self.cliente)

        self.assertIsNotNone(cliente_creado.id)
        self.assertEqual(cliente_creado.nombre, 'Cliente Test')

    @patch('app.repositories.cliente_repository.get_connection')
    def test_obtener_cliente_por_id(self, mock_conn):
        """Test: obtener cliente por ID"""
        mock_conn.side_effect = self._mock_get_connection

        cliente = ClienteRepository.crear(self.cliente)
        encontrado = ClienteRepository.obtener_por_id(cliente.id)

        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, cliente.nombre)

    @patch('app.repositories.cliente_repository.get_connection')
    def test_obtener_cliente_no_existente(self, mock_conn):
        """Test: obtener cliente inexistente"""
        mock_conn.side_effect = self._mock_get_connection

        resultado = ClienteRepository.obtener_por_id(999)
        self.assertIsNone(resultado)

    @patch('app.repositories.cliente_repository.get_connection')
    def test_listar_clientes_activos(self, mock_conn):
        """Test: listar clientes activos"""
        mock_conn.side_effect = self._mock_get_connection

        ClienteRepository.crear(self.cliente)

        clientes = ClienteRepository.listar()

        self.assertEqual(len(clientes), 1)
        self.assertEqual(clientes[0].nombre, 'Cliente Test')

    @patch('app.repositories.cliente_repository.get_connection')
    def test_actualizar_cliente(self, mock_conn):
        """Test: actualizar cliente"""
        mock_conn.side_effect = self._mock_get_connection

        cliente = ClienteRepository.crear(self.cliente)
        cliente.nombre = 'Cliente Actualizado'

        ClienteRepository.actualizar(cliente)

        actualizado = ClienteRepository.obtener_por_id(cliente.id)
        self.assertEqual(actualizado.nombre, 'Cliente Actualizado')

    @patch('app.repositories.cliente_repository.get_connection')
    def test_eliminar_cliente(self, mock_conn):
        """Test: eliminar (desactivar) cliente"""
        mock_conn.side_effect = self._mock_get_connection

        cliente = ClienteRepository.crear(self.cliente)

        ClienteRepository.eliminar(cliente.id)

        clientes = ClienteRepository.listar()
        self.assertEqual(len(clientes), 0)


if __name__ == '__main__':
    unittest.main()
