Q={}
Q['s2_select']="""SELECT fecha, cliente, producto, total
FROM ventas
LIMIT 5;"""
Q['s2_distinct']="""SELECT DISTINCT categoria
FROM ventas;"""
Q['s2_where']="""SELECT fecha, cliente, producto, total
FROM ventas
WHERE ciudad = 'Lima';"""
Q['s2_order']="""SELECT fecha, cliente, producto, total
FROM ventas
WHERE total >= 150
ORDER BY total DESC;"""
Q['s2_and']="""SELECT cliente, ciudad, producto, total
FROM ventas
WHERE categoria = 'Tecnología'
  AND ciudad = 'Lima';"""
Q['s2_or']="""SELECT cliente, ciudad, producto, total
FROM ventas
WHERE ciudad = 'Cusco'
   OR ciudad = 'Trujillo';"""
Q['s2_agg']="""SELECT COUNT(*)             AS lineas_venta,
       SUM(total)           AS ingresos,
       ROUND(AVG(total), 2) AS ticket_promedio,
       MAX(total)           AS venta_maxima,
       MIN(total)           AS venta_minima
FROM ventas;"""
Q['s2_group']="""SELECT categoria,
       COUNT(*)   AS lineas_venta,
       SUM(total) AS ingresos
FROM ventas
GROUP BY categoria
ORDER BY ingresos DESC;"""
Q['s2_top5']="""SELECT producto,
       SUM(cantidad) AS unidades,
       SUM(total)    AS ingresos
FROM ventas
GROUP BY producto
ORDER BY ingresos DESC
LIMIT 5;"""
Q['s3_inner']="""SELECT p.id_pedido,
       c.nombre AS cliente,
       c.ciudad,
       p.fecha_pedido,
       p.estado
FROM pedidos AS p
INNER JOIN clientes AS c
        ON p.id_cliente = c.id_cliente
ORDER BY p.fecha_pedido;"""
Q['s3_left']="""SELECT c.nombre   AS cliente,
       c.ciudad,
       p.id_pedido
FROM clientes AS c
LEFT JOIN pedidos AS p
       ON c.id_cliente = p.id_cliente
ORDER BY c.id_cliente;"""
Q['s3_left_null']="""SELECT c.nombre AS cliente, c.ciudad, c.fecha_registro
FROM clientes AS c
LEFT JOIN pedidos AS p
       ON c.id_cliente = p.id_cliente
WHERE p.id_pedido IS NULL;"""
Q['s3_multi']="""SELECT ca.nombre_categoria                   AS categoria,
       SUM(d.cantidad)                       AS unidades,
       SUM(d.cantidad * d.precio_unitario)   AS ingresos
FROM detalle_pedido AS d
INNER JOIN productos  AS pr ON d.id_producto  = pr.id_producto
INNER JOIN categorias AS ca ON pr.id_categoria = ca.id_categoria
GROUP BY ca.nombre_categoria
ORDER BY ingresos DESC;"""
Q['s3_multi_cli']="""SELECT c.nombre                               AS cliente,
       COUNT(DISTINCT p.id_pedido)            AS pedidos,
       SUM(d.cantidad * d.precio_unitario)    AS monto_total
FROM clientes AS c
INNER JOIN pedidos        AS p ON c.id_cliente = p.id_cliente
INNER JOIN detalle_pedido AS d ON p.id_pedido  = d.id_pedido
GROUP BY c.nombre
ORDER BY monto_total DESC;"""
Q['s3_having']="""SELECT c.nombre                               AS cliente,
       SUM(d.cantidad * d.precio_unitario)    AS monto_total
FROM clientes AS c
INNER JOIN pedidos        AS p ON c.id_cliente = p.id_cliente
INNER JOIN detalle_pedido AS d ON p.id_pedido  = d.id_pedido
WHERE p.estado = 'Entregado'
GROUP BY c.nombre
HAVING SUM(d.cantidad * d.precio_unitario) > 300
ORDER BY monto_total DESC;"""
Q['s3_sub_avg']="""SELECT nombre_producto, precio_unitario
FROM productos
WHERE precio_unitario > (SELECT AVG(precio_unitario)
                         FROM productos)
ORDER BY precio_unitario DESC;"""
Q['s3_sub_in']="""SELECT nombre_producto, precio_unitario
FROM productos
WHERE id_producto NOT IN (SELECT id_producto
                          FROM detalle_pedido);"""
Q['int_ciudad']="""SELECT c.ciudad,
       COUNT(DISTINCT p.id_pedido)           AS pedidos,
       SUM(d.cantidad * d.precio_unitario)   AS ingresos
FROM clientes AS c
INNER JOIN pedidos        AS p ON c.id_cliente = p.id_cliente
INNER JOIN detalle_pedido AS d ON p.id_pedido  = d.id_pedido
GROUP BY c.ciudad
ORDER BY ingresos DESC;"""
