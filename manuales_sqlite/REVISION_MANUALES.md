# Revisión de los manuales de SQLite · Fundamentos de Gestión de Datos 2026-II

Se revisaron los cinco archivos recibidos **ejecutando su código** en Python con SQLite (versión 3.45.1):

| Archivo original | Contenido | Reemplazado por |
|---|---|---|
| `manual_sqlite.pdf` | SQLite con la base AynyTech (mezcla nivel básico e intermedio) | `01_SQLite_Basico.ipynb` y `02_SQLite_Intermedio.ipynb` |
| `manual_sql_avanzado.html` / `.pdf` / `_joins.pdf` | Tres versiones del mismo manual avanzado (Lab D3) | `03_SQLite_Avanzado.ipynb` |
| `manual_modelado_relacional.pdf` | Modelo ER, cardinalidad, normalización, Lab D4 | `04_Modelado_Relacional_SQLite.ipynb` |

Los cuatro cuadernos se ejecutan de principio a fin sin errores, se pueden repetir sin duplicar datos y todos los resultados que comentan salen de ejecutar el código.

## Errores encontrados (y cómo quedaron corregidos)

### Errores que impiden ejecutar el manual

| # | Manual | Error | Corrección |
|---|---|---|---|
| 1 | `manual_sqlite` | Las celdas 1 y 2 usan `--` como comentario **dentro de código Python**. En Python `--` no es un comentario: da `SyntaxError` | En Python los comentarios son `#`; `--` solo dentro del texto de la consulta |
| 2 | `manual_sqlite`, `manual_modelado`, `manual_sql_avanzado` | `CREATE TABLE` e `INSERT` escritos como **SQLite suelto dentro de una celda de Python**, sin `cur.execute(...)`. Falla con `SyntaxError`, y por eso **todas las celdas siguientes fallan** con `no such table` | Todas las sentencias que cambian la base van dentro de `ejecutar("""...""")` |
| 3 | `manual_sql_avanzado` | Los bloques traen caracteres `■` dentro del código, que no son válidos | Eliminados |
| 4 | `manual_modelado` (Paso 3) | `cur.execute('''...` se cierra con `')` (una sola comilla): la cadena queda abierta. Además apunta a `entidad_a` y `entidad_b`, que no existen | Plantilla reemplazada por un ejemplo completo que sí ejecuta (4 tablas, 5 o más filas por tabla) |
| 5 | `manual_modelado` (Paso 4) | `INSERT` suelto, con `...` como relleno | Ejemplo completo con datos ficticios |
| 6 | Los tres manuales | Al volver a ejecutar las celdas se **duplican los datos** y falla `UNIQUE` en el correo | Cada celda de creación empieza con `DROP TABLE IF EXISTS` (en orden: primero la tabla hija) |
| 7 | `manual_sql_avanzado` | La sección 5.4 borra la vista `v_ventas_cliente` y la consulta D3-5, más adelante, la necesita: `no such table` | La limpieza de vistas pasa al **final** del cuaderno |

### Resultados mostrados que no coinciden con lo que da el código

| Dónde | El manual dice | El código devuelve |
|---|---|---|
| María Quispe, total comprado (2.2, 4.2, D3-1) | 5240 | **5140** |
| Carlos Ttito, total comprado (2.2, 4.2, D3-1) | 4000 | **4020** |
| María Quispe, `Unidades_Total` (D3-1) | 7 | **8** |
| Hardware, pedidos (3.1) | 4 | **3** |
| Software, pedidos (3.1) | 7 | **6** |
| Software, total de ventas (3.1 y 3.2) | 3870 | **4050** |
| Servicio, pedidos (3.1) | 4 | **6** |
| Servicio, total de ventas (3.1) | 2250 | **2750** |
| Tabla de la sección 4.2 | 4 filas | La consulta devuelve **9 filas** |

Además, la columna `Precio_Promedio` de la sección 3.1 (`AVG(pr.precio)`) promedia el precio de cada **fila de pedido**, no del catálogo, así que se pondera por el número de pedidos y confunde. Pasó a **`Ticket_Promedio`** (monto promedio por pedido).

### Errores de contenido

