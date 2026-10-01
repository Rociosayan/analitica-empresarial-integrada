# Semana 7 — Modelos de sustentación (Teoría de colas y Teoría de decisión)

Tres casos nuevos con el mismo formato del modelo anterior (Caso 1: colas M/M/s ·
Caso 2: árbol de decisión de un nivel · Caso 3: árbol con recurso de dos niveles),
en versión **DOCENTE** (solucionario con rúbrica, «Respuesta», «¿Por qué se resuelve así?» y el detalle paso a paso de cada porcentaje) y **ESTUDIANTE** (hoja en blanco: enunciados, preguntas y espacio para responder, sin soluciones).

| Archivo | Contenido |
|---|---|
| `modelos/Modelo_de_Sustentacion_Semana7_DOCENTE.docx` | Solucionario docente |
| `modelos/Hoja_de_Sustentacion_Semana7_ESTUDIANTE.docx` | Hoja del estudiante, sin soluciones |
| `calculos.py` | Todos los números de los tres casos, cada uno verificado con un segundo método |
| `figuras.py` | Gráfico de costos y árboles de decisión |
| `generar_modelos.py` | Genera los dos `.docx` a partir de `plantillas/` y `calculos.py` |

```bash
pip install python-docx matplotlib
python calculos.py          # imprime resultados y ejecuta las verificaciones cruzadas
python generar_modelos.py   # regenera figuras/ y modelos/
```

## Resultados (resumen)

| Caso | Decisión | Cifras clave |
|---|---|---|
| 1 · Clínica Valle Sur (M/M/s) | Contratar 5.º operador | Wq 8.95 → 1.92 min (meta ≤ 6); costo S/ 22,743 → S/ 18,552 (ahorro S/ 4,191) |
| 2 · Sabores del Sur (VE) | Mantener carta criolla | VE S/ 53,500 vs S/ 42,275 (dif. S/ 11,225); equilibrio P(alta) ≈ 0.83 |
| 3 · Huellitas (árbol con recurso) | Lanzar telemedicina + campaña de descuentos | VE neto S/ 156,000 vs S/ 140,000 seguro; sin recurso valdría S/ 96,000 |

Correcciones respecto del modelo anterior (Sustentación 2): se eliminaron las inconsistencias
(VE con pago equivocado, diferencia «S/ 11,000» en vez de S/ 6,500, árbol del Caso 2 con
valores que no coincidían con la tabla) y el enunciado del Caso 3 aclara que el costo
inicial no está incluido en las ganancias, para que no haya doble lectura.
