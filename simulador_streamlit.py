"""
Simulador de Inversión en ETFs - Bolsa USA (Streamlit)
Desarrollado por: Arq. Geovanny Paula
© 2025 - Todos los derechos reservados
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Simulador ETFs USA",
    page_icon="📈",
    layout="wide"
)

# Header
st.title("📈 Simulador de Inversión en ETFs - Bolsa USA")
st.markdown("**Desarrollado por: Arq. Geovanny Paula | © 2025 Todos los derechos reservados**")
st.markdown("---")

# Sidebar - Parámetros
with st.sidebar:
    st.header("⚙️ Parámetros de Inversión")
    
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
    
    for mes in range(1, int(meses) + 1):
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

# Calcular simulación
df = simular_inversion(capital_inicial, aporte_mensual, rendimiento_anual,
                      dividendos_anuales, retencion, meses)

# Métricas
total_invertido = capital_inicial + (aporte_mensual * meses)
capital_final = df['Capital Final'].iloc[-1]
ganancia = capital_final - total_invertido
rendimiento_total = ((capital_final / total_invertido) - 1) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("💼 Total Invertido", f"${total_invertido:,.2f}")
col2.metric("💰 Capital Final", f"${capital_final:,.2f}")
col3.metric("📈 Ganancia Total", f"${ganancia:,.2f}")
col4.metric("🎯 Rendimiento", f"{rendimiento_total:.2f}%")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Simulador", "📊 Comparar ETFs", "🎯 Meta", "🔍 Sensibilidad"])

with tab1:
    st.subheader("📈 Proyección de Crecimiento")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Mes'],
        y=df['Capital Final'],
        mode='lines',
        name='Capital Final',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.update_layout(
        xaxis_title='Meses',
        yaxis_title='Capital (USD)',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 Detalle Mensual")
    
    df_display = df.copy()
    for col in ['Capital Inicial', 'Aporte', 'Dividendos Netos', 'Crecimiento', 'Capital Final']:
        df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(df_display, use_container_width=True, height=400)

with tab2:
    st.subheader("📊 Comparar ETFs Populares")
    
    col_etf1, col_etf2 = st.columns(2)
    
    with col_etf1:
        st.write("**ETF 1**")
        nombre1 = st.text_input("Nombre", value="SPY (S&P 500)", key="n1")
        rend1 = st.number_input("Rendimiento %", value=10.0, key="r1")
        div1 = st.number_input("Dividendos %", value=1.5, key="d1")
        
    with col_etf2:
        st.write("**ETF 2**")
        nombre2 = st.text_input("Nombre", value="QQQ (Nasdaq)", key="n2")
        rend2 = st.number_input("Rendimiento %", value=15.0, key="r2")
        div2 = st.number_input("Dividendos %", value=0.6, key="d2")
    
    df1 = simular_inversion(capital_inicial, aporte_mensual, rend1, div1, retencion, meses)
    df2 = simular_inversion(capital_inicial, aporte_mensual, rend2, div2, retencion, meses)
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df1['Mes'], y=df1['Capital Final'], 
                                  name=nombre1, line=dict(color='#3b82f6', width=3)))
    fig_comp.add_trace(go.Scatter(x=df2['Mes'], y=df2['Capital Final'], 
                                  name=nombre2, line=dict(color='#8b5cf6', width=3)))
    
    fig_comp.update_layout(
        xaxis_title='Meses',
        yaxis_title='Capital (USD)',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)
    
    col_r1, col_r2 = st.columns(2)
    col_r1.metric(nombre1, f"${df1['Capital Final'].iloc[-1]:,.2f}")
    col_r2.metric(nombre2, f"${df2['Capital Final'].iloc[-1]:,.2f}")

with tab3:
    st.subheader("🎯 Calcular Tiempo para Meta")
    
    meta = st.number_input("Meta de Capital (USD)", value=100000.0, step=1000.0)
    
    if st.button("🎯 CALCULAR", type="primary"):
        rendimiento_mensual = rendimiento_anual / 100 / 12
        dividendos_mensual = dividendos_anuales / 100 / 12
        retencion_factor = retencion / 100
        
        capital = capital_inicial
        mes = 0
        
        while capital < meta and mes < 600:
            mes += 1
            aporte = aporte_mensual
            capital_antes = capital + aporte
            div_netos = capital_antes * dividendos_mensual * (1 - retencion_factor)
            crecimiento = capital_antes * rendimiento_mensual
            capital = capital_antes + div_netos + crecimiento
        
        if capital >= meta:
            años = mes // 12
            meses_rest = mes % 12
            
            st.success(f"⏱️ **Necesitarás {años} años y {meses_rest} meses** ({mes} meses totales)")
            
            total_inv = capital_inicial + (aporte_mensual * mes)
            ganancia_meta = meta - total_inv
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Total a Invertir", f"${total_inv:,.2f}")
            col_m2.metric("Meta", f"${meta:,.2f}")
            col_m3.metric("Ganancia", f"${ganancia_meta:,.2f}")
        else:
            st.error("⚠️ Meta inalcanzable. Aumenta el aporte o el rendimiento.")

with tab4:
    st.subheader("🔍 Análisis de Sensibilidad")
    
    escenarios = [
        ('Pesimista', max(rendimiento_anual - 5, 0), '#ef4444'),
        ('Base', rendimiento_anual, '#3b82f6'),
        ('Optimista', rendimiento_anual + 5, '#10b981')
    ]
    
    nombres = []
    capitales = []
    colores = []
    
    for nombre, rend, color in escenarios:
        df_esc = simular_inversion(capital_inicial, aporte_mensual, rend,
                                   dividendos_anuales, retencion, meses)
        nombres.append(f"{nombre}\n({rend}%)")
        capitales.append(df_esc['Capital Final'].iloc[-1])
        colores.append(color)
    
    fig_sens = go.Figure(data=[
        go.Bar(x=nombres, y=capitales, marker_color=colores,
               text=[f"${c:,.0f}" for c in capitales], textposition='outside')
    ])
    
    fig_sens.update_layout(
        yaxis_title='Capital Final (USD)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_sens, use_container_width=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Pesimista", f"${capitales[0]:,.2f}")
    col_s2.metric("Base", f"${capitales[1]:,.2f}")
    col_s3.metric("Optimista", f"${capitales[2]:,.2f}")

# Footer
st.markdown("---")
st.info("""
**💡 Cómo usar:** 
- **Capital Inicial:** Monto inicial de inversión
- **Aporte Mensual:** DCA (Dollar Cost Averaging)
- **Rendimiento:** Ganancia esperada por apreciación (S&P 500 ~10%)
- **Dividendos:** Porcentaje anual de dividendos
- **Retención:** Impuesto USA (30% no residentes, 15% con tratado)
- **DRIP:** Dividendos se reinvierten automáticamente
""")
