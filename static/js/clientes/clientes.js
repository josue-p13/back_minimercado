const API_URL = "/api/clientes";
let editando = false;

document.addEventListener("DOMContentLoaded", () => {
    cargarClientes();
});

// 1. CARGAR
async function cargarClientes() {
    try {
        const response = await fetch(API_URL);
        const resultado = await response.json();
        const tbody = document.querySelector("#tablaClientes tbody");
        tbody.innerHTML = "";

        if (response.ok && resultado.success) {
            const lista = resultado.clientes || [];
            if (lista.length === 0) {
                tbody.innerHTML = "<tr><td colspan='4'>No hay clientes registrados.</td></tr>";
                return;
            }

            lista.forEach(c => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${c.nombre}</strong></td>
                    <td>${c.telefono || '-'}</td>
                    <td>${c.email || '-'}</td>
                    <td>
                        <button class="btn-edit" onclick='cargarDatosEdicion(${JSON.stringify(c)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-delete" onclick="eliminarCliente(${c.id})">
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
async function guardarCliente() {
    const id = document.getElementById("cliente_id").value;
    const nombre = document.getElementById("nombre").value;
    const telefono = document.getElementById("telefono").value;
    const email = document.getElementById("email").value;

    if (!nombre) {
        mostrarMensaje("El nombre es obligatorio", "red");
        return;
    }

    const datos = { nombre, telefono, email };
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
            mostrarMensaje(editando ? "Cliente actualizado" : "Cliente registrado", "green");
            limpiarFormulario();
            cargarClientes();
        } else {
            mostrarMensaje("Error: " + resultado.message, "red");
        }
    } catch (error) {
        mostrarMensaje("Error de conexión", "red");
    }
}

// 3. EDITAR
function cargarDatosEdicion(cliente) {
    editando = true;
    document.getElementById("cliente_id").value = cliente.id;
    document.getElementById("nombre").value = cliente.nombre;
    document.getElementById("telefono").value = cliente.telefono;
    document.getElementById("email").value = cliente.email;

    document.getElementById("form-title").textContent = "Editar Cliente";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-sync"></i> Actualizar';
    document.getElementById("btn-cancelar").style.display = "inline-block";
}

function limpiarFormulario() {
    editando = false;
    document.getElementById("cliente_id").value = "";
    document.getElementById("nombre").value = "";
    document.getElementById("telefono").value = "";
    document.getElementById("email").value = "";

    document.getElementById("form-title").textContent = "Registrar Cliente";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-save"></i> Guardar';
    document.getElementById("btn-cancelar").style.display = "none";
}

// 4. ELIMINAR
async function eliminarCliente(id) {
    if (!confirm("¿Eliminar este cliente?")) return;
    try {
        const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        const resultado = await response.json();
        if (resultado.success) {
            cargarClientes();
            mostrarMensaje("Cliente eliminado", "green");
        } else { alert(resultado.message); }
    } catch (error) { alert("Error de conexión"); }
}

function mostrarMensaje(texto, color) {
    const msg = document.getElementById("mensaje");
    msg.style.color = color === "green" ? "#2E7D32" : "#D32F2F";
    msg.textContent = texto;
    setTimeout(() => { msg.textContent = ""; }, 3000);
}