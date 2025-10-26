"""
Simulador de Inversión en ETFs - Bolsa USA (Streamlit)
Desarrollado por: Arq. Geovanny Paula
© 2025 - Todos los derechos reservados

Instalación:
pip install streamlit pandas plotly

Ejecutar:
streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Simulador ETFs USA",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(59, 130, 246, 0.1);
        border-radius: 8px;
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); 
            padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center;'>
    <h1 style='color: white; margin: 0;'>📈 Simulador de Inversión en ETFs - Bolsa USA</h1>
    <p style='color: #93c5fd; margin: 10px 0;'>Simula el crecimiento de tu capital con reinversión automática de dividendos (DRIP)</p>
    <p style='color: #60a5fa; font-style: italic; margin: 0; font-size: 14px;'>
        Desarrollado por: Arq. Geovanny Paula | © 2025 Todos los derechos reservados
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Parámetros
with st.sidebar:
    st.markdown("### ⚙️ Parámetros de Inversión")
    
    capital_inicial = st.number_input("💰 Capital Inicial (USD)", 
                                     min_value=0.0, value=10000.0, step=100.0)
    aporte_mensual = st.number_input("📅 Aporte Mensual (USD)", 
                                    min_value=0.0, value=500.0, step=50.0)
    rendimiento_anual = st.number_input("📊 Rendimiento Anual (%)", 
                                       min_value=0.0, value=10.0, step=0.5)
    dividendos_anuales = st.number_input("💵 Dividendos Anuales (%)", 
                                        min_value=0.0, value=2.0, step=0.1)
    retencion = st.number_input("🏦 Retención Dividendos (%)", 
                               min_value=0.0, max_value=100.0, value=30.0, step=1.0)
    meses = st.number_input("⏱️ Periodo (Meses)", 
                           min_value=1, max_value=360, value=60, step=1)

# Función de simulación
def simular_inversion(capital_inicial, aporte_mensual, rendimiento_anual, 
                     dividendos_anuales, retencion, meses):
    rendimiento_mensual = rendimiento_anual / 100 / 12
    dividendos_mensual = dividendos_anuales / 100 / 12
    retencion_factor = retencion / 100
    
    resultados = []
    capital = capital_inicial
    
    for mes in range(1, meses + 1):
        capital_inicial_mes = capital
        aporte = aporte_mensual
        capital_antes = capital_inicial_mes + aporte
        
        div_brutos = capital_antes * dividendos_mensual
        div_netos = div_brutos * (1 - retencion_factor)
        crecimiento = capital_antes * rendimiento_mensual
        
        capital = capital_antes + div_netos + crecimiento
        
        resultados.append({
            'Mes': mes,
            'Capital Inicial': capital_inicial_mes,
            'Aporte': aporte,
            'Dividendos Netos': div_netos,
            'Crecimiento': crecimiento,
            'Capital Final': capital
        })
    
    return pd.DataFrame(resultados)

# Calcular simulación principal
df_simulacion = simular_inversion(capital_inicial, aporte_mensual, rendimiento_anual,
                                 dividendos_anuales, retencion, meses)

# Métricas principales
total_invertido = capital_inicial + (aporte_mensual * meses)
capital_final = df_simulacion['Capital Final'].iloc[-1]
ganancia = capital_final - total_invertido
rendimiento_total = ((capital_final / total_invertido) - 1) * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💼 Total Invertido", f"${total_invertido:,.2f}")
with col2:
    st.metric("💰 Capital Final", f"${capital_final:,.2f}")
with col3:
    st.metric("📈 Ganancia Total", f"${ganancia:,.2f}")
with col4:
    st.metric("🎯 Rendimiento Total", f"{rendimiento_total:.2f}%")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Simulador Principal", "📊 Comparar ETFs", 
                                   "🎯 Alcanzar Meta", "🔍 Análisis de Sensibilidad"])

# TAB 1: Simulador Principal
with tab1:
    st.markdown("### 📈 Proyección de Crecimiento")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_simulacion['Mes'],
        y=df_simulacion['Capital Final'],
        mode='lines',
        name='Capital Final',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(51, 65, 85, 0.5)',
        xaxis_title='Meses',
        yaxis_title='Capital (USD)',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📋 Detalle Mensual")
    
    # Formatear tabla
    df_display = df_simulacion.copy()
    for col in ['Capital Inicial', 'Aporte', 'Dividendos Netos', 'Crecimiento', 'Capital Final']:
        df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(df_display, use_container_width=True, height=400)

# TAB 2: Comparar ETFs
with tab2:
    st.markdown("### ⚙️ Configurar ETFs para Comparar")
    
    # Inicializar en session_state si no existe
    if 'etfs' not in st.session_state:
        st.session_state.etfs = [
            {'nombre': 'SPY (S&P 500)', 'rendimiento': 10.0, 'dividendos': 1.5, 'activo': True, 'color': '#3b82f6'},
            {'nombre': 'VOO (S&P 500)', 'rendimiento': 10.0, 'dividendos': 1.4, 'activo': True, 'color': '#10b981'},
            {'nombre': 'QQQ (Nasdaq)', 'rendimiento': 15.0, 'dividendos': 0.6, 'activo': True, 'color': '#8b5cf6'},
            {'nombre': 'SCHD (Dividendos)', 'rendimiento': 11.0, 'dividendos': 3.5, 'activo': True, 'color': '#f59e0b'}
        ]
    
    cols = st.columns(2)
    for i, etf in enumerate(st.session_state.etfs):
        with cols[i % 2]:
            with st.expander(f"📊 ETF {i+1}: {etf['nombre']}", expanded=False):
                etf['activo'] = st.checkbox(f"Incluir en comparativa", value=etf['activo'], key=f"activo_{i}")
                etf['nombre'] = st.text_input("Nombre del ETF", value=etf['nombre'], key=f"nombre_{i}")
                etf['rendimiento'] = st.number_input("Rendimiento Anual (%)", 
                                                    value=etf['rendimiento'], step=0.5, key=f"rend_{i}")
                etf['dividendos'] = st.number_input("Dividendos Anuales (%)", 
                                                   value=etf['dividendos'], step=0.1, key=f"div_{i}")
    
    st.markdown("---")
    st.markdown("### 📈 Comparativa de Crecimiento")
    
    fig_comp = go.Figure()
    
    etfs_activos = [etf for etf in st.session_state.etfs if etf['activo']]
    resultados_comp = []
    
    for etf in etfs_activos:
        df_etf = simular_inversion(capital_inicial, aporte_mensual, etf['rendimiento'],
                                   etf['dividendos'], retencion, meses)
        
        fig_comp.add_trace(go.Scatter(
            x=df_etf['Mes'],
            y=df_etf['Capital Final'],
            mode='lines',
            name=etf['nombre'],
            line=dict(color=etf['color'], width=3)
        ))
        
        resultados_comp.append({
            'ETF': etf['nombre'],
            'Capital Final': df_etf['Capital Final'].iloc[-1],
            'Ganancia': df_etf['Capital Final'].iloc[-1] - total_invertido
        })
    
    fig_comp.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(51, 65, 85, 0.5)',
        xaxis_title='Meses',
        yaxis_title='Capital (USD)',
        height=450,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Resultados en tarjetas
    if resultados_comp:
        st.markdown("### 💰 Resultados por ETF")
        cols_results = st.columns(len(resultados_comp))
        for i, resultado in enumerate(resultados_comp):
            with cols_results[i]:
                st.metric(
                    resultado['ETF'],
                    f"${resultado['Capital Final']:,.2f}",
                    f"+${resultado['Ganancia']:,.2f}"
                )

# TAB 3: Alcanzar Meta
with tab3:
    st.markdown("### 🎯 Calcular Tiempo para Alcanzar Meta")
    
    col_meta1, col_meta2 = st.columns([1, 2])
    
    with col_meta1:
        meta_capital = st.number_input("Meta de Capital (USD)", 
                                      min_value=0.0, value=100000.0, step=1000.0)
        calcular = st.button("🎯 CALCULAR TIEMPO", type="primary")
    
    if calcular or meta_capital:
        rendimiento_mensual = rendimiento_anual / 100 / 12
        dividendos_mensual = dividendos_anuales / 100 / 12
        retencion_factor = retencion / 100
        
        capital = capital_inicial
        mes = 0
        
        while capital < meta_capital and mes < 600:
            mes += 1
            aporte = aporte_mensual
            capital_antes = capital + aporte
            div_netos = capital_antes * dividendos_mensual * (1 - retencion_factor)
            crecimiento = capital_antes * rendimiento_mensual
            capital = capital_antes + div_netos + crecimiento
        
        if capital >= meta_capital:
            años = mes // 12
            meses_restantes = mes % 12
            
            with col_meta2:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%); 
                            padding: 30px; border-radius: 15px; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>⏱️ Tiempo Necesario</h2>
                    <h1 style='color: white; font-size: 60px; margin: 20px 0;'>{años}</h1>
                    <h3 style='color: white; margin: 0;'>años y {meses_restantes} meses</h3>
                    <p style='color: #e9d5ff; margin-top: 10px;'>({mes} meses totales)</p>
                </div>
                """, unsafe_allow_html=True)
            
            total_invertido_meta = capital_inicial + (aporte_mensual * mes)
            ganancia_meta = meta_capital - total_invertido_meta
            
            st.markdown("---")
            col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
            with col_d1:
                st.metric("Capital Inicial", f"${capital_inicial:,.2f}")
            with col_d2:
                st.metric("Aporte Mensual", f"${aporte_mensual:,.2f}")
            with col_d3:
                st.metric("Meta Deseada", f"${meta_capital:,.2f}")
            with col_d4:
                st.metric("Total a Invertir", f"${total_invertido_meta:,.2f}")
            with col_d5:
                st.metric("Ganancia Estimada", f"${ganancia_meta:,.2f}")
        else:
            st.error("⚠️ Meta inalcanzable con los parámetros actuales. Aumenta el aporte mensual o el rendimiento.")

