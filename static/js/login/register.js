document.addEventListener("DOMContentLoaded", () => {
    // Permitir registrarse al dar Enter en los campos
    const inputs = document.querySelectorAll("input, select");
    inputs.forEach(input => {
        input.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                registrar();
            }
        });
    });
});

async function registrar() {
    const nombre = document.getElementById("nombre").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const rol = document.getElementById("rol").value;
    const mensaje = document.getElementById("mensaje");

    const ROLES_VALIDOS = ["Admin", "Cajero", "Auxiliar"];

    if (!nombre || !username || !password || !rol) {
        mostrarMensaje("Todos los campos son obligatorios", "red");
        return;
    }

    if (!ROLES_VALIDOS.includes(rol)) {
        mostrarMensaje("Rol inválido", "red");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, username, password, rol })
        });

        const data = await response.json();

        if (response.ok && data.success) { // Aseguramos verificar data.success
            mostrarMensaje("Usuario registrado correctamente", "green");
            setTimeout(() => {
                window.location.href = "/login";
            }, 1500);
        } else {
            mostrarMensaje(data.message || data.detail || "Error al registrar", "red");
        }

    } catch (error) {
        mostrarMensaje("Error de conexión", "red");
        console.error(error);
    }
}

function mostrarMensaje(texto, color) {
    const mensaje = document.getElementById("mensaje");
    mensaje.style.color = color;
    mensaje.innerText = texto;
}