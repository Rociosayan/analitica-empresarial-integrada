# Fragmentos de código de la Unidad 2 (se ejecutan en orden, en un mismo espacio de nombres).
S = {}
S['s5_conexion'] = """import sqlite3
import pandas as pd

con = sqlite3.connect('rutamarket.db')
clientes = pd.read_sql_query('SELECT * FROM clientes', con)
print(clientes.shape)"""
S['s5_head'] = """clientes[['id_cliente', 'ciudad', 'edad', 'canal_registro', 'visitas_web_mes']].head()"""
S['s5_join'] = """consulta = '''
SELECT p.id_pedido, p.id_cliente, p.fecha_pedido, p.metodo_pago, p.estado,
       SUM(d.cantidad * d.precio_unitario) AS monto
FROM pedidos AS p
JOIN detalle_pedido AS d ON p.id_pedido = d.id_pedido
GROUP BY p.id_pedido;
'''
pedidos = pd.read_sql_query(consulta, con)
print(pedidos.shape)"""
S['s5_csv'] = """productos = pd.read_csv('productos.csv')
productos.head(3)"""
S['s5_series'] = """edades = clientes['edad']      # una columna: Series
print(type(clientes).__name__, type(edades).__name__)
print(edades.dtype)"""
S['s5_info'] = """clientes.info()"""
S['s5_describe'] = """pedidos['monto'].describe().round(2)"""
S['s5_vc'] = """clientes['ciudad'].value_counts(dropna=False)"""
S['s5_resumen'] = """resumen = (pedidos.groupby('id_cliente')
                  .agg(n_pedidos=('id_pedido', 'count'), gasto=('monto', 'sum'))
                  .reset_index()
                  .merge(clientes[['id_cliente', 'visitas_web_mes']],
                         on='id_cliente'))
resumen[['visitas_web_mes', 'n_pedidos', 'gasto']].corr().round(2)"""
# ---------------- Semana 6 ----------------
S['s6_nulos'] = """print(clientes.isnull().sum())
print('Pedidos sin método de pago:', pedidos['metodo_pago'].isnull().sum())"""
S['s6_tipos'] = """clientes['edad'] = pd.to_numeric(clientes['edad'], errors='coerce')
clientes['fecha_registro'] = pd.to_datetime(clientes['fecha_registro'])
print(clientes['edad'].dtype, clientes['edad'].isnull().sum())"""
S['s6_imposibles'] = """print(clientes['edad'].describe().round(1)[['min', 'max']])
clientes.loc[(clientes['edad'] < 18) | (clientes['edad'] > 100), 'edad'] = None"""
S['s6_texto'] = """clientes['ciudad'] = clientes['ciudad'].str.strip().str.title()
clientes['ciudad'].value_counts(dropna=False)"""
S['s6_dup_cli'] = """print('Clientes con email repetido:', clientes.duplicated(subset='email').sum())
clientes = clientes.drop_duplicates(subset='email', keep='first')
print(clientes.shape)"""
S['s6_dup_ped'] = """clave = ['id_cliente', 'fecha_pedido', 'monto', 'estado']
print('Pedidos duplicados:', pedidos.duplicated(subset=clave).sum())
pedidos = pedidos.drop_duplicates(subset=clave, keep='first')
print(pedidos.shape)"""
S['s6_imputar'] = """print('Media:', round(clientes['edad'].mean(), 1),
      '| Mediana:', clientes['edad'].median())
clientes['edad'] = clientes['edad'].fillna(clientes['edad'].median())
clientes['ciudad'] = clientes['ciudad'].fillna('No registrada')
moda_pago = pedidos['metodo_pago'].mode()[0]
pedidos['metodo_pago'] = pedidos['metodo_pago'].fillna(moda_pago)
print('Moda método de pago:', moda_pago)"""
S['s6_iqr'] = """q1, q3 = pedidos['monto'].quantile([0.25, 0.75])
iqr = q3 - q1
lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
atipicos_iqr = pedidos[(pedidos['monto'] < lim_inf) | (pedidos['monto'] > lim_sup)]
z = (pedidos['monto'] - pedidos['monto'].mean()) / pedidos['monto'].std()
print('Límite superior IQR:', round(lim_sup, 2))
print('Atípicos por IQR:', len(atipicos_iqr),
      '| por z-score (|z|>3):', (z.abs() > 3).sum())"""
