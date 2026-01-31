async function registrar() {
    const nombre = document.getElementById("nombre").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const rol = document.getElementById("rol").value;
    const mensaje = document.getElementById("mensaje");

    const ROLES_VALIDOS = ["Admin", "Cajero", "Auxiliar"];

    // Validación básica
    if (!nombre || !username || !password || !rol) {
        mensaje.style.color = "red";
        mensaje.innerText = "Todos los campos son obligatorios";
        return;
    }

    // Validación de rol
    if (!ROLES_VALIDOS.includes(rol)) {
        mensaje.style.color = "red";
        mensaje.innerText = "Rol inválido. Debe ser Admin, Cajero o Auxiliar";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nombre,
                username,
                password,
                rol
            })
        });

        const data = await response.json();

        if (response.ok) {
            mensaje.style.color = "green";
            mensaje.innerText = "Usuario registrado correctamente";

            setTimeout(() => {
                window.location.href = "/login";
            }, 1500);
        } else {
            mensaje.style.color = "red";
            mensaje.innerText = data.detail || "Error al registrar usuario";
        }

    } catch (error) {
        mensaje.style.color = "red";
        mensaje.innerText = "Error de conexión con el servidor";
        console.error(error);
    }
}
