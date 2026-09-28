import sqlite3
CATEGORIAS=[(1,'Tecnología'),(2,'Hogar'),(3,'Deportes'),(4,'Libros')]
PRODUCTOS=[(1,'Audífonos inalámbricos',1,120.00),(2,'Mouse inalámbrico',1,45.00),(3,'Teclado mecánico',1,210.00),
 (4,'Licuadora 600 W',2,189.90),(5,'Juego de sábanas',2,95.00),(6,'Mancuernas 5 kg',3,80.00),(7,'Mat de yoga',3,55.00),
 (8,'Libro Introducción a SQL',4,65.00)]
CLIENTES=[(1,'Ana Torres','Lima','ana.torres@correo.pe','2025-11-04'),(2,'Luis Quispe','Arequipa','luis.quispe@correo.pe','2025-12-10'),
 (3,'María Huamán','Cusco','maria.huaman@correo.pe','2026-01-15'),(4,'Jorge Ramos','Lima','jorge.ramos@correo.pe','2026-01-20'),
 (5,'Rosa Flores','Trujillo','rosa.flores@correo.pe','2026-02-02'),(6,'Carlos Mendoza','Piura','carlos.mendoza@correo.pe','2026-02-25')]
PEDIDOS=[(101,1,'2026-03-02','Entregado'),(102,2,'2026-03-05','Entregado'),(103,1,'2026-03-09','Entregado'),(104,3,'2026-03-12','Entregado'),
 (105,4,'2026-03-15','Entregado'),(106,5,'2026-03-20','Entregado'),(107,2,'2026-03-24','En camino'),(108,4,'2026-03-28','En camino')]
DETALLE=[(101,1,1),(101,2,2),(102,4,1),(103,3,1),(103,7,1),(104,6,2),(104,7,1),(105,1,2),(106,5,2),(107,2,1),(107,3,1),(108,4,1),(108,6,1)]
def conectar():
    c=sqlite3.connect(':memory:')
    c.executescript('''
    CREATE TABLE categorias(id_categoria INTEGER PRIMARY KEY, nombre_categoria TEXT NOT NULL);
    CREATE TABLE productos(id_producto INTEGER PRIMARY KEY, nombre_producto TEXT NOT NULL, id_categoria INTEGER NOT NULL REFERENCES categorias(id_categoria), precio_unitario REAL NOT NULL);
    CREATE TABLE clientes(id_cliente INTEGER PRIMARY KEY, nombre TEXT NOT NULL, ciudad TEXT, email TEXT UNIQUE, fecha_registro TEXT);
    CREATE TABLE pedidos(id_pedido INTEGER PRIMARY KEY, id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente), fecha_pedido TEXT NOT NULL, estado TEXT NOT NULL);
    CREATE TABLE detalle_pedido(id_pedido INTEGER REFERENCES pedidos(id_pedido), id_producto INTEGER REFERENCES productos(id_producto), cantidad INTEGER NOT NULL, precio_unitario REAL NOT NULL, PRIMARY KEY(id_pedido,id_producto));
    ''')
    c.executemany('INSERT INTO categorias VALUES(?,?)',CATEGORIAS)
    c.executemany('INSERT INTO productos VALUES(?,?,?,?)',PRODUCTOS)
    c.executemany('INSERT INTO clientes VALUES(?,?,?,?,?)',CLIENTES)
    c.executemany('INSERT INTO pedidos VALUES(?,?,?,?)',PEDIDOS)
    precio={p[0]:p[3] for p in PRODUCTOS}
    c.executemany('INSERT INTO detalle_pedido VALUES(?,?,?,?)',[(a,b,q,precio[b]) for a,b,q in DETALLE])
    c.executescript('''
    CREATE TABLE ventas AS
    SELECT ROW_NUMBER() OVER (ORDER BY d.id_pedido, d.rowid) AS id_venta, p.id_pedido, p.fecha_pedido AS fecha, c.nombre AS cliente, c.ciudad,
      pr.nombre_producto AS producto, ca.nombre_categoria AS categoria, d.cantidad, d.precio_unitario,
      ROUND(d.cantidad*d.precio_unitario,2) AS total
    FROM detalle_pedido d JOIN pedidos p USING(id_pedido) JOIN clientes c USING(id_cliente)
    JOIN productos pr USING(id_producto) JOIN categorias ca USING(id_categoria);
    ''')
    return c
def run(c,sql):
    cur=c.execute(sql); return [d[0] for d in cur.description], cur.fetchall()
