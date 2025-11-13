rimport streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="NEXUS Audit Suite",
    page_icon="🔍",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #ff4b4b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    .risk-medium {
        background-color: #ffa500;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    .risk-low {
        background-color: #00cc96;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    .module-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class NexusAuditSuite:
    def __init__(self):
        self.sistema_actual = {}
        
    def header(self):
        st.markdown('<div class="main-header">🔍 NEXUS AUDIT SUITE</div>', unsafe_allow_html=True)
        st.markdown("**Tu asistente para auditoría ética de sistemas autónomos**")
        
    def sidebar(self):
        st.sidebar.title("Navegación")
        modulo = st.sidebar.radio(
            "Selecciona el módulo:",
            ["🏠 Dashboard", "🤖 Autonomía", "💎 Valores", "⚖️ Sesgos", "📊 Informes"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **Cómo usar:**
        1. Completa cada módulo
        2. Sube datos si dispones
        3. Genera informes automáticos
        """)
        
        return modulo
    
    def dashboard(self):
        st.header("📊 Dashboard Principal")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sistemas Auditados", "3", "1 esta semana")
        with col2:
            st.metric("Riesgo Promedio", "Medio", "-2% vs mes pasado")
        with col3:
            st.metric("Recomendaciones", "12", "3 críticas")
        
        # Progreso de auditorías
        st.subheader("Progreso de Auditoría Actual")
        
        if 'autonomia_score' not in st.session_state:
            st.session_state.autonomia_score = 0
        if 'valores_score' not in st.session_state:
            st.session_state.valores_score = 0
        if 'sesgos_score' not in st.session_state:
            st.session_state.sesgos_score = 0
            
        progreso_data = {
            'Módulo': ['Autonomía', 'Valores', 'Sesgos'],
            'Completado': [
                st.session_state.autonomia_score,
                st.session_state.valores_score, 
                st.session_state.sesgos_score
            ]
        }
        
        fig = px.bar(progreso_data, x='Módulo', y='Completado',
                     title="Progreso de la Auditoría",
                     color='Completado',
                     color_continuous_scale=['red', 'orange', 'green'])
        st.plotly_chart(fig, use_container_width=True)
        
    def modulo_autonomia(self):
        st.header("🤖 Evaluación de Autonomía")
        
        with st.form("autonomia_form"):
            st.subheader("Clasificación del Sistema")
            
            nombre_sistema = st.text_input("Nombre del sistema:", placeholder="Ej: Asistente Contratación IA")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Nivel de Autonomía**")
                nivel = st.radio(
                    "Selecciona el nivel:",
                    [1, 2, 3],
                    format_func=lambda x: {
                        1: "Nivel 1: Asistente (Sugiere)",
                        2: "Nivel 2: Colaborador (Actúa bajo supervisión)", 
                        3: "Nivel 3: Actor (Decide autónomamente)"
                    }[x]
                )
                
            with col2:
                st.markdown("**Capacidades**")
                puede_aprender = st.checkbox("Puede aprender/modificar comportamiento")
                actua_solo = st.checkbox("Puede actuar sin supervisión inmediata")
                toma_decisiones = st.checkbox("Toma decisiones estratégicas")
            
            st.markdown("---")
            st.subheader("Evaluación C4 - Control Humano")
            
            comprension = st.slider("🧠 Comprensión - ¿Los operadores entienden el sistema?", 1, 5, 3)
            capacidad = st.slider("🛑 Capacidad - ¿Pueden intervenir efectivamente?", 1, 5, 3) 
            contexto = st.slider("🌍 Contexto - ¿El sistema tiene información suficiente?", 1, 5, 3)
            consecuencia = st.slider("⚖️ Consecuencia - ¿Hay responsables claros?", 1, 5, 3)
            
            submitted = st.form_submit_button("Calcular Evaluación")
            
            if submitted:
                # Cálculo de scores
                score_c4 = (comprension + capacidad + contexto + consecuencia) / 4
                riesgo_autonomia = (nivel * 2) - score_c4
                
                st.session_state.autonomia_score = 100
                st.session_state.nivel_autonomia = nivel
                st.session_state.riesgo_autonomia = riesgo_autonomia
                st.session_state.score_c4 = score_c4
                
                # Mostrar resultados
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Nivel Autonomía", nivel)
                with col2:
                    st.metric("Score Control Humano", f"{score_c4:.1f}/5")
                with col3:
                    st.metric("Riesgo Calculado", f"{riesgo_autonomia:.1f}/5")
                
                # Recomendaciones
                st.subheader("🔍 Recomendaciones")
                
                if riesgo_autonomia >= 4:
                    st.error("""
                    **🚨 ACCIÓN INMEDIATA REQUERIDA**
                    - Revisar mecanismos de control humano
                    - Establecer responsables claros
                    - Considerar reducir nivel de autonomía
                    """)
                elif riesgo_autonomia >= 2.5:
                    st.warning("""
                    **⚠️ MEJORAS RECOMENDADAS**
                    - Fortalecer supervisión humana
                    - Mejorar documentación y formación
                    - Establecer protocolos de emergencia
                    """)
                else:
                    st.success("""
                    **✅ DENTRO DE PARÁMETROS ACEPTABLES**
                    - Mantener controles actuales
                    - Monitorizar periódicamente
                    """)
    
    def modulo_valores(self):
        st.header("💎 Diseño Centrado en Valores")
        
        st.info("Identifica y prioriza los valores humanos que el sistema debe respetar")
        
        with st.form("valores_form"):
            # Stakeholders y valores
            st.subheader("1. Identificación de Stakeholders")
            
            stakeholders = st.multiselect(
                "Selecciona los grupos de interés:",
                ["Usuarios finales", "Empleados", "Clientes", "Comunidad local", 
                 "Reguladores", "Inversores", "Grupos vulnerables", "Futuras generaciones"]
            )
            
            st.subheader("2. Priorización de Valores")
            st.markdown("**Distribuye 100 puntos entre los valores:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                equidad = st.slider("Equidad/Justicia", 0, 100, 25)
                transparencia = st.slider("Transparencia", 0, 100, 20)
                privacidad = st.slider("Privacidad", 0, 100, 15)
                
            with col2:
                autonomia = st.slider("Autonomía humana", 0, 100, 15)
                seguridad = st.slider("Seguridad", 0, 100, 15)
                sostenibilidad = st.slider("Sostenibilidad", 0, 100, 10)
            
            total = equidad + transparencia + privacidad + autonomia + seguridad + sostenibilidad
            
            if total != 100:
                st.warning(f"Total: {total}/100 puntos - Ajusta para sumar 100")
            else:
                st.success(f"✅ Total: {100}/100 puntos")
            
            st.subheader("3. Especificaciones Técnicas")
            
            valor_principal = st.selectbox("Selecciona valor para especificar:", 
                                         ["Equidad", "Transparencia", "Privacidad"])
            
            especificacion = st.text_area(
                f"Especificación técnica para {valor_principal}:",
                placeholder=f"Ej: Para '{valor_principal}' implementaremos...",
                height=100
            )
            
            submitted = st.form_submit_button("Guardar Análisis de Valores")
            
            if submitted and total == 100:
                st.session_state.valores_score = 100
                st.session_state.valores_priorizados = {
                    'Equidad': equidad,
                    'Transparencia': transparencia, 
                    'Privacidad': privacidad,
                    'Autonomía': autonomia,
                    'Seguridad': seguridad,
                    'Sostenibilidad': sostenibilidad
                }
                
                # Visualización
                fig = px.pie(
                    values=[equidad, transparencia, privacidad, autonomia, seguridad, sostenibilidad],
                    names=['Equidad', 'Transparencia', 'Privacidad', 'Autonomía', 'Seguridad', 'Sostenibilidad'],
                    title="Priorización de Valores"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.success("✅ Análisis de valores guardado correctamente")
    
    def modulo_sesgos(self):
        st.header("⚖️ Detección de Sesgos Algorítmicos")
        
        tab1, tab2, tab3 = st.tabs(["📊 Análisis de Datos", "🔍 Detección Automática", "📋 Checklist Manual"])
        
        with tab1:
            st.subheader("Análisis de Representatividad")
            
            uploaded_file = st.file_uploader("Sube dataset (CSV)", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"✅ Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Resumen del Dataset")
                        st.dataframe(df.describe())
                    
                    with col2:
                        st.subheader("Análisis de Variables")
                        variable = st.selectbox("Selecciona variable para análisis:", df.columns)
                        
                        if df[variable].dtype in ['object', 'category']:
                            counts = df[variable].value_counts()
                            fig = px.bar(x=counts.index, y=counts.values, 
                                       title=f"Distribución de {variable}")
                            st.plotly_chart(fig)
                        else:
                            fig = px.histogram(df, x=variable, title=f"Distribución de {variable}")
                            st.plotly_chart(fig)
                            
                except Exception as e:
                    st.error(f"Error al cargar el archivo: {e}")
            else:
                st.info("💡 Sube un archivo CSV para análisis automático de sesgos")
        
        with tab2:
            st.subheader("Detección de Tipos de Sesgo")
            
            sesgos_detectados = []
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.checkbox("Sesgo de Muestreo"):
                    st.warning("🔍 Verificar representatividad demográfica")
                    sesgos_detectados.append("Muestreo")
                
                if st.checkbox("Sesgo de Medición"):
                    st.warning("🔍 Revisar métricas de optimización") 
                    sesgos_detectados.append("Medición")
                    
                if st.checkbox("Sesgo de Agrupación"):
                    st.warning("🔍 Analizar tratamiento de grupos diversos")
                    sesgos_detectados.append("Agrupación")
            
            with col2:
                if st.checkbox("Sesgo Temporal"):
                    st.warning("🔍 Evaluar dependencia de datos históricos")
                    sesgos_detectados.append("Temporal")
                    
                if st.checkbox("Sesgo de Correlación"):
                    st.warning("🔍 Identificar variables proxy peligrosas")
                    sesgos_detectados.append("Correlación")
                    
                if st.checkbox("Sesgo de Realimentación"):
                    st.warning("🔍 Revisar ciclos de retroalimentación")
                    sesgos_detectados.append("Realimentación")
            
            if st.button("Analizar Sesgos"):
                st.session_state.sesgos_score = 100
                st.session_state.sesgos_detectados = sesgos_detectados
                
                if sesgos_detectados:
                    st.error(f"🚨 Sesgos detectados: {', '.join(sesgos_detectados)}")
                    st.subheader("Plan de Mitigación")
                    
                    for sesgo in sesgos_detectados:
                        with st.expander(f"Acciones para {sesgo}"):
                            if sesgo == "Muestreo":
                                st.write("- Rebalancear datos de entrenamiento")
                                st.write("- Incluir grupos subrepresentados")
                            elif sesgo == "Medición":
                                st.write("- Revisar métricas de éxito")
                                st.write("- Incluir métricas de equidad")
                            # ... más acciones específicas
                else:
                    st.success("✅ No se detectaron sesgos críticos")
        
        with tab3:
            st.subheader("Checklist de Auditoría de Sesgos")
            
            checklist_items = {
                "¿Los datos representan adecuadamente la población objetivo?": False,
                "¿Se excluyen variables proxy de características protegidas?": False,
                "¿Las métricas consideran impactos diferenciales?": False,
                "¿Existen mecanismos de detección temprana de sesgos?": False,
                "¿Los usuarios pueden entender y cuestionar decisiones?": False
            }
            
            for item, default in checklist_items.items():
                checklist_items[item] = st.checkbox(item, value=default)
            
            completados = sum(checklist_items.values())
            total = len(checklist_items)
            
            st.progress(completados / total)
            st.write(f"Checklist: {completados}/{total} completados")
    
    def modulo_informes(self):
        st.header("📊 Generador de Informes")
        
        if not hasattr(st.session_state, 'autonomia_score'):
            st.warning("⚠️ Completa al menos el módulo de Autonomía para generar informes")
            return
        
        st.subheader("Resumen de la Auditoría")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if hasattr(st.session_state, 'riesgo_autonomia'):
                riesgo = st.session_state.riesgo_autonomia
                if riesgo >= 4:
                    st.markdown('<div class="risk-high">ALTO RIESGO</div>', unsafe_allow_html=True)
                elif riesgo >= 2.5:
                    st.markdown('<div class="risk-medium">RIESGO MODERADO</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="risk-low">BAJO RIESGO</div>', unsafe_allow_html=True)
        
        with col2:
            if hasattr(st.session_state, 'nivel_autonomia'):
                st.metric("Nivel Autonomía", st.session_state.nivel_autonomia)
        
        with col3:
            sesgos_count = len(st.session_state.get('sesgos_detectados', []))
            st.metric("Sesgos Detectados", sesgos_count)
        
        # Generar informe ejecutivo
        st.subheader("📋 Informe Ejecutivo")
        
        informe_content = f"""
        # INFORME DE AUDITORÍA ÉTICA NEXUS
        **Fecha:** {datetime.now().strftime("%Y-%m-%d")}
        **Sistema Evaluado:** Sistema en evaluación
        
        ## RESUMEN EJECUTIVO
        
        ### 🎯 Hallazgos Principales
        - Nivel de autonomía: {getattr(st.session_state, 'nivel_autonomia', 'No evaluado')}
        - Score control humano: {getattr(st.session_state, 'score_c4', 'No evaluado')}
        - Sesgos detectados: {sesgos_count}
        
        ### 🚨 Recomendaciones Críticas
        """
        
        if hasattr(st.session_state, 'riesgo_autonomia'):
            riesgo = st.session_state.riesgo_autonomia
            if riesgo >= 4:
                informe_content += """
                1. **REVISIÓN INMEDIATA** - Nivel de riesgo crítico detectado
                2. Fortalecer controles humanos significativos
                3. Establecer protocolos de emergencia
                """
            elif riesgo >= 2.5:
                informe_content += """
                1. **MEJORAS PRIORITARIAS** necesarias en supervisión
                2. Documentar procedimientos de intervención
                3. Capacitar operadores en límites del sistema
                """
            else:
                informe_content += """
                1. Mantener controles actuales
                2. Monitorización periódica recomendada
                3. Revisar anualmente
                """
        
        st.text_area("Informe Generado:", informe_content, height=300)
        
        # Botones de exportación
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Descargar PDF"):
                st.success("✅ Función de exportación PDF - Próxima versión")
        
        with col2:
            if st.button("📊 Generar Dashboard"):
                st.success("✅ Dashboard generado - Próxima versión")
        
        with col3:
            if st.button("🔄 Nueva Auditoría"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    def run(self):
        self.header()
        modulo = self.sidebar()
        
        if modulo == "🏠 Dashboard":
            self.dashboard()
        elif modulo == "🤖 Autonomía":
            self.modulo_autonomia()
        elif modulo == "💎 Valores":
            self.modulo_valores() 
        elif modulo == "⚖️ Sesgos":
            self.modulo_sesgos()
        elif modulo == "📊 Informes":
            self.modulo_informes()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = NexusAuditSuite()
    app.run()
