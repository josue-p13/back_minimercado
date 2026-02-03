const API_URL_PRODUCTOS = "/api/inventario/productos";
const API_URL_PROVEEDORES = "/api/proveedores";

// Variables de estado
let editando = false;
let proveedoresMap = {}; // Diccionario ID -> Nombre

document.addEventListener("DOMContentLoaded", async () => {
    // Esperamos a cargar proveedores antes de cargar productos para tener los nombres listos
    await cargarProveedores();
    cargarProductos();
});

// ==========================================
// 1. CARGA DE DATOS (TABLA Y SELECT)
// ==========================================

async function cargarProveedores() {
    const select = document.getElementById("proveedor");
    select.innerHTML = '<option value="">-- Seleccione --</option>';

    try {
        const response = await fetch(API_URL_PROVEEDORES);
        const resultado = await response.json();

        if (response.ok && resultado.success) {
            const lista = resultado.proveedores || [];

            lista.forEach(p => {
                // 1. Llenar Select
                const option = document.createElement("option");
                option.value = p.id;
                option.textContent = p.nombre;
                select.appendChild(option);

                // 2. Guardar en mapa para la tabla
                proveedoresMap[p.id] = p.nombre;
            });
        }
    } catch (error) {
        console.error("Error al cargar proveedores:", error);
    }
}

async function cargarProductos() {
    const tbody = document.querySelector("#tablaProductos tbody");
    tbody.innerHTML = "<tr><td colspan='7'>Cargando...</td></tr>"; // colspan 7 por la nueva columna

    try {
        const response = await fetch(API_URL_PRODUCTOS);
        const resultado = await response.json();

        if (response.ok && resultado.success) {
            const lista = resultado.productos || [];
            tbody.innerHTML = "";

            if (lista.length === 0) {
                tbody.innerHTML = "<tr><td colspan='7'>No hay productos registrados.</td></tr>";
                return;
            }

            lista.forEach(p => {
                // Alerta visual de stock bajo
                const alertaClass = (p.stock <= p.stock_minimo) ? "color: #D32F2F; font-weight: bold;" : "";
                // Obtener nombre del proveedor o guión
                const nombreProveedor = proveedoresMap[p.fk_proveedor] || "-";

                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><small style="font-family: monospace; font-size: 1.1em;">${p.codigo_barras || '-'}</small></td>
                    <td><strong>${p.nombre}</strong></td>
                    <td>$${p.precio.toFixed(2)}</td>
                    <td style="${alertaClass}">${p.stock}</td>
                    <td>${p.stock_minimo}</td>
                    <td style="color: #555;">${nombreProveedor}</td>
                    <td>
                        <button class="btn-edit" onclick='cargarDatosEdicion(${JSON.stringify(p)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-delete" onclick="eliminarProducto(${p.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        tbody.innerHTML = "<tr><td colspan='7'>Error de conexión</td></tr>";
    }
}

// ==========================================
// 2. CREAR Y EDITAR (GUARDAR)
// ==========================================

async function guardarProducto() {
    const id = document.getElementById("producto_id").value;
    const codigoBarras = document.getElementById("codigo_barras").value.trim(); // NUEVO
    const nombre = document.getElementById("nombre").value.trim();
    const precio = document.getElementById("precio").value;
    const stock = document.getElementById("stock").value;
    const stockMinimo = document.getElementById("stock_minimo").value;
    const proveedorId = document.getElementById("proveedor").value;

    // Validaciones
    if (!nombre || !precio || !stock || !stockMinimo) {
        mostrarMensaje("Complete los campos obligatorios (*)", "red");
        return;
    }

    if (parseFloat(precio) < 0 || parseInt(stock) < 0 || parseInt(stockMinimo) < 0) {
        mostrarMensaje("Los valores no pueden ser negativos", "red");
        return;
    }

    // Objeto a enviar (incluye el código de barras)
    const datos = {
        nombre: nombre,
        precio: parseFloat(precio),
        stock: parseInt(stock),
        stock_minimo: parseInt(stockMinimo),
        fk_proveedor: proveedorId ? parseInt(proveedorId) : null,
        codigo_barras: codigoBarras // Enviamos el código (vacío o con datos)
    };

    const metodo = editando ? "PUT" : "POST";
    const url = editando ? `${API_URL_PRODUCTOS}/${id}` : API_URL_PRODUCTOS;

    try {
        const response = await fetch(url, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();

        if (response.ok && resultado.success) {
            mostrarMensaje(editando ? "Producto actualizado" : "Producto registrado", "green");
            limpiarFormulario();
            cargarProductos();
        } else {
            mostrarMensaje("Error: " + (resultado.message || resultado.detail), "red");
        }
    } catch (error) {
        mostrarMensaje("Error de conexión con el servidor", "red");
    }
}

// ==========================================
// 3. FUNCIONES DE EDICIÓN Y LIMPIEZA
// ==========================================

function cargarDatosEdicion(producto) {
    editando = true;
    document.getElementById("producto_id").value = producto.id;
    document.getElementById("codigo_barras").value = producto.codigo_barras || ""; // Cargar código
    document.getElementById("nombre").value = producto.nombre;
    document.getElementById("precio").value = producto.precio;
    document.getElementById("stock").value = producto.stock;
    document.getElementById("stock_minimo").value = producto.stock_minimo;
    document.getElementById("proveedor").value = producto.fk_proveedor || "";

    // Cambiar UI
    document.getElementById("form-title").textContent = "Editar Producto";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-sync"></i> Actualizar';
    document.getElementById("btn-cancelar").style.display = "inline-block";
}

function limpiarFormulario() {
    editando = false;
    document.getElementById("producto_id").value = "";
    document.getElementById("codigo_barras").value = ""; // Limpiar código
    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("stock").value = "";
    document.getElementById("stock_minimo").value = "";
    document.getElementById("proveedor").value = "";

    // Resetear UI
    document.getElementById("form-title").textContent = "Registrar Producto";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-save"></i> Guardar';
    document.getElementById("btn-cancelar").style.display = "none";
    document.getElementById("mensaje").textContent = "";
}

// ==========================================
// 4. ELIMINAR
// ==========================================

async function eliminarProducto(id) {
    if (!confirm("¿Estás seguro de eliminar este producto?")) return;

    try {
        const response = await fetch(`${API_URL_PRODUCTOS}/${id}`, {
            method: "DELETE"
        });
        const resultado = await response.json();

        if (resultado.success) {
            mostrarMensaje("Producto eliminado", "green");
            cargarProductos();
        } else {
            alert("Error: " + (resultado.message || "No se pudo eliminar"));
        }
    } catch (error) {
        alert("Error de conexión");
    }
}

// ==========================================
// 5. UTILIDADES
// ==========================================

function mostrarMensaje(texto, color) {
    const msg = document.getElementById("mensaje");
    msg.style.color = color === "green" ? "#2E7D32" : "#D32F2F";
    msg.textContent = texto;
    setTimeout(() => { msg.textContent = ""; }, 3000);
}