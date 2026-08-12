# Analítica Empresarial Integrada — TECSUP 2026-I

Datos de los laboratorios del curso **Analítica Empresarial Integrada**
(Big Data y Ciencia de Datos · código C28).

**Docente:** Pilar Rocío Sayán Mejía

---

## Caso del curso: AgroAndes Export S.A.C.

Agroexportadora peruana con seis fundos en Ica, La Libertad, Lambayeque, Piura,
Áncash y Arequipa. Exporta arándano, uva de mesa, palta Hass, espárrago, mango y
granada a ocho mercados internacionales.

> Los datos son **sintéticos y de uso académico**. Reproducen relaciones plausibles
> del sector agroexportador peruano, pero no corresponden a ninguna empresa real ni
> contienen información personal de ninguna persona.

## Contenido

| Ruta | Archivo | Filas | Descripción |
|---|---|---|---|
| `semana01/datos/` | `embarques.csv` | 15 705 | Un registro por embarque, de enero 2022 a junio 2026 |
| `semana01/datos/` | `clientes.csv` | 72 | Clientes internacionales, país y canal |
| `semana01/datos/` | `productos.csv` | 20 | Catálogo de SKU, cultivo, variedad y calibre |
| `semana01/datos/` | `fundos.csv` | 6 | Fundos, UBIGEO del INEI, hectáreas y puerto |

### Detalles que importan al leer los archivos

- **`ubigeo` es texto, no número.** El código del INEI puede empezar en cero
  (Casma, Áncash, es `020801`). Léalo con `dtype={"ubigeo": str}` o perderá el cero.
- **`fecha` y `fecha_alta` son fechas.** Use `parse_dates` al leerlas.
- Los archivos conservan a propósito tres problemas de calidad que se trabajan en el
  laboratorio de la Semana 1: precios nulos, filas duplicadas y embarques con cero cajas.
  **No están corregidos**: encontrarlos es parte del ejercicio.

## Cómo cargar los datos desde Google Colab

```python
import pandas as pd

URL = ("https://raw.githubusercontent.com/Rociosayan/"
       "analitica-empresarial-integrada/main/semana01/datos")

embarques = pd.read_csv(f"{URL}/embarques.csv", parse_dates=["fecha"])
fundos    = pd.read_csv(f"{URL}/fundos.csv", dtype={"ubigeo": str})
productos = pd.read_csv(f"{URL}/productos.csv")
clientes  = pd.read_csv(f"{URL}/clientes.csv", parse_dates=["fecha_alta"])
```

## Licencia de uso

Material académico del curso. Puede reutilizarse con fines educativos citando la fuente.
