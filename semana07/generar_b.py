"""Serie B de modelos de sustentación (Semana 7): 3 casos nuevos.

Fase 1 (esta versión): hoja del ESTUDIANTE, sin soluciones.
Los números salen de calculos_b.py (verificados con un segundo método).
Uso:  python generar_b.py
"""
from pathlib import Path

import calculos_b as B
from generar_modelos import AQUI, SALIDA, Modelo, s

SUBTITULO = "Semana 7 · Serie B · Teoría de colas y Teoría de decisión"


def caso1(m):
    c = B.B1
    r = B.caso1()
    hm = r["horas_mes"]
    m.caso(1, "Atención en ventanillas de CAJA RURAL SOL DEL NORTE", "Teoría de colas")
    m.enunciado("CAJA RURAL SOL DEL NORTE es una entidad financiera peruana que atiende a sus "
                "clientes en las ventanillas de una de sus agencias. Cuando un cliente llega, se "
                "incorpora a una fila única hasta que un cajero esté disponible. A un cajero le "
                f"toma, en promedio, {c['servicio_min']} minutos atender a un cliente, con "
                "tiempos que se ajustan a una distribución exponencial. Asimismo, se ha "
                f"estimado que en promedio llegan a la agencia {c['clientes']} clientes cada "
                f"{c['cada_min']} minutos, siguiendo una distribución de Poisson.")
    m.enunciado("Los cajeros trabajan un solo turno diario de 8:00 a. m. a 4:00 p. m., de lunes "
                f"a sábado, {c['sem_mes']} semanas al mes, y tienen una remuneración de "
                f"{c['sueldo_dia']} soles diarios. Los costos del sistema de caja (terminal y "
                f"licencias) son de {c['sistema_sem']} soles semanales por cajero. Asimismo, se "
                "estima que por cada cliente que permanece en la fila se incurre en un costo de "
                f"oportunidad de {c['costo_espera_h']} soles por hora.")
    m.enunciado("Actualmente, la entidad trabaja con el número mínimo de cajeros que le garantiza "
                "poder atender a todos los clientes que llegan; sin embargo, en las últimas "
                "semanas ha recibido numerosos reclamos por las largas filas, por lo que se "
                "desea evaluar la conveniencia de contratar a un cajero adicional. Esta "
                "propuesta debe estar sustentada en lo siguiente:")
    m.vineta(f"El cliente no debe esperar en la fila más de {c['wq_max_min']} minutos por la "
             "atención del cajero.")
    m.vineta("El costo total del servicio debe ser menor.")
    m.enunciado("Las tasas de llegada y de atención deben expresarse en clientes/hora.",
                italica=True)

    m.pregunta("¿Cuál es la situación problemática? (Debe incluir el problema a resolver, las "
               "distintas propuestas y el objetivo)", "INTERPRETACIÓN")
    m.pregunta("¿Cómo representaría los modelos a comparar y las metas que debe alcanzar?",
               "REPRESENTACIÓN")
    m.pregunta("¿Qué cálculos debe obtener para evaluar las metas? (Debe ser presentado en un "
               "cuadro y presentar un gráfico que explique el comportamiento de los costos)",
               "CÁLCULO", espacio=8)
    filas = [["Medida", f"s = {c['s_actual']} (actual)", f"s = {c['s_propuesta']} (propuesta)"],
             ["λ (clientes/hora)", "", ""],
             ["μ por cajero (clientes/hora)", "", ""],
             ["ρ = λ / (s·μ)", "", ""],
             ["P0 (prob. sistema vacío)", "", ""],
             ["P(espera) – Erlang C", "", ""],
             ["Wq (minutos)", "", ""],
             ["Lq (clientes en espera)", "", ""],
             ["Costo fijo mensual (planilla + sistema)", "", ""],
             [f"Costo de espera mensual ({c['costo_espera_h']} soles/h × Lq × {hm} h/mes)",
              "", ""],
             ["Costo total mensual", "", ""]]
    m.tabla(filas, [3489, 3489, 3489])
    m.pregunta("¿Qué propuesta es la mejor? Realice una discusión de resultados para argumentar "
               "su decisión.", "ANÁLISIS Y ARGUMENTACIÓN")


