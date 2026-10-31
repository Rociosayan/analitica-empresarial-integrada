"""Genera rutamarket.db: datos SINTÉTICOS del caso RutaMarket para la Unidad 2.
Incluye a propósito problemas de calidad (nulos, duplicados, tipos incorrectos,
valores atípicos e inconsistencias) que se trabajan en la Semana 6."""
import sqlite3, os
import numpy as np, pandas as pd

rng = np.random.default_rng(2026)
N = 400
ciudades = ['Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Piura', 'Chiclayo']
p_ciudad = [0.45, 0.15, 0.12, 0.10, 0.10, 0.08]
# Segmentos latentes (no se guardan): define el comportamiento de compra
seg = rng.choice(4, size=N, p=[0.20, 0.25, 0.30, 0.25])
#            frecuentes-alto, ocasional-ticket-alto, frecuente-ticket-bajo, dormido
lam_ped = np.array([14, 4, 11, 2])[seg]
ticket_mu = np.array([280, 420, 90, 150])[seg]

cli = pd.DataFrame({
    'id_cliente': np.arange(1, N + 1),
    'nombre': [f'Cliente {i:03d}' for i in range(1, N + 1)],
    'ciudad': rng.choice(ciudades, size=N, p=p_ciudad),
    'edad': np.clip(rng.normal(36, 10, N).round(), 18, 72).astype(int),
    'canal_registro': rng.choice(['Web', 'App'], size=N, p=[0.55, 0.45]),
    'fecha_registro': pd.to_datetime('2023-01-01') + pd.to_timedelta(rng.integers(0, 1080, N), unit='D'),
})
cli['email'] = [f'cliente{i:03d}@correo.pe' for i in cli.id_cliente]
antig = ((pd.Timestamp('2025-12-31') - cli.fecha_registro).dt.days / 30.4)
# Visitas web mensuales: ligadas a la frecuencia de compra y a la antigüedad
cli['visitas_web_mes'] = np.clip(np.round(lam_ped * 0.9 + antig * 0.08 + rng.normal(0, 2.2, N)), 1, None).astype(int)

# Pedidos 2025
rows = []; det = []
productos = pd.DataFrame({
    'id_producto': range(1, 21),
    'nombre_producto': ['Audífonos inalámbricos', 'Mouse inalámbrico', 'Teclado mecánico', 'Monitor 24"', 'Parlante Bluetooth',
                        'Licuadora 600 W', 'Juego de sábanas', 'Freidora de aire', 'Set de ollas', 'Lámpara LED',
                        'Mancuernas 5 kg', 'Mat de yoga', 'Bicicleta estática', 'Zapatillas running', 'Tomatodo térmico',
                        'Libro Introducción a SQL', 'Novela contemporánea', 'Libro de cocina', 'Agenda 2026', 'Atlas del Perú'],
    'id_categoria': [1]*5 + [2]*5 + [3]*5 + [4]*5,
    'precio_unitario': [120, 45, 210, 650, 99, 189.9, 95, 329, 259, 39.9, 80, 55, 899, 279, 49.9, 65, 59, 79, 35, 89],
})
cats = pd.DataFrame({'id_categoria': [1, 2, 3, 4], 'nombre_categoria': ['Tecnología', 'Hogar', 'Deportes', 'Libros']})
pid = 10001
for i in range(N):
    k = max(1, rng.poisson(lam_ped[i]))
    if seg[i] == 3:   # dormidos: compras concentradas a inicios de año
        dias = rng.integers(0, 150, k)
    else:
        dias = rng.integers(0, 365, k)
    for dd in sorted(dias):
        target = rng.lognormal(np.log(ticket_mu[i]), 0.45)
        # elegir productos hasta aproximar el ticket
        n_items = 1 + rng.poisson(0.6)
        precios = productos.precio_unitario.values
        w = np.exp(-np.abs(np.log(precios) - np.log(target / n_items)))
        prods = rng.choice(productos.id_producto.values, size=min(n_items, 4), replace=False, p=w / w.sum())
        rows.append((pid, int(cli.id_cliente[i]), (pd.Timestamp('2025-01-01') + pd.Timedelta(days=int(dd))).strftime('%Y-%m-%d'),
                     rng.choice(['Tarjeta', 'Yape/Plin', 'Transferencia', 'Contraentrega'], p=[0.45, 0.30, 0.15, 0.10]),
                     rng.choice(['Entregado', 'Devuelto'], p=[0.95, 0.05])))
        for p in prods:
            det.append((pid, int(p), int(1 + rng.poisson(0.3)), float(productos.precio_unitario[p - 1])))
        pid += 1
ped = pd.DataFrame(rows, columns=['id_pedido', 'id_cliente', 'fecha_pedido', 'metodo_pago', 'estado'])
dp = pd.DataFrame(det, columns=['id_pedido', 'id_producto', 'cantidad', 'precio_unitario'])

# ---------- problemas de calidad (a propósito) ----------
cli['edad'] = cli['edad'].astype(str)
idx = rng.choice(N, 28, replace=False); cli.loc[idx, 'edad'] = ''                    # vacíos
idx2 = rng.choice(list(set(range(N)) - set(idx)), 6, replace=False); cli.loc[idx2, 'edad'] = 'N.D.'  # texto
cli.loc[rng.choice(N, 2, replace=False), 'edad'] = '150'                             # imposible
idx3 = rng.choice(N, 12, replace=False); cli.loc[idx3, 'ciudad'] = None              # ciudad faltante
ok = cli.index[cli.ciudad.notna()]
idx4 = rng.choice(ok, 18, replace=False)
cli.loc[idx4, 'ciudad'] = [c.lower() if j % 2 else f' {c.upper()} ' for j, c in enumerate(cli.loc[idx4, 'ciudad'])]
cli['fecha_registro'] = cli.fecha_registro.dt.strftime('%Y-%m-%d')
# clientes duplicados (mismo email, otro id)
dup = cli.sample(8, random_state=7).copy(); dup['id_cliente'] = range(N + 1, N + 9)
cli = pd.concat([cli, dup], ignore_index=True)
# pedidos duplicados por doble registro (mismo cliente, fecha, método; id consecutivo)
dups = ped.sample(15, random_state=3).copy(); dups['id_pedido'] = range(pid, pid + 15)
mapa = dict(zip(ped.loc[dups.index, 'id_pedido'], dups.id_pedido))
ddet = dp[dp.id_pedido.isin(mapa)].copy(); ddet['id_pedido'] = ddet.id_pedido.map(mapa)
ped = pd.concat([ped, dups], ignore_index=True); dp = pd.concat([dp, ddet], ignore_index=True)
# método de pago faltante
ped.loc[rng.choice(len(ped), 90, replace=False), 'metodo_pago'] = None
# errores de digitación en precio (x100) en 6 líneas
bad = rng.choice(len(dp), 6, replace=False); dp.loc[bad, 'precio_unitario'] = dp.loc[bad, 'precio_unitario'] * 100

if os.path.exists('rutamarket.db'):
    os.remove('rutamarket.db')
con = sqlite3.connect('rutamarket.db')
cats.to_sql('categorias', con, index=False)
productos.to_sql('productos', con, index=False)
cli[['id_cliente', 'nombre', 'ciudad', 'edad', 'canal_registro', 'fecha_registro', 'email', 'visitas_web_mes']].to_sql('clientes', con, index=False, dtype={'edad': 'TEXT'})
ped.to_sql('pedidos', con, index=False)
dp.to_sql('detalle_pedido', con, index=False)
con.close()
print(len(cli), len(ped), len(dp))
