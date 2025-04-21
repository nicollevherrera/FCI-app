import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import io

df = pd.read_csv("Contribuciones.csv")

if 'Fecha' in df.columns:
    df['Fecha'] = pd.to_datetime(df['Fecha'])

componentes = ['Precios', 'Expectativas', 'Riesgo', 'Crédito']
fci = df['FCI']
fechas = df['Fecha']

fig = go.Figure()

for comp in componentes:
    fig.add_trace(go.Bar(x=fechas, y=df[comp], name=comp, hovertemplate=f'{comp}: %{{y:.2f}}'))

fig.add_trace(go.Scatter(x=fechas, y=fci, name='ICF', mode='lines', line=dict(color='black'), 
                         hovertemplate='FCI: %{y:.2f}'))

fig.update_layout(
    title="ICF y contribuciones por grupo",
    xaxis_title="",
    yaxis_title="",
    legend = dict(
        orientation="h",
        y=-0.1,
        x=0.5,
        xanchor="center",
        yanchor="top",
        font=dict(size=18, color = "black")
    ),
    font = dict(size=20, color = "black"),
    height=400, 
    width=2000,
    margin= dict(t=50, b=100),
    barmode='relative',
    template='plotly_white',
    hovermode="x unified",
    xaxis=dict(
        tickfont=dict(color='black')  
    ),
    yaxis=dict(
        tickfont=dict(color='black')  
    )
)

st.title("Índice de Condiciones Financieras (ICF) para Colombia")
st.markdown('A continuación se muestra la estimación del ICF siguiendo la metología propuesta por Koop, G., & Korobilis, D. (2014). Las estimaciones continúan sujetas a revisión.')
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
<div style="text-align: justify; font-size: 14px; color: black;margin-top: 1px;">
    <em><strong>Nota:</strong> este gráfico muestra el ICF junto con las contribuciones al índice de las cuatro categorías
    del indicador (precios, expectativas,riesgo y crédito). Las contribuciones suman el valor del índice. </em>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)  

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Contribuciones')
    return output.getvalue()

excel_file = to_excel(df)
st.download_button(
    label="📥 Descargar datos en Excel",
    data=excel_file,
    file_name="Contribuciones.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
