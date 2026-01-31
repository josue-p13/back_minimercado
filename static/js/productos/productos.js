// URL base de la API
const API_URL_PRODUCTOS = "/api/inventario/productos";
const API_URL_PROVEEDORES = "/api/proveedores";

// Cargar proveedores al iniciar la página
document.addEventListener("DOMContentLoaded", () => {
    cargarProveedores();
});

// static/js/productos/productos.js

async function cargarProveedores() {
    const select = document.getElementById("proveedor");
    // Limpiamos y dejamos la opción por defecto
    select.innerHTML = '<option value="">-- Seleccione un proveedor --</option>'; 
    
    try {
        const response = await fetch(API_URL_PROVEEDORES);
        const resultado = await response.json();

        if (response.ok && resultado.success) {
            // CORRECCIÓN AQUÍ: Usamos .proveedores en lugar de .data
            // Los logs dicen que el servidor devuelve { proveedores: [...] }
            const lista = resultado.proveedores || []; 

            lista.forEach(p => {
                const option = document.createElement("option");
                option.value = p.id; 
                option.textContent = p.nombre; 
                select.appendChild(option);
            });
        } else {
            console.error("Error al cargar proveedores:", resultado);
        }
    } catch (error) {
        console.error("Error de conexión:", error);
    }
}

// Función principal de registro
async function registrarProducto() {
    // Obtener valores
    const nombre = document.getElementById("nombre").value.trim();
    const precio = document.getElementById("precio").value;
    const stock = document.getElementById("stock").value;
    const stockMinimo = document.getElementById("stock_minimo").value;
    const proveedorId = document.getElementById("proveedor").value; // Puede estar vacío
    
    const mensaje = document.getElementById("mensaje");

    // 1. Validaciones
    if (!nombre || !precio || !stock || !stockMinimo) {
        mostrarMensaje("Todos los campos marcados con * son obligatorios", "error");
        return;
    }

    if (parseFloat(precio) < 0 || parseInt(stock) < 0 || parseInt(stockMinimo) < 0) {
        mostrarMensaje("Los valores numéricos no pueden ser negativos", "error");
        return;
    }

    // 2. Construir objeto JSON según el modelo 'ProductoCreate' de Pydantic
    const datosProducto = {
        nombre: nombre,
        precio: parseFloat(precio),       // Convertir a float
        stock: parseInt(stock),           // Convertir a int
        stock_minimo: parseInt(stockMinimo), // Convertir a int (IMPORTANTE)
        fk_proveedor: proveedorId ? parseInt(proveedorId) : null // Si hay valor, es int, sino null
    };

    try {
        const response = await fetch(API_URL_PRODUCTOS, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datosProducto)
        });

        const resultado = await response.json();

        if (response.ok && resultado.success) {
            mostrarMensaje("¡Producto registrado correctamente!", "success");
            limpiarFormulario();
        } else {
            // Mostrar error del backend o de validación
            const errorMsg = resultado.detail || resultado.message || "Error desconocido";
            mostrarMensaje("Error: " + errorMsg, "error");
        }

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión con el servidor", "error");
    }
}

// Utilidades
function mostrarMensaje(texto, tipo) {
    const msgDiv = document.getElementById("mensaje");
    if (tipo === "success") {
        msgDiv.style.color = "#2E7D32"; // Verde
    } else {
        msgDiv.style.color = "#D64545"; // Rojo
    }
    msgDiv.innerText = texto;
}

function limpiarFormulario() {
    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("stock").value = "";
    document.getElementById("stock_minimo").value = "";
    document.getElementById("proveedor").value = ""; // Resetear select
}