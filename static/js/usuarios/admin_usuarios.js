document.addEventListener("DOMContentLoaded", () => {
    cargarUsuarios();
});

const API_URL = "/api/usuarios";

// 1. REGISTRAR USUARIO (POST)
async function registrarUsuario() {
    const nombre = document.getElementById("nombre").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const rol = document.getElementById("rol").value;
    
    // Validaciones básicas
    if (!nombre || !username || !password || !rol) {
        mostrarMensaje("Todos los campos son obligatorios", "red");
        return;
    }

    const datos = {
        nombre: nombre,
        username: username,
        password: password,
        rol: rol
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
            mostrarMensaje("¡Usuario creado correctamente!", "green");
            limpiarFormulario();
            cargarUsuarios(); // Recargar la tabla
        } else {
            mostrarMensaje("Error: " + (resultado.message || "No se pudo guardar"), "red");
        }

    } catch (error) {
        console.error("Error:", error);
        mostrarMensaje("Error de conexión con el servidor", "red");
    }
}

// 2. LISTAR USUARIOS (GET)
async function cargarUsuarios() {
    try {
        const response = await fetch(API_URL);
        const resultado = await response.json();
        
        const tbody = document.querySelector("#tablaUsuarios tbody");
        tbody.innerHTML = ""; 

        if (response.ok && resultado.success) {
            const lista = resultado.usuarios || [];

            lista.forEach(u => {
                const tr = document.createElement("tr");
                
                // Asignar color de etiqueta según el rol
                let badgeClass = "badge-gray";
                if(u.rol === 'Admin') badgeClass = "badge-red"; // Asume que tienes estilos de badge
                if(u.rol === 'Cajero') badgeClass = "badge-green";
                if(u.rol === 'Auxiliar') badgeClass = "badge-blue";

                // Estilo simple inline para el badge si no existe en CSS
                const badgeStyle = `padding: 4px 8px; border-radius: 4px; background: #eee; font-size: 0.85em; font-weight: bold;`;

                tr.innerHTML = `
                    <td>${u.id}</td>
                    <td><strong>${u.nombre}</strong></td>
                    <td>${u.username}</td>
                    <td><span style="${badgeStyle}">${u.rol}</span></td>
                    <td>${u.activo ? '<span style="color:green">Activo</span>' : '<span style="color:red">Inactivo</span>'}</td>
                    <td>
                        <button class="btn-delete" onclick="eliminarUsuario(${u.id})">
                           <i class="fas fa-trash"></i> Eliminar
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error("Error cargando usuarios:", error);
    }
}

// 3. ELIMINAR USUARIO (DELETE)
async function eliminarUsuario(id) {
    if(!confirm("¿Estás seguro de eliminar este usuario?")) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });
        const resultado = await response.json();

        if (resultado.success) {
            cargarUsuarios();
            mostrarMensaje("Usuario eliminado", "green");
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
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    document.getElementById("rol").value = "";
}