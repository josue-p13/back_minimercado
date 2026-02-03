const API_URL = "/api/proveedores";
let editando = false;

document.addEventListener("DOMContentLoaded", () => {
    cargarProveedores();
});

// 1. CARGAR (GET)
async function cargarProveedores() {
    try {
        const response = await fetch(API_URL);
        const resultado = await response.json();
        const tbody = document.querySelector("#tablaProveedores tbody");
        tbody.innerHTML = "";

        if (response.ok && resultado.success) {
            const lista = resultado.proveedores || [];
            if (lista.length === 0) {
                tbody.innerHTML = "<tr><td colspan='4'>No hay proveedores registrados.</td></tr>";
                return;
            }

            lista.forEach(p => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${p.nombre}</strong></td>
                    <td>${p.telefono || '-'}</td>
                    <td>${p.direccion || '-'}</td>
                    <td>
                        <button class="btn-edit" onclick='cargarDatosEdicion(${JSON.stringify(p)})'>
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-delete" onclick="eliminarProveedor(${p.id})">
                           <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// 2. GUARDAR (POST / PUT)
async function guardarProveedor() {
    const id = document.getElementById("proveedor_id").value;
    const nombre = document.getElementById("nombre").value;
    const telefono = document.getElementById("telefono").value;
    const direccion = document.getElementById("direccion").value;

    if (!nombre) {
        mostrarMensaje("El nombre es obligatorio", "red");
        return;
    }

    const datos = { nombre, telefono, direccion };

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
            mostrarMensaje(editando ? "Proveedor actualizado" : "Proveedor registrado", "green");
            limpiarFormulario();
            cargarProveedores();
        } else {
            mostrarMensaje("Error: " + (resultado.message || "Error al guardar"), "red");
        }
    } catch (error) {
        mostrarMensaje("Error de conexión", "red");
    }
}

// 3. EDITAR (UI)
function cargarDatosEdicion(proveedor) {
    editando = true;
    document.getElementById("proveedor_id").value = proveedor.id;
    document.getElementById("nombre").value = proveedor.nombre;
    document.getElementById("telefono").value = proveedor.telefono;
    document.getElementById("direccion").value = proveedor.direccion;

    document.getElementById("form-title").textContent = "Editar Proveedor";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-sync"></i> Actualizar';
    document.getElementById("btn-cancelar").style.display = "inline-block";
}

function limpiarFormulario() {
    editando = false;
    document.getElementById("proveedor_id").value = "";
    document.getElementById("nombre").value = "";
    document.getElementById("telefono").value = "";
    document.getElementById("direccion").value = "";

    document.getElementById("form-title").textContent = "Registrar Proveedor";
    document.getElementById("btn-guardar").innerHTML = '<i class="fas fa-save"></i> Guardar';
    document.getElementById("btn-cancelar").style.display = "none";
}

// 4. ELIMINAR (DELETE)
async function eliminarProveedor(id) {
    if (!confirm("¿Eliminar este proveedor?")) return;
    try {
        const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        const resultado = await response.json();
        if (resultado.success) {
            mostrarMensaje("Proveedor eliminado", "green");
            cargarProveedores();
        } else {
            alert(resultado.message);
        }
    } catch (error) { alert("Error de conexión"); }
}

function mostrarMensaje(texto, color) {
    const msg = document.getElementById("mensaje");
    msg.style.color = color === "green" ? "#2E7D32" : "#D32F2F";
    msg.textContent = texto;
    setTimeout(() => { msg.textContent = ""; }, 3000);
}