def caso2(m):
    c = B.B2
    cv, og = c["conv"], c["org"]
    q = 1 - c["p_alto"]
    m.doc.vacio()
    m.caso(2, "Decisión de certificación orgánica en la finca cafetalera “La Selva Alta”",
           "Teoría de decisión – valor esperado, un nivel")
    m.enunciado("Carmen Huamán, dueña de la finca cafetalera “La Selva Alta”, debe decidir cómo "
                "orientar su producción para la próxima campaña: mantener únicamente su café "
                "convencional o certificar una parcela como café orgánico de especialidad, con "
                "el objetivo de maximizar su utilidad neta. El resultado dependerá del precio de "
                "mercado, que se prevé en dos escenarios: precio alto por demanda de cafés "
                "especiales o precio estándar.")
    m.enunciado(f"Si opta por mantener solo el café convencional, sus costos serán de "
                f"{s(cv['costo'])}; si el precio es alto obtendría ingresos por "
                f"{s(cv['ing_alto'])}, mientras que si el precio es estándar obtendría ingresos "
                f"por {s(cv['ing_est'])}.")
    m.enunciado(f"Si opta por certificar el café orgánico, sus costos serán de {s(og['costo'])}; "
                f"si el precio es alto obtendría ingresos por {s(og['ing_alto'])}, mientras que "
                f"si el precio es estándar, dichos ingresos se reducirían en un "
                f"{og['caida']*100:.0f}%. Además, ha estimado que la probabilidad de un precio "
                f"alto es de {c['p_alto']:.2f}.")
    m.pregunta("¿Cuál es la situación problemática, qué problema hay que resolver y con qué "
               "finalidad?", "INTERPRETACIÓN")
    m.pregunta("¿Qué herramienta se utilizaría para resolver el problema? Presente los "
               "elementos, muestre el desarrollo de los cálculos necesarios para hallar los "
               "pagos y aplicar el criterio del valor esperado.", "REPRESENTACIÓN y CÁLCULO",
               espacio=12)
    filas = [["Alternativa", "Escenario", "Ingreso", "Costo", "Pago (utilidad)"],
             ["Café convencional", f"Precio alto (P = {c['p_alto']:.2f})", "", "", ""],
             ["Café convencional", f"Precio estándar (P = {q:.2f})", "", "", ""],
             ["Café orgánico", f"Precio alto (P = {c['p_alto']:.2f})", "", "", ""],
             ["Café orgánico", f"Precio estándar (P = {q:.2f})", "", "", ""]]
    m.tabla(filas, [2013, 1988, 1955, 1916, 1983])
    m.pregunta("¿Cuál es la mejor decisión? Realice una discusión de resultados para argumentar "
               "su elección.", "ANÁLISIS Y ARGUMENTACIÓN")


def caso3(m):
    c = B.B3
    q = 1 - c["p_alta"]
    m.doc.vacio()
    m.caso(3, "Estrategia de expansión de la empresa de transporte “Rutas del Sur”",
           "Teoría de decisión – árbol con recurso, dos niveles")
    m.enunciado("Una empresa de transporte evalúa si continuar operando únicamente con su "
                f"servicio de carga seca, obteniendo una utilidad anual segura de "
                f"{s(c['seguro'])}, o lanzar una nueva línea de transporte refrigerado, para lo "
                "cual deberá asumir costos iniciales de flota y certificaciones por "
                f"{s(c['costo_ini'])}. Las ganancias y pérdidas que se indican a continuación no "
                "incluyen este costo inicial ni la inversión adicional que se menciona más "
                "adelante.")
    m.enunciado(f"Si decide lanzar la nueva línea, existe una probabilidad de "
                f"{c['p_alta']*100:.0f}% de lograr una alta aceptación entre los clientes, "
                f"generando una ganancia de {s(c['g_alta'])}. Sin embargo, existe una "
                f"probabilidad de {q*100:.0f}% de no alcanzar la aceptación esperada, situación "
                "en la que deberá decidir entre reorientar el servicio hacia nuevos clientes, "
                f"lo que requiere una inversión adicional de {s(c['inv_extra'])}, o vender los "
                "camiones refrigerados.")
    m.enunciado(f"Si decide reorientar el servicio, el mercado podría responder "
                f"favorablemente, con una probabilidad de {c['p_fav']*100:.0f}%, generando una "
                f"utilidad de {s(c['u_fav'])}, o desfavorablemente, con una probabilidad de "
                f"{(1-c['p_fav'])*100:.0f}%, generando una utilidad de {s(c['u_des'])}.")
    m.enunciado("Si decide vender los camiones refrigerados, luego de cubrir los gastos de "
                f"traspaso, obtendría un ingreso neto de {s(c['venta'])}.")
    m.pregunta("Construya el árbol de decisión con todos sus elementos.", "REPRESENTACIÓN",
               espacio=16)
    m.pregunta("Desarrolle el criterio del valor esperado realizando los cálculos necesarios y "
               "tome la decisión que corresponda en cada nodo.", "CÁLCULO", espacio=12)
    m.pregunta("¿Qué posibles estrategias se pueden seguir a partir del árbol construido?",
               "INTERPRETACIÓN")
    m.pregunta("¿Cuál es la mejor estrategia? Sustente su respuesta.", "ANÁLISIS Y ARGUMENTACIÓN")


def generar_estudiante():
    plantilla = AQUI / "plantillas" / "Modelo_de_Sustentacion_2_ESTUDIANTE.docx"
    m = Modelo(False, plantilla)
    m.titulo(SUBTITULO)
    caso1(m); caso2(m); caso3(m)
    m.fin()
    m.doc.d.core_properties.title = "Sustentación Semana 7 – Serie B – Hoja del estudiante"
    ruta = SALIDA / "Hoja_de_Sustentacion_Semana7_SerieB_ESTUDIANTE.docx"
    m.doc.guardar(ruta)
    return ruta


if __name__ == "__main__":
    print("generado:", generar_estudiante())
