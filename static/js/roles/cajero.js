document.addEventListener("DOMContentLoaded", () => {
    verificarEstadoCaja();
});

// 1. VERIFICAR ESTADO (GET)
async function verificarEstadoCaja() {
    try {
        const response = await fetch("/api/caja/actual");
        const resultado = await response.json();

        if (resultado.success && resultado.abierta) {
            // CAJA ABIERTA
            document.getElementById("view-closed").style.display = "none";
            document.getElementById("view-open").style.display = "block";

            // Llenar datos
            document.getElementById("fecha_apertura_display").textContent = resultado.caja.fecha_apertura;
            document.getElementById("base_inicial_display").textContent = "$" + resultado.caja.monto_inicial;
        } else {
            // CAJA CERRADA
            document.getElementById("view-closed").style.display = "block";
            document.getElementById("view-open").style.display = "none";
            document.getElementById("zona-cierre").style.display = "none";
        }

    } catch (error) {
        console.error("Error verificando caja:", error);
        alert("Error de conexión con el servidor");
    }
}

// 2. ABRIR CAJA (POST)
async function abrirCaja() {
    const monto = document.getElementById("monto_inicial").value;

    if (monto === "" || parseFloat(monto) < 0) {
        alert("Ingresa un monto válido");
        return;
    }

    try {
        const response = await fetch("/api/caja/abrir", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                monto_inicial: parseFloat(monto),
                fk_usuario: 1 // Temporal
            })
        });

        const resultado = await response.json();

        if (resultado.success) {
            alert("¡Caja abierta correctamente!");
            verificarEstadoCaja();
        } else {
            alert("Error: " + resultado.message);
        }

    } catch (error) {
        console.error(error);
        alert("Error al abrir caja");
    }
}

// 3. CERRAR CAJA (POST)
async function cerrarCaja() {
    const monto = document.getElementById("monto_final").value;

    if (!monto) {
        alert("Debes ingresar el total del dinero en caja");
        return;
    }

    if (!confirm("¿Seguro que deseas cerrar el turno? Esto bloqueará las ventas.")) return;

    try {
        const response = await fetch("/api/caja/cerrar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                monto_final: parseFloat(monto)
            })
        });

        const resultado = await response.json();

        if (resultado.success) {
            alert("Turno cerrado correctamente.");
            location.reload(); // Recargar para volver a la pantalla de apertura
        } else {
            alert("Error: " + resultado.message);
        }

    } catch (error) {
        console.error(error);
    }
}

// Funciones de UI
function mostrarCierre() {
    document.getElementById("zona-cierre").style.display = "block";
}
function ocultarCierre() {
    document.getElementById("zona-cierre").style.display = "none";
}
function irAFacturacion() {
    // Aún no tenemos esta página, pero la dejaremos lista
    window.location.href = "/ventas/nuevo";
}