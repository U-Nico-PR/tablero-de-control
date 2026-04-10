# Práctica del Modelo GQM
## Información general de la práctica
Esta práctica consistió en desarrollar un tablero de control utilizando tecnologías seleccionadas libremente. Para guiar el diseño se empleó el modelo de calidad GQM (Goal, Question, Metric), el cual permite definir el objetivo del problema a resolver —en este caso relacionado con throughput—, identificar preguntas clave y establecer métricas que ayudan a responderlas y cumplir el objetivo.

El tablero es interactivo y muestra métricas como Cycle Time, Tiempo de Resolución (MTTR) y Tasa de Entrega. Está organizado en varias secciones: en el panel derecho se encuentra la opción para cargar el archivo de entrada; debajo, al cargarlo, se habilita un filtrado de los módulos ingresados para las métricas; y en el área principal se presentan las métricas junto con gráficas interactivas que apoyan la toma de decisiones y el análisis de resultados.

# Tecnologías
- Python
- Streamlit
- Pandas
- Plotly

# Pasos para ejecución

> Esta práctica sse llevo a cabo en el Sistema Operativo Linux

1. Ejecutar el comando para el entorno virtual:
```python
python -m venv venv
```
2. Levantar el entorno virtual:
```python
source  venv/bin/activate
```
> Se mostrará ´(venv)´ al inicio de la ruta donde se encuentra.
> Es ***importante*** que la instrucción anterior se ejecute donde se encuentra el entorno virtual.

3. Instalar las bibliotecas necesarias para la ejecución del proyecto con el siguiente comando:
```python
pip install -r requeriments.txt
```
4. Ejecutar el proyecto. Se levantará una página web automáticamente gracias a Streamlit con el siguiente comando:
```python
streamlit run app.py
```
5.  Para terminar el proceso de Streamlit pulsar la combinación de teclas `Ctrl + c`.
6. Para desactivar el entorno virtual:
```python
deactivate
```
