# core/ml_model.py
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Entrenamiento simulado: puedes reemplazarlo con tus datos reales/simulados
def entrenar_modelo():
    from sklearn.model_selection import train_test_split

    # Dataset de ejemplo (sustituye esto con tus datos históricos reales/simulados)
    datos = np.array([
        [14, 90, 2.5, 13.5],
        [16, 95, 4.2, 15.8],
        [12, 70, 2.1, 11.0],
        [10, 60, 1.8, 9.5],
        [18, 100, 4.5, 17.9]
    ])
    
    X = datos[:, :3]  # notas, asistencia, participacion
    y = datos[:, 3]   # rendimiento futuro

    model = RandomForestRegressor()
    model.fit(X, y)
    return model

# Clasificación: bajo / medio / alto
def clasificar_rendimiento(valor):
    if valor < 11:
        return "bajo"
    elif valor < 15:
        return "medio"
    else:
        return "alto"

# Ejecutar predicción
modelo_rf = entrenar_modelo()

def predecir_rendimiento(promedio_notas, asistencia, participacion):
    entrada = np.array([[promedio_notas, asistencia, participacion]])
    prediccion = modelo_rf.predict(entrada)[0]
    clasificacion = clasificar_rendimiento(prediccion)
    return prediccion, clasificacion
