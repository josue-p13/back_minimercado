const API_URL = "/api/usuarios";
let editando = false;

document.addEventListener("DOMContentLoaded", () => {
    cargarUsuarios();
});

// 1. CARGAR
async function cargarUsuarios() {
    try {
        const response = await fetch(API_URL);
        const resultado = await response.json();
        const tbody = document.querySelector("#tablaUsuarios tbody");
        tbody.innerHTML = "";

        if (response.ok && resultado.success) {
            const lista = resultado.usuarios || [];
            if (lista.length === 0) {
                tbody.innerHTML = "<tr><td colspan='5'>No hay usuarios.</td></tr>";
                return;
            }

            lista.forEach(u => {
                let badgeClass = u.activo ? "color:green" : "color:red";

                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${u.nombre}</strong></td>
                    <td>${u.username}</td>
                    <td>${u.rol}</td>
                    <td><span style="${badgeClass}">${u.activo ? 'Activo' : 'Inactivo'}</span></td>
                    <td>
                        <button class="btn-edit" onclick='cargarDatosEdicion(${JSON.stringify(u)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-delete" onclick="eliminarUsuario(${u.id})">
                           <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) { console.error(error); }
}

// 2. GUARDAR
async function guardarUsuario() {
    const id = document.getElementById("usuario_id").value;
    const nombre = document.getElementById("nombre").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const rol = document.getElementById("rol").value;

    // Validaciones
    if (!nombre || !username || !rol) {
        mostrarMensaje("Nombre, usuario y rol son obligatorios", "red");
        return;
    }

    // Si NO estamos editando, la contraseña es obligatoria
    if (!editando && !password) {
        mostrarMensaje("La contraseña es obligatoria para nuevos usuarios", "red");
        return;
    }

    const datos = { nombre, username, rol };

    // Solo enviamos password si el usuario escribió algo (o si es nuevo)
    if (password) {
        datos.password = password;
    } else if (editando) {
        datos.password = null; // Backend ignora si es null en update
    }

    const metodo = editando ? "PUT" : "POST";
    const url = editando ? `${API_URL}/${id}` : API_URL;

    try {
        const response = await fetch(url, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();

        if (response.ok && resultado.success) {
            mostrarMensaje(editando ? "Usuario actualizado" : "Usuario creado", "green");
            limpiarFormulario();
            cargarUsuarios();
        } else {
            mostrarMensaje("Error: " + (resultado.message || resultado.detail), "red");
        }

    } catch (error) {
        mostrarMensaje("Error de conexión", "red");
    }
}

// 3. EDITAR
function cargarDatosEdicion(usuario) {
    editando = true;
    document.getElementById("usuario_id").value = usuario.id;
    document.getElementById("nombre").value = usuario.nombre;
    document.getElementById("username").value = usuario.username;
    document.getElementById("rol").value = usuario.rol;

    // Contraseña se limpia para no mostrar el hash
    document.getElementById("password").value = "";
    document.getElementById("pass-help").style.display = "block"; // Mostrar ayuda

    document.getElementById("form-title").textContent = "Editar Usuario";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-sync"></i> Actualizar';
    document.getElementById("btn-cancelar").style.display = "inline-block";
}

function limpiarFormulario() {
    editando = false;
    document.getElementById("usuario_id").value = "";
    document.getElementById("nombre").value = "";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    document.getElementById("rol").value = "";

    document.getElementById("pass-help").style.display = "none"; // Ocultar ayuda

    document.getElementById("form-title").textContent = "Registrar Usuario";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-user-plus"></i> Guardar';
    document.getElementById("btn-cancelar").style.display = "none";
}

// 4. ELIMINAR
async function eliminarUsuario(id) {
    if (!confirm("¿Eliminar este usuario?")) return;
    try {
        const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        const resultado = await response.json();
        if (resultado.success) {
            cargarUsuarios();
            mostrarMensaje("Usuario eliminado", "green");
        } else { alert(resultado.message); }
    } catch (error) { alert("Error de conexión"); }
}

function mostrarMensaje(texto, color) {
    const msg = document.getElementById("mensaje");
    msg.style.color = color === "green" ? "#2E7D32" : "#D32F2F";
    msg.textContent = texto;
    setTimeout(() => { msg.textContent = ""; }, 3000);
}