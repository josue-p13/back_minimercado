from app.database.connection import get_connection
from app.models.venta import Venta

class VentaRepository:
    
    @staticmethod
    def crear_venta(venta):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # 1. Insertar Cabecera de Venta
            cursor.execute('''
                INSERT INTO venta (fecha, total, fk_cliente, fk_usuario, fk_caja)
                VALUES (?, ?, ?, ?, ?)
            ''', (venta.fecha, venta.total, venta.fk_cliente, venta.fk_usuario, venta.fk_caja))
            
            venta_id = cursor.lastrowid
            venta.id = venta_id
            
            # 2. Insertar Detalles (Items)
            for item in venta.items:
                cursor.execute('''
                    INSERT INTO detalle_venta (fk_venta, fk_producto, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venta_id, item['producto_id'], item['cantidad'], item['precio'], item['subtotal']))
            
            conn.commit()
            return venta
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor()
        # Hacemos un JOIN para traer el nombre del cliente y del usuario
        query = '''
            SELECT v.id, v.fecha, v.total, c.nombre as cliente, u.username as usuario
            FROM venta v
            LEFT JOIN cliente c ON v.fk_cliente = c.id
            LEFT JOIN usuario u ON v.fk_usuario = u.id
            ORDER BY v.id DESC
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        # Retornamos diccionarios directamente para facilitar la vista
        return [
            {
                "id": r[0], "fecha": r[1], "total": r[2], 
                "cliente": r[3] if r[3] else "Consumidor Final", 
                "usuario": r[4]
            } 
            for r in rows
        ]

    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtener cabecera
        cursor.execute('SELECT * FROM venta WHERE id = ?', (id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
            
        venta_dict = {
            "id": row[0], "fecha": row[1], "total": row[2], 
            "fk_cliente": row[3], "fk_usuario": row[4], "fk_caja": row[5],
            "items": []
        }
        
        # Obtener detalles
        cursor.execute('''
            SELECT d.cantidad, d.precio_unitario, d.subtotal, p.nombre 
            FROM detalle_venta d
            JOIN producto p ON d.fk_producto = p.id
            WHERE d.fk_venta = ?
        ''', (id,))
        
        detalles = cursor.fetchall()
        conn.close()
        
        for d in detalles:
            venta_dict["items"].append({
                "cantidad": d[0], "precio": d[1], 
                "subtotal": d[2], "producto": d[3]
            })
            
        return venta_dict