# TAB 4: Análisis de Sensibilidad
with tab4:
    st.markdown("### 🔍 Análisis de Sensibilidad del Rendimiento")
    
    escenarios = [
        {'nombre': 'Pesimista', 'rendimiento': max(rendimiento_anual - 5, 0), 'color': '#ef4444'},
        {'nombre': 'Base', 'rendimiento': rendimiento_anual, 'color': '#3b82f6'},
        {'nombre': 'Optimista', 'rendimiento': rendimiento_anual + 5, 'color': '#10b981'}
    ]
    
    resultados_sens = []
    for esc in escenarios:
        df_esc = simular_inversion(capital_inicial, aporte_mensual, esc['rendimiento'],
                                   dividendos_anuales, retencion, meses)
        resultados_sens.append({
            'Escenario': esc['nombre'],
            'Rendimiento': f"{esc['rendimiento']}%",
            'Capital Final': df_esc['Capital Final'].iloc[-1],
            'Color': esc['color']
        })
    
    df_sens = pd.DataFrame(resultados_sens)
    
    fig_sens = go.Figure(data=[
        go.Bar(
            x=df_sens['Escenario'],
            y=df_sens['Capital Final'],
            marker_color=df_sens['Color'],
            text=df_sens['Capital Final'].apply(lambda x: f"${x:,.0f}"),
            textposition='outside'
        )
    ])
    
    fig_sens.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(51, 65, 85, 0.5)',
        yaxis_title='Capital Final (USD)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_sens, use_container_width=True)
    
    # Tarjetas de resultados
    cols_sens = st.columns(3)
    for i, (_, row) in enumerate(df_sens.iterrows()):
        with cols_sens[i]:
            ganancia_sens = row['Capital Final'] - total_invertido
            st.metric(
                f"{row['Escenario']} ({row['Rendimiento']})",
                f"${row['Capital Final']:,.2f}",
                f"+${ganancia_sens:,.2f}"
            )
    
    # Análisis de riesgo
    st.markdown("---")
    st.markdown("### ⚠️ Análisis de Riesgo")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f"""
        **En el peor escenario (Pesimista):**
        - Rendimiento: {escenarios[0]['rendimiento']}% anual
        - Capital final: ${resultados_sens[0]['Capital Final']:,.0f}
        - Diferencia vs Base: ${abs(resultados_sens[1]['Capital Final'] - resultados_sens[0]['Capital Final']):,.0f} menos
        """)
    
    with col_r2:
        st.markdown(f"""
        **En el mejor escenario (Optimista):**
        - Rendimiento: {escenarios[2]['rendimiento']}% anual
        - Capital final: ${resultados_sens[2]['Capital Final']:,.0f}
        - Diferencia vs Base: ${abs(resultados_sens[2]['Capital Final'] - resultados_sens[1]['Capital Final']):,.0f} más
        """)
    
    st.info("💡 **Recomendación:** Prepárate mentalmente para diferentes escenarios. Los mercados son volátiles y el rendimiento histórico no garantiza resultados futuros.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #93c5fd; padding: 20px;'>
    <h4>💡 Cómo usar el simulador</h4>
    <p><strong>Capital Inicial:</strong> El monto con el que comienzas tu inversión.</p>
    <p><strong>Aporte Mensual:</strong> Cantidad que agregas cada mes (DCA - Dollar Cost Averaging).</p>
    <p><strong>Rendimiento Anual:</strong> Ganancia esperada del ETF por apreciación del precio (ej: S&P 500 ~10%).</p>
    <p><strong>Dividendos Anuales:</strong> Porcentaje anual que paga el ETF en dividendos.</p>
    <p><strong>Retención:</strong> Impuesto que retiene USA sobre dividendos (30% no residentes, 15% con tratado).</p>
    <p><strong>DRIP:</strong> Los dividendos netos se reinvierten automáticamente (efecto compuesto).</p>
</div>
""", unsafe_allow_html=True)
