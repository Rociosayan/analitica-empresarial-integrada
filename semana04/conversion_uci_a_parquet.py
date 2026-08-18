# -*- coding: utf-8 -*-
"""
Conversión del archivo original de UCI a Parquet.

El repositorio de UCI publica el conjunto «Online Retail II» como un único
archivo .xlsx de 45 MB comprimido en ZIP. Leerlo con openpyxl toma alrededor
de cien segundos, tiempo que no resulta razonable dentro de una sesión de
laboratorio. Por esa razón se publica aquí una copia en formato Parquet, que
se lee en pocos segundos.

La conversión no altera los datos: se conservan las 1 067 371 filas, las ocho
columnas y sus valores originales. El único cambio es de tipo de dato: las
columnas Invoice, StockCode, Description y Country se fuerzan a texto, porque
algunos códigos de factura combinan letras y dígitos (por ejemplo, C489449) y
una lectura automática los interpretaría de forma inconsistente.

Para reproducir el archivo publicado, ejecute este script tal como está.
"""
import hashlib
import zipfile
from pathlib import Path

import pandas as pd
import requests

URL_UCI = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
SHA256_ESPERADO = "572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb"

destino = Path("online_retail_II.zip")
destino.write_bytes(requests.get(URL_UCI, timeout=600).content)

obtenido = hashlib.sha256(destino.read_bytes()).hexdigest()
if obtenido != SHA256_ESPERADO:
    raise SystemExit(f"El archivo descargado no coincide con el original: {obtenido}")

with zipfile.ZipFile(destino).open("online_retail_II.xlsx") as f:
    libro = pd.ExcelFile(f, engine="openpyxl")
    datos = pd.concat([libro.parse(h) for h in libro.sheet_names], ignore_index=True)

for columna in ["Invoice", "StockCode", "Description", "Country"]:
    datos[columna] = datos[columna].astype(str)

datos.to_parquet("online_retail_II.parquet", index=False)
print(f"Filas: {len(datos):,}  Columnas: {len(datos.columns)}")
