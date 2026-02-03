// Agregamos los escuchadores de eventos para la tecla ENTER
document.addEventListener("DOMContentLoaded", () => {
    // Permitir Enter en el campo de contraseña
    document.getElementById("password").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Evitar comportamientos por defecto
            login(); // Ejecutar la función de login
        }
    });

    // Opcional: Permitir Enter también en el campo usuario
    document.getElementById("username").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            // Si da enter en usuario, pasamos el foco a la contraseña
            document.getElementById("password").focus();
        }
    });
});

async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const mensaje = document.getElementById("mensaje");

    if (!username || !password) {
        mensaje.style.color = "red";
        mensaje.innerText = "Usuario y contraseña obligatorios";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            mensaje.style.color = "red";
            mensaje.innerText = data.detail || "Credenciales inválidas";
            return;
        }

        // Guardar sesión
        localStorage.setItem("token", data.token);
        localStorage.setItem("usuario", JSON.stringify(data.usuario));

        const rol = data.usuario.rol;

        // 🔀 Redirección por rol
        if (rol === "Admin") {
            window.location.href = "/admin";
        } else if (rol === "Cajero") {
            window.location.href = "/caja";
        } else if (rol === "Auxiliar") {
            window.location.href = "/auxiliar";
        } else {
            mensaje.style.color = "red";
            mensaje.innerText = "Rol no reconocido";
        }

    } catch (error) {
        mensaje.style.color = "red";
        mensaje.innerText = "Error de conexión con el servidor";
        console.error(error);
    }
}