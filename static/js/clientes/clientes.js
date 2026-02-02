document.addEventListener("DOMContentLoaded", () => {
    cargarClientes();
});

const API_URL = "/api/clientes";

// 1. REGISTRAR CLIENTE
async function registrarCliente() {
    const nombre = document.getElementById("nombre").value;
    const telefono = document.getElementById("telefono").value;
    const email = document.getElementById("email").value;

    if (!nombre) {
        mostrarMensaje("El nombre es obligatorio", "red");
        return;
    }

    const datos = { nombre, telefono, email };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();

        if (response.ok && resultado.success) {
            mostrarMensaje("Cliente registrado", "green");
            limpiarFormulario();
            cargarClientes();
        } else {
            mostrarMensaje("Error: " + resultado.message, "red");
        }
    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión", "red");
    }
}

// 2. LISTAR CLIENTES
async function cargarClientes() {
    try {
        const response = await fetch(API_URL);
        const resultado = await response.json();
        const tbody = document.querySelector("#tablaClientes tbody");
        tbody.innerHTML = "";

        if (response.ok && resultado.success) {
            const lista = resultado.clientes || [];
            lista.forEach(c => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${c.id}</td>
                    <td><strong>${c.nombre}</strong></td>
                    <td>${c.telefono || '-'}</td>
                    <td>${c.email || '-'}</td>
                    <td>
                        <button class="btn-delete" onclick="eliminarCliente(${c.id})">
                           <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error("Error cargando clientes:", error);
    }
}

// 3. ELIMINAR CLIENTE
async function eliminarCliente(id) {
    if (!confirm("¿Eliminar este cliente?")) return;
    try {
        const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        const resultado = await response.json();
        if (resultado.success) cargarClientes();
        else alert(resultado.message);
    } catch (error) {
        alert("Error de conexión");
    }
}

function mostrarMensaje(texto, color) {
    const msgDiv = document.getElementById("mensaje");
    msgDiv.style.color = color === "green" ? "#2E7D32" : "#D32F2F";
    msgDiv.textContent = texto;
    setTimeout(() => { msgDiv.textContent = ""; }, 3000);
}

function limpiarFormulario() {
    document.getElementById("nombre").value = "";
    document.getElementById("telefono").value = "";
    document.getElementById("email").value = "";
}