import unittest
import sqlite3
import tempfile
import os
from unittest.mock import patch

from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente


class TestClienteRepository(unittest.TestCase):

    def setUp(self):
        # Archivo temporal SQLite
        self.db_fd, self.db_path = tempfile.mkstemp()

        # Crear esquema
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE cliente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                telefono TEXT,
                email TEXT,
                activo INTEGER
            )
        """)
        conn.commit()
        conn.close()

        self.cliente = Cliente(
            nombre="Cliente Test",
            telefono="0999999999",
            email="test@email.com",
            activo=1
        )

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _mock_get_connection(self):
        """Cada llamada devuelve una conexión nueva"""
        return sqlite3.connect(self.db_path)

    @patch('app.repositories.cliente_repository.get_connection')
    def test_crear_cliente(self, mock_conn):
        mock_conn.side_effect = self._mock_get_connection

        cliente = ClienteRepository.crear(self.cliente)
        self.assertIsNotNone(cliente.id)

    @patch('app.repositories.cliente_repository.get_connection')
    def test_obtener_cliente_por_id(self, mock_conn):
        mock_conn.side_effect = self._mock_get_connection

        creado = ClienteRepository.crear(self.cliente)
        encontrado = ClienteRepository.obtener_por_id(creado.id)

        self.assertIsNotNone(encontrado)

    @patch('app.repositories.cliente_repository.get_connection')
    def test_listar_clientes_activos(self, mock_conn):
        mock_conn.side_effect = self._mock_get_connection

        ClienteRepository.crear(self.cliente)
        clientes = ClienteRepository.listar()

        self.assertEqual(len(clientes), 1)

    @patch('app.repositories.cliente_repository.get_connection')
    def test_actualizar_cliente(self, mock_conn):
        mock_conn.side_effect = self._mock_get_connection

        cliente = ClienteRepository.crear(self.cliente)
        cliente.nombre = "Actualizado"

        ClienteRepository.actualizar(cliente)
        actualizado = ClienteRepository.obtener_por_id(cliente.id)

        self.assertEqual(actualizado.nombre, "Actualizado")

    @patch('app.repositories.cliente_repository.get_connection')
    def test_eliminar_cliente(self, mock_conn):
        mock_conn.side_effect = self._mock_get_connection

        cliente = ClienteRepository.crear(self.cliente)
        ClienteRepository.eliminar(cliente.id)

        eliminado = ClienteRepository.obtener_por_id(cliente.id)
        self.assertEqual(eliminado.activo, 0)


    @patch('app.repositories.cliente_repository.get_connection')
    def test_obtener_cliente_no_existe(self, mock_conn):
        mock_conn.side_effect = self._mock_get_connection

        cliente = ClienteRepository.obtener_por_id(999)

        self.assertIsNone(cliente)