| # | Manual | Error | Corrección |
|---|---|---|---|
| 8 | `manual_sql_avanzado` (2.3) | El «RIGHT JOIN simulado con LEFT JOIN invertido» es **la misma consulta** que el LEFT JOIN anterior: no invierte nada | Se muestra la forma equivalente correcta (`clientes LEFT JOIN pedidos`) junto al `RIGHT JOIN` nativo |
| 9 | `manual_sql_avanzado` (2.4) | Dice que SQLite **no** soporta `RIGHT JOIN` ni `FULL JOIN`. Desde la **versión 3.39.0 (junio de 2022)** sí los soporta | El cuaderno comprueba la versión del entorno y muestra la forma nativa o la equivalente según corresponda. El `FULL JOIN` se ilustra comparando dos listas, donde sí se nota la diferencia |
| 10 | `manual_sql_avanzado` (D3-1 y 4.3) | **Empates sin desempate**: tres clientes empatan en S/ 500 y tres productos empatan en unidades. El resultado cambia según el motor | Se agregó desempate en el `ORDER BY` (`ORDER BY Monto_Total DESC, Cliente`) |
| 11 | `manual_sqlite` | Dice que el tipo `NUMERIC` guarda «números exactos (dinero, fechas)» con el ejemplo `2024-05-10`. SQLite **no tiene tipo fecha**: las fechas se guardan como `TEXT` | Tabla de tipos corregida, con la nota sobre fechas |
| 12 | `manual_sqlite`, `manual_modelado` | Describen las claves foráneas como si se respetaran siempre. En SQLite **vienen apagadas**: hace falta `PRAGMA foreign_keys = ON` (el manual de modelado lo menciona solo al final, y sin usarlo en el código) | La celda de preparación activa `PRAGMA foreign_keys = ON`, y se muestran los errores que SQLite devuelve al romper una relación |
| 13 | `manual_sqlite` | Dice que SQL «no tiene bucles ni funciones», lo cual es impreciso | Se explica que es un lenguaje **declarativo** (dices *qué* quieres, no *cómo*) |
| 14 | `manual_sqlite` | Mezcla niveles: en un manual «básico» entran `JOIN`, `GROUP BY` y `HAVING`, que el sílabo ubica en la semana 3 | Dividido en Básico (semana 2) e Intermedio (semana 3) |
| 15 | `manual_sqlite` | El resumen incluye `UPDATE`, `DELETE` y `DROP TABLE` pero ninguna celda los enseña | Se agregó una sección corta de `UPDATE` con verificación antes y después |
| 16 | `manual_modelado` (2.3) | Las cardinalidades del diagrama están como «N 1 N M»; deberían ser **1 N N M** (un cliente realiza muchos pedidos) | Diagrama redibujado y leído en voz alta debajo |
| 17 | `manual_modelado` (4.3) | En el ejemplo de 3FN se crea `empleados` con clave foránea a `ciudades` **antes** de crear `ciudades`, contra su propia regla «primero el padre» | `ciudades` se crea primero |
| 18 | `manual_modelado` (3.3 y 4.2) | `detalle_pedido` tiene `precio_unitario` en un ejemplo y no en el otro, sin explicar por qué | Se explica: el precio en el momento de la compra pertenece a la relación |
| 19 | `manual_modelado` (referencias) | Cita «SQLite Pocket Reference» de Jay A. Kreibich. **A verificar:** la obra de Kreibich que conozco es *Using SQLite* (O'Reilly, 2010) | Reemplazada por *Using SQLite*; confírmala antes de repartir la bibliografía |

### Detalles de presentación (en los PDF originales)

- Numeración de celdas inconsistente en `manual_sqlite` (3, 4, 5, 6, 7, 8, 9, **9b**, 10...).
- `manual_sql_avanzado_joins.pdf`: texto que se desborda en las tablas y `\n` escrito literalmente en la tabla de buenas prácticas. Hay tres versiones del mismo manual con diferencias (con y sin tildes, 13 y 25 páginas, y el PDF de 13 páginas corta los datos con «... 10 clientes en total», por lo que **no se puede reproducir**).
- `manual_modelado`: columna `#` demasiado ancha en la lista de entrega; el carácter ☐ aparece roto.
- `tabulate` puede no estar instalado en Colab: los cuadernos usan `pandas`, que viene incluido.

## Lo que sí estaba bien

Los datos de ejemplo (AynyTech y Lab D3), la lógica de `LEFT JOIN` frente a `INNER JOIN` (Marco Salas con 0 pedidos), la explicación de `WHERE` frente a `HAVING`, el orden correcto de las cláusulas y las reglas de normalización (1FN, 2FN y 3FN).

## Cómo están organizados los cuatro cuadernos

| Cuaderno | Semana del sílabo | Base de datos | Contenido | Ejercicios |
|---|---|---|---|---|
| `01_SQLite_Basico.ipynb` | 2 | AynyTech: `departamentos` (5), `empleados` (8) | `CREATE`, `INSERT`, `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`, `UPDATE` | 6 |
| `02_SQLite_Intermedio.ipynb` | 3 | AynyTech completa: 4 tablas (6, 8, 6 y 10 filas) | `INNER JOIN`, `LEFT JOIN`, `GROUP BY`, `HAVING`, `COUNT(DISTINCT)` | 5 |
| `03_SQLite_Avanzado.ipynb` | 3 (Lab D3) | `clientes` (10), `productos` (6), `pedidos` (15) | `RIGHT`/`FULL JOIN`, subconsultas, `CASE`, `UNION`, vistas, buenas prácticas, las 5 consultas del Lab D3 | 5 |
| `04_Modelado_Relacional_SQLite.ipynb` | 4 (Lab D4) | Varias bases pequeñas creadas durante el cuaderno | Modelo ER, cardinalidad 1:1 / 1:N / N:M, normalización, ER → SQLite, Lab D4 con ejemplo completo | 3 |

Cada cuaderno incluye los resultados ya ejecutados, así que se pueden leer en GitHub sin abrir Colab. Para trabajarlos: en Google Colab, **Archivo ▸ Abrir cuaderno ▸ GitHub** (o **Subir**), y **Entorno de ejecución ▸ Ejecutar todo**.
