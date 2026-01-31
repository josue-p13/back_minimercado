document.addEventListener("DOMContentLoaded", () => {
    cargarResumenProductos();
    cargarResumenProveedores();
});

// ==========================================
// 1. CARGAR PRODUCTOS
// ==========================================
async function cargarResumenProductos() {
    const tbody = document.getElementById("tabla-productos");
    
    try {
        const response = await fetch("/api/inventario/productos");
        const resultado = await response.json();

        // DEPURACIÓN: Ver qué llega realmente en la consola del navegador
        console.log("Respuesta API Productos:", resultado);

        if (response.ok && resultado.success) {
            // CORRECCIÓN AQUÍ:
            // Buscamos la lista en 'productos' (lo más probable), 'data' o 'products'
            const lista = resultado.productos || resultado.data || resultado.products || [];
            
            tbody.innerHTML = ""; // Limpiar "Cargando..."

            if (lista.length === 0) {
                tbody.innerHTML = "<tr><td colspan='3'>No hay productos registrados.</td></tr>";
                return;
            }

            // Mostramos solo los primeros 8
            const vistaPrevia = lista.slice(0, 8); 

            vistaPrevia.forEach(prod => {
                // Validación de seguridad para evitar errores si faltan campos
                const stock = prod.stock || 0;
                const stockMin = prod.stock_minimo || 0;
                const precio = prod.precio || 0;

                // Lógica visual: Si stock es menor o igual al mínimo, poner en rojo
                const claseStock = (stock <= stockMin) ? "low-stock" : "";
                
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${prod.nombre}</td>
                    <td>$${parseFloat(precio).toFixed(2)}</td>
                    <td class="${claseStock}">${stock}</td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            console.error("Error en respuesta lógica:", resultado);
            tbody.innerHTML = "<tr><td colspan='3'>Error al cargar datos.</td></tr>";
        }
    } catch (error) {
        console.error("Error productos:", error);
        tbody.innerHTML = "<tr><td colspan='3'>Error de conexión.</td></tr>";
    }
}

// ==========================================
// 2. CARGAR PROVEEDORES
// ==========================================
async function cargarResumenProveedores() {
    const tbody = document.getElementById("tabla-proveedores");

    try {
        const response = await fetch("/api/proveedores");
        const resultado = await response.json();

        if (response.ok && resultado.success) {
            // IMPORTANTE: Tu API de proveedores devuelve { proveedores: [...] } según vimos antes
            const lista = resultado.proveedores || resultado.data || [];

            tbody.innerHTML = "";

            if (lista.length === 0) {
                tbody.innerHTML = "<tr><td colspan='2'>No hay proveedores.</td></tr>";
                return;
            }

            // Mostramos los primeros 8
            const vistaPrevia = lista.slice(0, 8);

            vistaPrevia.forEach(prov => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${prov.nombre}</strong></td>
                    <td>${prov.telefono || '-'}</td>
                `;
                tbody.appendChild(tr);
            });

        } else {
            tbody.innerHTML = "<tr><td colspan='2'>Error al cargar datos.</td></tr>";
        }

    } catch (error) {
        console.error("Error proveedores:", error);
        tbody.innerHTML = "<tr><td colspan='2'>Error de conexión.</td></tr>";
    }
}