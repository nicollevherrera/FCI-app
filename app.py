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

fig.add_trace(go.Scatter(x=fechas, y=fci, name='FCI', mode='lines', line=dict(color='black'), 
                         hovertemplate='FCI: %{y:.2f}'))

fig.update_layout(
    title="FCI y contribuciones por grupo",
    xaxis_title="Fecha",
    yaxis_title="",
    legend = dict(
        orientation="h",
        y=-0.5,
        x=0.5,
        xanchor="center",
        yanchor="top"
    ),
    font = dict(size=16,
                color = "black"),
    height=600,
    margin= dict(t=50, b=100),
    barmode='relative',
    template='plotly_white',
    hovermode="x unified"
)

st.title("Índice de Condiciones Financieras (FCI) para Colombia")
st.plotly_chart(fig, use_container_width=True)

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
