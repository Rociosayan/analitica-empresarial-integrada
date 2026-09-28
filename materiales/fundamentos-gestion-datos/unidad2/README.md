# Fundamentos de Gestión de Datos — Unidad 2: Python para Datos, Limpieza y ML Básico

Material de estudio de la Unidad 2 (Semanas 5 a 8) · TECSUP 2026-II
**Docente:** Pilar Rocío Sayán Mejía

| Semana | Tema |
|---|---|
| 5 | Python y Pandas para Datos |
| 6 | Limpieza de Datos |
| 7 | ML Supervisado: Regresión y Clasificación |
| 8 | ML No Supervisado: Clustering (K-Means) |

Continúa el caso transversal **RutaMarket S.A.C.** (empresa *ficticia*) de la Unidad 1.

## Archivos

- `Unidad2_Fundamentos_Gestion_Datos_TECSUP_2026-II.docx` / `.pdf` — documento de estudio (25 páginas A4).
- `Unidad2_RutaMarket.ipynb` — notebook para Google Colab con todo el código de la unidad, en orden.
- `datos/rutamarket.db` — base SQLite **sintética** del caso (408 clientes, 3 004 pedidos de 2025).
  Contiene problemas de calidad **intencionales** (nulos ocultos, duplicados, tipos incorrectos, textos
  inconsistentes y errores de precio) que se trabajan en la Semana 6.
- `datos/productos.csv` — catálogo de productos, usado para practicar `pd.read_csv()`.
- `fuente/` — scripts que generan los datos (`generar_datos.py`), ejecutan el código (`snippets.py`, `runner.py`),
  producen las figuras (`figuras.py`) y el documento (`fmt.py`, `build_u2.py`).

## Uso en Colab

1. Abrir `Unidad2_RutaMarket.ipynb` en Google Colab.
2. Subir `datos/rutamarket.db` y `datos/productos.csv` al panel *Archivos*.
3. Ejecutar las celdas en orden. Los resultados coinciden con los del documento (pandas 2.x, scikit-learn).
