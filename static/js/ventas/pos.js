let carrito = [];
let productosGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
    cargarProductos();
    cargarClientes();
});

// 1. CARGAR DATOS INICIALES
async function cargarProductos() {
    const res = await fetch("/api/inventario/productos");
    const data = await res.json();
    if(data.success) {
        productosGlobal = data.productos;
        renderizarProductos(productosGlobal);
    }
}

async function cargarClientes() {
    const res = await fetch("/api/clientes");
    const data = await res.json();
    if(data.success) {
        const select = document.getElementById("select-cliente");
        data.clientes.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.id;
            opt.text = c.nombre;
            select.appendChild(opt);
        });
    }
}

// 2. RENDERIZADO DE PRODUCTOS (GRID)
function renderizarProductos(lista) {
    const container = document.getElementById("lista-productos");
    container.innerHTML = "";
    
    lista.forEach(p => {
        if(p.stock > 0) { // Solo mostrar si hay stock
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

// 3. LÓGICA DEL CARRITO
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

// 4. PROCESAR VENTA (POST)
async function procesarVenta() {
    if (carrito.length === 0) {
        alert("El carrito está vacío");
        return;
    }

    const clienteId = document.getElementById("select-cliente").value;
    
    const ventaData = {
        items: carrito.map(i => ({ producto_id: i.producto_id, cantidad: i.cantidad })),
        fk_cliente: clienteId ? parseInt(clienteId) : null,
        fk_usuario: 1 // Temporal
    };

    try {
        const res = await fetch("/api/ventas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(ventaData)
        });
        
        const resultado = await res.json();
        
        if (resultado.success) {
            alert("¡Venta realizada con éxito!");
            carrito = []; // Limpiar carrito
            actualizarVistaCarrito();
            cargarProductos(); // Recargar stock visual
        } else {
            alert("Error: " + resultado.message);
        }

    } catch (error) {
        console.error(error);
        alert("Error de conexión");
    }
}