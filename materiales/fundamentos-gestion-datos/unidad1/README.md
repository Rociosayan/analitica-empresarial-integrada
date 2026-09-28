# Fundamentos de Gestión de Datos — Unidad 1: Fundamentos del Dato y SQL

Material de estudio de la Unidad 1 (Semanas 1 a 4) · TECSUP 2026-II
**Docente:** Pilar Rocío Sayán Mejía

| Semana | Tema |
|---|---|
| 1 | El Dato y la Gestión de Datos |
| 2 | SQLite Básico: Consultas y Filtros |
| 3 | SQL Avanzado: JOINs y Agrupaciones |
| 4 | Modelado Relacional |

Caso transversal: **RutaMarket S.A.C.**, empresa de comercio electrónico *ficticia*.

## Archivos

- `Unidad1_Fundamentos_Gestion_Datos_TECSUP_2026-II.docx` — documento editable (27 páginas A4).
- `Unidad1_Fundamentos_Gestion_Datos_TECSUP_2026-II.pdf` — versión para distribuir.
- `fuente/` — scripts que generan el documento:
  - `caso.py`: base de datos SQLite del caso (clientes, categorías, productos, pedidos, detalle_pedido y la tabla `ventas`).
  - `queries.py`: todas las consultas SQL del material. Los "resultados esperados" del documento se obtienen ejecutándolas.
  - `diagramas.py`: figuras (DIKW, ciclo de vida, modelo relacional).
  - `fmt.py`, `build.py`: formato y contenido del documento.

## Regenerar

```bash
pip install python-docx matplotlib
cd fuente
python diagramas.py
python build.py Unidad1.docx
```
