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
    try {
        const res = await fetch("/api/inventario/productos");
        const data = await res.json();
        if (data.success) {
            productosGlobal = data.productos;
            renderizarProductos(productosGlobal);
        }
    } catch (e) { console.error("Error cargando productos", e); }
}

async function cargarClientes() {
    try {
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
    } catch (e) { console.error("Error cargando clientes", e); }
}

// ==========================================
// 2. RENDERIZADO Y BÚSQUEDA
// ==========================================

function renderizarProductos(lista) {
    const container = document.getElementById("lista-productos");
    container.innerHTML = "";

    lista.forEach(p => {
        if (p.stock > 0) {
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
// 3. LÓGICA DEL CARRITO
// ==========================================

function agregarAlCarrito(producto) {
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
// 4. LÓGICA DEL MODAL DE PAGO
// ==========================================

function procesarVenta() {
    if (carrito.length === 0) {
        alert("El carrito está vacío");
        return;
    }

    // Calcular total
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    // Abrir Modal
    document.getElementById("modal-total-pagar").textContent = "$" + total.toFixed(2);
    document.getElementById("modal-pago").style.display = "flex";

    // Resetear campos
    document.getElementById("select-metodo").value = "Efectivo";
    document.getElementById("input-recibido").value = "";
    document.getElementById("lbl-cambio").textContent = "$0.00";
    document.getElementById("lbl-cambio").style.color = "#666";
    document.getElementById("input-lote").value = "";
    document.getElementById("input-voucher").value = "";
    document.getElementById("input-ref-transf").value = "";

    cambiarMetodoPago();
    setTimeout(() => document.getElementById("input-recibido").focus(), 100);
}

function cerrarModalPago() {
    document.getElementById("modal-pago").style.display = "none";
}

function cambiarMetodoPago() {
    const metodo = document.getElementById("select-metodo").value;

    document.getElementById("div-efectivo").style.display = "none";
    document.getElementById("div-tarjeta").style.display = "none";
    document.getElementById("div-transferencia").style.display = "none";

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
    if (cambio >= -0.01) { // Pequeña tolerancia para floats
        lbl.textContent = "$" + (cambio > 0 ? cambio : 0).toFixed(2);
        lbl.style.color = "#2E7D32";
    } else {
        lbl.textContent = "Falta: $" + Math.abs(cambio).toFixed(2);
        lbl.style.color = "#D32F2F";
    }
}

// ==========================================
// 5. ENVÍO AL SERVIDOR (AQUÍ OCURRE EL COBRO)
// ==========================================

async function confirmarVenta() {
    const metodo = document.getElementById("select-metodo").value;
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const clienteId = document.getElementById("select-cliente").value;

    let montoPago = 0;
    let referencia = "";

    // VALIDACIONES DEL CLIENTE
    if (metodo === "Efectivo") {
        montoPago = parseFloat(document.getElementById("input-recibido").value) || 0;
        if (montoPago < total) {
            alert("El monto recibido es menor al total.");
            return;
        }
    } else if (metodo === "Tarjeta") {
        montoPago = total;
        const lote = document.getElementById("input-lote").value.trim();
        const voucher = document.getElementById("input-voucher").value.trim();
        if (!lote || !voucher) {
            alert("Ingrese Lote y Voucher"); return;
        }
        referencia = `Lote: ${lote} - Ref: ${voucher}`;
    } else if (metodo === "Transferencia") {
        montoPago = total;
        const ref = document.getElementById("input-ref-transf").value.trim();
        if (!ref) {
            alert("Ingrese Referencia"); return;
        }
        referencia = `Ref: ${ref}`;
    }

    // JSON QUE SE ENVÍA (Debe coincidir con VentaRequest en Python)
    const ventaData = {
        items: carrito.map(i => ({ producto_id: i.producto_id, cantidad: i.cantidad })),
        fk_cliente: clienteId ? parseInt(clienteId) : null,
        fk_usuario: 1, // Temporal
        metodo_pago: metodo,
        monto_pago: montoPago,
        referencia: referencia ? referencia : null // Enviar null si está vacío
    };

    try {
        const res = await fetch("/api/ventas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(ventaData)
        });

        const resultado = await res.json();

        if (resultado.success) {
            let msg = "✅ Venta exitosa.";
            if (metodo === "Efectivo" && resultado.cambio > 0) {
                msg += `\n\n💰 Su cambio es: $${resultado.cambio.toFixed(2)}`;
            }
            alert(msg);

            cerrarModalPago();
            carrito = [];
            actualizarVistaCarrito();
            cargarProductos();
        } else {
            alert("Error del servidor: " + (resultado.message || resultado.detail));
        }

    } catch (error) {
        console.error(error);
        alert("Error de conexión");
    }
}