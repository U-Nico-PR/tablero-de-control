import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Métricas GQM", layout="wide")

st.sidebar.header("Configuración de Datos")

archivo = st.sidebar.file_uploader(
    "Sube tu reporte",
    type=["csv"],
    help="El archivo debe ser un CSV con formato UTF-8"
)

if archivo is not None:
    try:
        df = pd.read_csv(archivo)
        columnas_requeridas = ['fecha_entrada', 'fecha_termino', 'tipo', 'prioridad', 'modulo', 'estado']
        columnas_presentes = all(col in df.columns for col in columnas_requeridas)
        
        if columnas_presentes:
            df['fecha_entrada'] = pd.to_datetime(df['fecha_entrada'])
            df['fecha_termino'] = pd.to_datetime(df['fecha_termino'])
            df['duracion_horas'] = (df['fecha_termino'] - df['fecha_entrada']).dt.total_seconds() / 3600
            df['dias'] = (df['fecha_termino'] - df['fecha_entrada']).dt.days
            # Aquí va todo el cuerpo del dashboard
            
            st.title("Dashboard de Control de Calidad de Software")
            st.markdown("---")
            
            st.sidebar.header("Filtros del Proyecto")
            modulo_seleccionado = st.sidebar.multiselect(
                "Selecciona el Módulo",
                options=df["modulo"].unique(),
                default=df["modulo"].unique()
            )
            df_filtrado = df[df["modulo"].isin(modulo_seleccionado)]
            
            
            # Calculo de métricas
            # Para MTTR
            bugs_filtrados = df_filtrado[df_filtrado['tipo'] == 'Bug']
            if not bugs_filtrados.empty:
                bugs_cerrados = bugs_filtrados[bugs_filtrados['estado'] == 'Cerrado']
                total_de_bugs_cerrados = len(bugs_cerrados)
                if total_de_bugs_cerrados > 0:
                    total_horas_en_los_bugs = bugs_cerrados["duracion_horas"].sum()
                    mttr_actual = total_horas_en_los_bugs / total_de_bugs_cerrados
                else:
                    mttr_actual = 0.0
            else:
                mttr_actual = 0.0
                
            INDICADOR_MTTR = 5 # Resolver los bugs en menos de 5 horas MTTR <= 5 eficiente
            
            # Inferfaz de Usuario
            st.subheader("Indicadores Clave de Desempeño (KPIs)")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                delta_val = INDICADOR_MTTR - mttr_actual
                if delta_val >= 0:
                    delta_texto = f"{abs(delta_val):.1f} hrs debajo del límite"
                else:
                    delta_texto = f"-{abs(delta_val):.1f} hrs encima del límite"
                
                st.metric(
                    label="MTTR (Bugs)",
                    value=f"{mttr_actual:.1f} hrs",
                    delta=delta_texto,
                    delta_color="normal"
                )
            
            with col2:
                st.metric(
                    label="ítems de Trabajo",
                    value=f"{len(df_filtrado)}"
                )
            
            with col3:
                tareas_cerradas = df_filtrado[df_filtrado['estado'] == 'Cerrado']
                if not tareas_cerradas.empty:
                    # cycle_time_horas = tareas_cerradas['duracion_horas'].mean()
                    total_horas = tareas_cerradas['duracion_horas'].sum()
                    cycle_time_horas = total_horas/len(tareas_cerradas);
                    cycle_time_dias = cycle_time_horas / 24
                    st.metric(
                        label="Cycle Time Promedio",
                        value=f"{cycle_time_horas:.1f} Hrs",
                        delta=f"{cycle_time_dias:.0f} Días" # .1f para ver fracción de día
                    )
                else:
                    st.metric(label="Cycle Time Promedio", value="0 Hrs")
            
            with col4:
                total_tareas = len(df_filtrado)
                # Total de tareas cerradas
                tareas_cerradas = len(df_filtrado[df_filtrado['estado'] == 'Cerrado'])
                # Calcular tasa de entrega como porcentaje
                if total_tareas > 0:
                    tasa_entrega = (tareas_cerradas / total_tareas) * 100
                else:
                    tasa_entrega = 0.0
                st.metric(
                    label="Tasa de Entrega",
                    value=f"{tasa_entrega:.1f} %"
                )
            
            st.markdown("---")
            
            # Graficas
            st.subheader("Análisis por Módulo")
            col_izq, col_der = st.columns(2)
            
            with col_izq:
                st.markdown("**Distribución de Carga de Trabajo**")
                tareas_por_modulo = df_filtrado.groupby("modulo").size().reset_index(name="cantidad")
                st.bar_chart(
                    data=tareas_por_modulo,
                    x="modulo",
                    y="cantidad"
                )
                
            with col_der:
                st.markdown("**Prioridad de las tareas**")
                fig = px.pie(df_filtrado, names='prioridad', hole=0.3)
                st.plotly_chart(
                    fig,
                    width="stretch"
                )
            
            # Graficas extras
            st.markdown("---")
            st.header("Análisis Detallado de Operaciones")
            
            st.subheader("Eficiencia: Historis de Usuario vs Bugs")
            resumen_tipo = df_filtrado[df_filtrado['estado'] == 'Cerrado'].groupby('tipo').agg(
                tareas_finalizadas=('id', 'count'),
                tiempo_promedio_hrs=('duracion_horas', 'mean'),
                max_tiempo_hrs=('duracion_horas', 'max')
            ).reset_index()
            
            resumen_tipo['tiempo_promedio_hrs'] = resumen_tipo['tiempo_promedio_hrs'].map('{:.1f} hrs'.format)
            resumen_tipo['max_tiempo_hrs'] = resumen_tipo['max_tiempo_hrs'].map('{:.1f} hrs'.format)
            st.table(resumen_tipo)
            
            st.subheader("Seguimiento de Entregas en el Sprint")
            st.info("Eje x: Fecha de cierre | Eje Y: Días invertidos por tarea")
            
            entregas_df = df_filtrado[df_filtrado['estado'] == 'Cerrado'].copy()
            entregas_df['dias_totales'] = entregas_df['duracion_horas'] / 24
            
            fig_sprint = px.scatter(
                entregas_df,
                x='fecha_termino',
                y='dias_totales',
                color='tipo',
                size='duracion_horas',
                hover_data=['id', 'modulo', 'prioridad'],
                labels={'fecha_termino': 'Día del Sprint', 'dias_totales': 'Días para finalizar'},
                title="Dispersión de Etnrega (Cycle Time por Item)"
            )
            
            promedio_dias = entregas_df['dias_totales'].mean() if not entregas_df.empty else 0
            fig_sprint.add_hline(y=promedio_dias, line_dash="dot", annotation_text="Promedio", line_color="green")
            
            st.plotly_chart(fig_sprint, width='stretch')
            
            st.subheader("Deuda Técnica: Trabajo Pendiente")
            pendientes = df_filtrado[df_filtrado['estado'] != 'Cerrado']
            
            if not pendientes.empty:
                def color_prioridad(val):
                    color = 'red' if val == 'Alta' else 'orange' if val == 'Media' else 'white'
                    return f'color: {color}'

                st.dataframe(
                    pendientes[['id', 'modulo', 'tipo', 'prioridad', 'fecha_entrada']].style.map(color_prioridad, subset=['prioridad']),
                    width='stretch'
                )
            else:
                st.success("¡Excelente! No hay tareas pendientes en el módulo seleccionado.")
            # Mostrar la tabla de datos
            if st.checkbox("Ver datos en bruto."):
                st.write(df)
        else:
            st.error("Error de estructura: El CSV no tiene las columnas necesarias (fecha_entrada, fecha_termino, etc.).")
            st.info("Revisa que el archivo coincida con el formato del Modelo GQM definido.")
    except Exception as e:
        st.error(f"No se pudo procesar en el archivo: {e}")
else:
    st.info("Por favor, sube un archivo **CSV** para generar el Dashboard interactivo.")
    st.write("### Estructura esperada del CSV:")
    ejemplo = pd.DataFrame({
        'id': ['HU-01'], 'fecha_entrada': ['2024-01-01 10:00'],
        'fecha_termino': ['2024-01-01 12:00'], 'tipo': ['Bug'], 
        'prioridad': ['Alta'], 'modulo': ['Pagos'], 'estado': ['Cerrado']
    })
    st.table(ejemplo)