S['s6_top'] = """pedidos.nlargest(8, 'monto')[['id_pedido', 'id_cliente', 'monto']]"""
S['s6_precio'] = """detalle = pd.read_sql_query('SELECT * FROM detalle_pedido', con)
catalogo = pd.read_sql_query('''SELECT id_producto, precio_unitario AS precio_catalogo
                                 FROM productos''', con)
detalle = detalle.merge(catalogo, on='id_producto')
errores = detalle[detalle['precio_unitario'] != detalle['precio_catalogo']]
print('Líneas con precio distinto al catálogo:', len(errores))
errores[['id_pedido', 'id_producto', 'precio_unitario', 'precio_catalogo']]"""
S['s6_corregir'] = """detalle['precio_unitario'] = detalle['precio_catalogo']
montos = (detalle.assign(subtotal=detalle['cantidad'] * detalle['precio_unitario'])
                 .groupby('id_pedido', as_index=False)['subtotal'].sum())
pedidos = (pedidos.drop(columns='monto')
                  .merge(montos, on='id_pedido')
                  .rename(columns={'subtotal': 'monto'}))
print(pedidos['monto'].describe().round(2)[['mean', '50%', 'max']])"""
S['s6_features'] = """pedidos['fecha_pedido'] = pd.to_datetime(pedidos['fecha_pedido'])
validos = pedidos[pedidos['estado'] == 'Entregado']
corte = pd.Timestamp('2025-12-31')
modelo = (validos.groupby('id_cliente')
          .agg(pedidos_2025=('id_pedido', 'count'),
               gasto_2025=('monto', 'sum'),
               ultima_compra=('fecha_pedido', 'max'))
          .reset_index())
modelo['ticket_promedio'] = (modelo['gasto_2025'] / modelo['pedidos_2025']).round(2)
modelo['dias_sin_comprar'] = (corte - modelo['ultima_compra']).dt.days
atributos = ['id_cliente', 'ciudad', 'edad', 'visitas_web_mes', 'fecha_registro']
modelo = modelo.merge(clientes[atributos], on='id_cliente')
dias = (corte - modelo['fecha_registro']).dt.days
modelo['antiguedad_meses'] = (dias / 30.4).round(1)
modelo = modelo.drop(columns=['ultima_compra', 'fecha_registro'])
print(modelo.shape)"""
S['s6_escalar'] = """from sklearn.preprocessing import MinMaxScaler, StandardScaler
cols = ['pedidos_2025', 'ticket_promedio']
minmax = MinMaxScaler().fit_transform(modelo[cols])
estandar = StandardScaler().fit_transform(modelo[cols])
print('Min-Max  -> mín:', minmax.min(axis=0).round(2),
      'máx:', minmax.max(axis=0).round(2))
print('Estándar -> media:', estandar.mean(axis=0).round(2),
      'desv.:', estandar.std(axis=0).round(2))"""
S['s6_guardar'] = """clientes.to_sql('clientes_limpio', con, if_exists='replace', index=False)
pedidos.to_sql('pedidos_limpio', con, if_exists='replace', index=False)
modelo.to_sql('clientes_modelo', con, if_exists='replace', index=False)
pd.read_sql_query('''SELECT COUNT(*) AS filas, ROUND(AVG(gasto_2025), 2) AS gasto_medio
                     FROM clientes_modelo''', con)"""
