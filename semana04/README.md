# Semana 4 — Analítica diagnóstica: ¿por qué pasó?

Datos del **Laboratorio Dirigido N.° 04** del curso Analítica Empresarial Integrada
(TECSUP, 2026-II). A diferencia de la Semana 1, aquí no se trabaja con datos
sintéticos: el conjunto es real, público y verificable.

## Ficha de trazabilidad

| Campo | Valor |
|---|---|
| Nombre | Online Retail II |
| Repositorio de origen | UCI Machine Learning Repository, conjunto n.° 502 |
| Enlace | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| Descarga directa | https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip |
| Donante | Dr. Daqing Chen, London South Bank University |
| Licencia | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Periodo cubierto | 1 de diciembre de 2009 a 9 de diciembre de 2011 |
| Registros | 1 067 371 |
| Columnas | 8 |
| SHA-256 del ZIP original | `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` |
| SHA-256 del Parquet publicado | `8f64c20d17d38ab02c0dfddda323574e0ee8c34e719df6ea574d16a6e3678e96` |

## Qué contiene la carpeta

| Archivo | Descripción |
|---|---|
| `datos/online_retail_II.parquet` | Copia íntegra del archivo de UCI en formato Parquet (7.3 MB) |
| `conversion_uci_a_parquet.py` | Script que reproduce esa conversión desde el origen |

## Por qué Parquet y no el archivo original

UCI publica el conjunto como un único archivo `.xlsx` de 45 MB. Leerlo con
`openpyxl` toma alrededor de cien segundos, tiempo que no cabe dentro de un
bloque de laboratorio. La copia en Parquet se lee en pocos segundos y conserva
las mismas 1 067 371 filas y los mismos valores.

La única diferencia es de tipo de dato: `Invoice`, `StockCode`, `Description` y
`Country` se almacenan como texto, porque algunos códigos de factura combinan
letras y dígitos —por ejemplo `C489449`, que corresponde a una cancelación— y
una lectura automática los interpretaría de forma inconsistente.

Quien desee comprobarlo puede ejecutar `conversion_uci_a_parquet.py`: descarga
el archivo desde UCI, verifica su SHA-256 y regenera el Parquet publicado.

## Descripción de las columnas

| Columna | Contenido |
|---|---|
| `Invoice` | Número de factura. Si empieza con `C`, la operación es una cancelación |
| `StockCode` | Código del producto. Algunos códigos no son productos, sino servicios o ajustes |
| `Description` | Nombre del producto |
| `Quantity` | Unidades de la línea. Puede ser negativa en devoluciones |
| `InvoiceDate` | Fecha y hora de la transacción |
| `Price` | Precio unitario en libras esterlinas |
| `Customer ID` | Identificador del cliente. Está vacío en aproximadamente el 23 % de las líneas |
| `Country` | País de residencia del cliente |

## Uso desde Google Colab

```python
import polars as pl

URL = ("https://raw.githubusercontent.com/Rociosayan/"
       "analitica-empresarial-integrada/main/semana04/datos/online_retail_II.parquet")
crudo = pl.read_parquet(URL)
```

## Cita

Chen, D. (2019). *Online Retail II* [conjunto de datos]. UCI Machine Learning
Repository. https://doi.org/10.24432/C5CG6D
