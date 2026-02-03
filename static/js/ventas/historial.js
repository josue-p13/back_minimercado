document.addEventListener("DOMContentLoaded", () => {
    cargarVentas();
});

async function cargarVentas() {
    try {
        const res = await fetch("/api/ventas");
        const data = await res.json();

        const tbody = document.getElementById("tabla-ventas");
        tbody.innerHTML = "";

        if (data.success) {
            data.ventas.forEach(v => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>#${v.id}</strong></td>
                    <td>${v.fecha}</td>
                    <td>${v.cliente}</td>
                    <td>${v.usuario}</td>
                    <td style="font-weight:bold; color:#2E7D32;">$${v.total.toFixed(2)}</td>
                    <td>
                        <button class="btn-detalle" onclick="verDetalle(${v.id})">
                            <i class="fas fa-eye"></i> Ver
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

async function verDetalle(id) {
    try {
        const res = await fetch(`/api/ventas/${id}`);
        const data = await res.json();

        if (data.success) {
            const v = data.venta;
            document.getElementById("detalle-id").textContent = v.id;
            document.getElementById("detalle-total").textContent = "$" + v.total.toFixed(2);

            const lista = document.getElementById("lista-items");
            lista.innerHTML = "";

            v.items.forEach(item => {
                const div = document.createElement("div");
                div.className = "item-row";
                div.innerHTML = `
                    <span><strong>${item.cantidad}x</strong> ${item.producto}</span>
                    <span>$${item.subtotal.toFixed(2)}</span>
                `;
                lista.appendChild(div);
            });

            // CORRECCIÓN: Usamos 'flex' para que el modal se centre gracias al CSS
            document.getElementById("modal-detalle").style.display = "flex";
        }
    } catch (error) {
        console.error("Error al ver detalle:", error);
    }
}