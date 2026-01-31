document.addEventListener("DOMContentLoaded", () => {
    cargarProveedores();
});

// URL base de tu API
const API_URL = "/api/proveedores";

// 1. REGISTRAR PROVEEDOR (POST)
async function registrarProveedor() {
    const nombre = document.getElementById("nombre").value;
    const telefono = document.getElementById("telefono").value;
    const direccion = document.getElementById("direccion").value;
    const mensaje = document.getElementById("mensaje");

    if (!nombre) {
        mostrarMensaje("El nombre es obligatorio", "red");
        return;
    }

    const datos = {
        nombre: nombre,
        telefono: telefono,
        direccion: direccion
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();

        if (response.ok && resultado.success) {
            mostrarMensaje("¡Proveedor registrado correctamente!", "green");
            limpiarFormulario();
            cargarProveedores(); // Recargar la tabla
        } else {
            mostrarMensaje("Error: " + (resultado.message || "No se pudo guardar"), "red");
        }

    } catch (error) {
        console.error("Error:", error);
        mostrarMensaje("Error de conexión con el servidor", "red");
    }
}



async function cargarProveedores() {
    try {
        const response = await fetch(API_URL);
        const resultado = await response.json();
        console.log(">>> LISTA RECIBIDA:", resultado);

        const tbody = document.querySelector("#tablaProveedores tbody");
        tbody.innerHTML = ""; 

        if (response.ok && resultado.success) {
            // CORRECCIÓN AQUÍ: Usamos .proveedores
            // Si resultado.proveedores no existe, usamos un array vacío [] para evitar errores
            const lista = resultado.proveedores || [];

            lista.forEach(p => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${p.id}</td>
                    <td><strong>${p.nombre}</strong></td>
                    <td>${p.telefono || '-'}</td>
                    <td>${p.direccion || '-'}</td>
                    <td>
                        <button class="btn-delete" onclick="eliminarProveedor(${p.id})">
                           <i class="fas fa-trash"></i> Eliminar
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error("Error cargando proveedores:", error);
    }
}

// 3. ELIMINAR PROVEEDOR (DELETE)
async function eliminarProveedor(id) {
    if(!confirm("¿Estás seguro de eliminar este proveedor?")) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });
        const resultado = await response.json();

        if (resultado.success) {
            cargarProveedores();
        } else {
            alert("Error al eliminar: " + resultado.message);
        }
    } catch (error) {
        alert("Error de conexión");
    }
}

// UTILIDADES
function mostrarMensaje(texto, color) {
    const msgDiv = document.getElementById("mensaje");
    msgDiv.style.color = color === "green" ? "#2E7D32" : "#D32F2F";
    msgDiv.textContent = texto;
    setTimeout(() => { msgDiv.textContent = ""; }, 3000);
}

function limpiarFormulario() {
    document.getElementById("nombre").value = "";
    document.getElementById("telefono").value = "";
    document.getElementById("direccion").value = "";
}