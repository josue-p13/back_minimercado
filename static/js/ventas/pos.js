let carrito = [];
let productosGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
    cargarProductos();
    cargarClientes();
});

// ==========================================
// 1. CARGA DE DATOS
// ==========================================

async function cargarProductos() {
    const res = await fetch("/api/inventario/productos");
    const data = await res.json();
    if (data.success) {
        productosGlobal = data.productos;
        renderizarProductos(productosGlobal);
    }
}

async function cargarClientes() {
    const res = await fetch("/api/clientes");
    const data = await res.json();
    if (data.success) {
        const select = document.getElementById("select-cliente");
        data.clientes.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.id;
            opt.text = c.nombre;
            select.appendChild(opt);
        });
    }
}

// ==========================================
// 2. RENDERIZADO Y BUSQUEDA
// ==========================================

function renderizarProductos(lista) {
    const container = document.getElementById("lista-productos");
    container.innerHTML = "";

    lista.forEach(p => {
        if (p.stock > 0) { // Solo mostrar si hay stock
            const card = document.createElement("div");
            card.className = "product-card";
            card.onclick = () => agregarAlCarrito(p);
            card.innerHTML = `
                <div style="font-weight:bold;">${p.nombre}</div>
                <div class="product-price">$${p.precio.toFixed(2)}</div>
                <small style="color:#666;">Stock: ${p.stock}</small>
            `;
            container.appendChild(card);
        }
    });
}

function filtrarProductos() {
    const texto = document.getElementById("buscador").value.toLowerCase();
    const filtrados = productosGlobal.filter(p => p.nombre.toLowerCase().includes(texto));
    renderizarProductos(filtrados);
}

// ==========================================
// 3. LOGICA DEL CARRITO
// ==========================================

function agregarAlCarrito(producto) {
    // Buscar si ya existe
    const itemExistente = carrito.find(item => item.producto_id === producto.id);

    if (itemExistente) {
        if (itemExistente.cantidad < producto.stock) {
            itemExistente.cantidad++;
        } else {
            alert("No hay más stock disponible");
        }
    } else {
        carrito.push({
            producto_id: producto.id,
            nombre: producto.nombre,
            precio: producto.precio,
            cantidad: 1,
            stock_max: producto.stock
        });
    }
    actualizarVistaCarrito();
}

function eliminarDelCarrito(index) {
    carrito.splice(index, 1);
    actualizarVistaCarrito();
}

function actualizarVistaCarrito() {
    const tbody = document.getElementById("tabla-carrito");
    tbody.innerHTML = "";
    let total = 0;

    carrito.forEach((item, index) => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.nombre}</td>
            <td>${item.cantidad}</td>
            <td>$${subtotal.toFixed(2)}</td>
            <td><i class="fas fa-times" style="color:red; cursor:pointer;" onclick="eliminarDelCarrito(${index})"></i></td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById("total-venta").textContent = total.toFixed(2);
}

// ==========================================
// 4. PROCESO DE PAGO (MODAL)
// ==========================================

function procesarVenta() {
    if (carrito.length === 0) {
        alert("El carrito está vacío");
        return;
    }

    // Calcular total actual
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    // Configurar Modal
    document.getElementById("modal-total-pagar").textContent = "$" + total.toFixed(2);
    document.getElementById("modal-pago").style.display = "flex";

    // Resetear campos del modal
    document.getElementById("select-metodo").value = "Efectivo";
    document.getElementById("input-recibido").value = "";
    document.getElementById("lbl-cambio").textContent = "$0.00";
    document.getElementById("lbl-cambio").style.color = "#666";

    document.getElementById("input-lote").value = "";
    document.getElementById("input-voucher").value = "";
    document.getElementById("input-ref-transf").value = "";

    cambiarMetodoPago(); // Ajustar visibilidad inicial

    // Enfocar input efectivo automáticamente
    setTimeout(() => document.getElementById("input-recibido").focus(), 100);
}

function cerrarModalPago() {
    document.getElementById("modal-pago").style.display = "none";
}

