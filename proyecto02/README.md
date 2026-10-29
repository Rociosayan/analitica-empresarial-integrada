# Proyecto Integrador 2 (PMD2) · LC8

Analítica Empresarial Integrada · TECSUP · 2026-II · Docente: Pilar Rocío Sayán Mejía

El proyecto acumula el trabajo de las **semanas 9 a 15** y se sustenta en la **semana 16**.

## Documentos

| Archivo | Para qué sirve |
|---|---|
| `PMD2_AEI_Casos_2026II.docx` | Los cinco casos, la ruta semana por semana, el contrato de datos y las reglas de cada escenario. **Empiece por aquí.** |
| `PMD2_AEI_Rubrica_2026II.docx` | Con qué se califica el Colab, el informe gerencial y la sustentación. |
| `PMD2_AEI_Caso_Ejemplo_2026II.docx` | Caso resuelto de referencia (Patitas Andinas). Ningún grupo lo desarrolla. |

## Código de arranque: un encabezado por caso

Cada encabezado lee las ocho tablas de su caso, **estructura la base de datos en DuckDB**, corre diez controles de recepción y guarda la base en un archivo para la semana 14. Es lo primero que se ejecuta en la semana 9.

| Grupo | Abrir en Colab | Archivo |
|---|---|---|
| 1 · AndeHogar | [Abrir](https://colab.research.google.com/github/Rociosayan/analitica-empresarial-integrada/blob/main/proyecto02/ENCABEZADO-PMD2-G1-ANDEHOGAR.ipynb) | `ENCABEZADO-PMD2-G1-ANDEHOGAR.ipynb` |
| 2 · Café de Origen | [Abrir](https://colab.research.google.com/github/Rociosayan/analitica-empresarial-integrada/blob/main/proyecto02/ENCABEZADO-PMD2-G2-CAFE-DE-ORIGEN.ipynb) | `ENCABEZADO-PMD2-G2-CAFE-DE-ORIGEN.ipynb` |
| 3 · VitalFit | [Abrir](https://colab.research.google.com/github/Rociosayan/analitica-empresarial-integrada/blob/main/proyecto02/ENCABEZADO-PMD2-G3-VITALFIT.ipynb) | `ENCABEZADO-PMD2-G3-VITALFIT.ipynb` |
| 4 · Suministros Sur | [Abrir](https://colab.research.google.com/github/Rociosayan/analitica-empresarial-integrada/blob/main/proyecto02/ENCABEZADO-PMD2-G4-SUMINISTROS-SUR.ipynb) | `ENCABEZADO-PMD2-G4-SUMINISTROS-SUR.ipynb` |
| 5 · AulaActiva | [Abrir](https://colab.research.google.com/github/Rociosayan/analitica-empresarial-integrada/blob/main/proyecto02/ENCABEZADO-PMD2-G5-AULAACTIVA.ipynb) | `ENCABEZADO-PMD2-G5-AULAACTIVA.ipynb` |

Abra el encabezado de su grupo, cambie `USUARIO` por su usuario de GitHub después del *fork* y ejecútelo completo. Si los diez controles salen en verde, los datos están listos y puede empezar el trabajo de la semana 9.

## Dónde están los datos

Los datos **no están en este repositorio**. Están en el repositorio del proyecto:

**https://github.com/Rociosayan/pmd2-aei-2026ii**

Cada grupo hace un *fork* de ese repositorio, trabaja dentro de la carpeta de su caso y entrega el enlace de su fork. El encabezado lee los CSV por URL, así que no hace falta descargar nada.

| Grupo | Carpeta del caso | Empresa |
|---|---|---|
| 1 | `casos/caso1_andehogar` | AndeHogar |
| 2 | `casos/caso2_cafe_de_origen` | Café de Origen |
| 3 | `casos/caso3_vitalfit` | VitalFit |
| 4 | `casos/caso4_suministros_sur` | Suministros Sur |
| 5 | `casos/caso5_aulaactiva` | AulaActiva |