# ---------------- Semana 7 ----------------
S['s7_leer'] = """df = pd.read_sql_query('SELECT * FROM clientes_modelo', con)
columnas = ['visitas_web_mes', 'antiguedad_meses', 'edad', 'gasto_2025']
df[columnas].describe().round(1).loc[['mean', 'min', 'max']]"""
S['s7_split'] = """from sklearn.model_selection import train_test_split
X = df[['visitas_web_mes']]
y = df['gasto_2025']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)
print(len(X_train), 'clientes para entrenar |', len(X_test), 'para evaluar')"""
S['s7_simple'] = """from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
reg = LinearRegression().fit(X_train, y_train)
pred = reg.predict(X_test)
mse = mean_squared_error(y_test, pred)
print('Intercepto:', round(reg.intercept_, 2))
print('Coeficiente visitas_web_mes:', round(reg.coef_[0], 2))
print('R² (prueba):', round(r2_score(y_test, pred), 3))
print('MSE:', round(mse, 1), '| RMSE:', round(mse ** 0.5, 1))"""
S['s7_multiple'] = """variables = ['visitas_web_mes', 'antiguedad_meses', 'edad']
X_train, X_test, y_train, y_test = train_test_split(df[variables], y,
                                                    test_size=0.2, random_state=42)
reg2 = LinearRegression().fit(X_train, y_train)
pred2 = reg2.predict(X_test)
for v, c in zip(variables, reg2.coef_):
    print(f'{v:18s} {c:9.2f}')
print('R² (prueba):', round(r2_score(y_test, pred2), 3),
      '| RMSE:', round(mean_squared_error(y_test, pred2) ** 0.5, 1))"""
S['s7_overfit'] = """from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
muestra = df.sample(40, random_state=1)
Xa, Xb, ya, yb = train_test_split(muestra[['visitas_web_mes']], muestra['gasto_2025'],
                                  test_size=0.3, random_state=0)
for grado in [1, 3, 10]:
    m = make_pipeline(PolynomialFeatures(grado), StandardScaler(), LinearRegression())
    m.fit(Xa, ya)
    r2_ent = r2_score(ya, m.predict(Xa))
    r2_pru = r2_score(yb, m.predict(Xb))
    print(f'grado {grado:2d} | R² entrenamiento: {r2_ent:.2f} | R² prueba: {r2_pru:.2f}')"""
S['s7_clasif'] = """from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
umbral = df['gasto_2025'].quantile(0.75)
df['alto_valor'] = (df['gasto_2025'] >= umbral).astype(int)
Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    df[variables], df['alto_valor'], test_size=0.2,
    random_state=42, stratify=df['alto_valor'])
clf = LogisticRegression(max_iter=1000).fit(Xc_train, yc_train)
pred_c = clf.predict(Xc_test)
print('Umbral alto valor: S/', round(umbral, 2))
print('Exactitud (accuracy):', round(accuracy_score(yc_test, pred_c), 3))
print(confusion_matrix(yc_test, pred_c))"""
# ---------------- Semana 8 ----------------
S['s8_escalar'] = """from sklearn.cluster import KMeans
rfm = ['pedidos_2025', 'ticket_promedio', 'dias_sin_comprar']
X_esc = StandardScaler().fit_transform(df[rfm])
inercias = []
for k in range(1, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_esc)
    inercias.append(round(km.inertia_, 1))
print(inercias)"""
S['s8_kmeans'] = """km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X_esc)
df['cluster'] = km.labels_
print('Iteraciones hasta converger:', km.n_iter_)
perfil = df.groupby('cluster')[rfm + ['gasto_2025']].mean().round(1)
perfil['clientes'] = df['cluster'].value_counts().sort_index()
perfil"""
S['s8_nombrar'] = """nombres = {0: 'Regulares', 1: 'Inactivos', 2: 'Frecuentes',
           3: 'Compras grandes ocasionales'}
df['segmento'] = df['cluster'].map(nombres)
df['segmento'].value_counts()"""
S['s8_guardar'] = """df.to_sql('clientes_modelo', con, if_exists='replace', index=False)
pd.read_sql_query('''SELECT segmento, COUNT(*) AS clientes,
                            ROUND(SUM(gasto_2025), 2) AS gasto_total
                     FROM clientes_modelo
                     GROUP BY segmento
                     ORDER BY gasto_total DESC''', con)"""