function cambiarMetodoPago() {
    const metodo = document.getElementById("select-metodo").value;

    // Ocultar todos primero
    document.getElementById("div-efectivo").style.display = "none";
    document.getElementById("div-tarjeta").style.display = "none";
    document.getElementById("div-transferencia").style.display = "none";

    // Mostrar el seleccionado
    if (metodo === "Efectivo") {
        document.getElementById("div-efectivo").style.display = "block";
        setTimeout(() => document.getElementById("input-recibido").focus(), 100);
    } else if (metodo === "Tarjeta") {
        document.getElementById("div-tarjeta").style.display = "block";
        setTimeout(() => document.getElementById("input-lote").focus(), 100);
    } else if (metodo === "Transferencia") {
        document.getElementById("div-transferencia").style.display = "block";
        setTimeout(() => document.getElementById("input-ref-transf").focus(), 100);
    }
}

function calcularCambio() {
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const recibido = parseFloat(document.getElementById("input-recibido").value) || 0;
    const cambio = recibido - total;

    const lbl = document.getElementById("lbl-cambio");
    if (cambio >= 0) {
        lbl.textContent = "$" + cambio.toFixed(2);
        lbl.style.color = "#2E7D32"; // Verde
    } else {
        lbl.textContent = "Falta: $" + Math.abs(cambio).toFixed(2);
        lbl.style.color = "#D32F2F"; // Rojo
    }
}

// ==========================================
// 5. ENVÍO FINAL AL BACKEND
// ==========================================

async function confirmarVenta() {
    const metodo = document.getElementById("select-metodo").value;
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const clienteId = document.getElementById("select-cliente").value;

    let montoPago = 0;
    let referencia = "";

    // --- Validaciones según método ---
    if (metodo === "Efectivo") {
        montoPago = parseFloat(document.getElementById("input-recibido").value) || 0;

        // Pequeño margen de error para flotantes, pero validamos estricto
        if (montoPago < total) {
            alert("El monto recibido es menor al total de la venta.");
            return;
        }
    } else if (metodo === "Tarjeta") {
        montoPago = total; // En tarjeta se asume pago exacto
        const lote = document.getElementById("input-lote").value.trim();
        const voucher = document.getElementById("input-voucher").value.trim();

        if (!lote || !voucher) {
            alert("Por favor ingresa el Lote y el Número de Comprobante.");
            return;
        }
        referencia = `Lote: ${lote} - Ref: ${voucher}`;

    } else if (metodo === "Transferencia") {
        montoPago = total; // En transferencia se asume pago exacto
        const ref = document.getElementById("input-ref-transf").value.trim();

        if (!ref) {
            alert("Por favor ingresa el Número de Referencia de la transferencia.");
            return;
        }
        referencia = `Ref: ${ref}`;
    }

    // --- Preparar JSON para el backend ---
    const ventaData = {
        items: carrito.map(i => ({ producto_id: i.producto_id, cantidad: i.cantidad })),
        fk_cliente: clienteId ? parseInt(clienteId) : null,
        fk_usuario: 1, // Nota: Esto se reemplazará por el usuario del Token en el futuro
        metodo_pago: metodo,
        monto_pago: montoPago,
        referencia: referencia
    };

    try {
        const res = await fetch("/api/ventas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(ventaData)
        });

        const resultado = await res.json();

        if (resultado.success) {
            // Mensaje de éxito
            let msg = "✅ Venta realizada correctamente.";
            if (metodo === "Efectivo") {
                msg += `\n\n💰 Su cambio es: $${resultado.cambio.toFixed(2)}`;
            }
            alert(msg);

            // Resetear todo
            cerrarModalPago();
            carrito = [];
            actualizarVistaCarrito();
            cargarProductos(); // Recargar para ver el stock actualizado

        } else {
            alert("❌ Error: " + (resultado.message || "No se pudo procesar la venta."));
        }

    } catch (error) {
        console.error(error);
        alert("Error de conexión con el servidor.");
    }
}