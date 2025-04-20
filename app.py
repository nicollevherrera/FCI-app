import pandas as pd
import plotly.graph_objects as go
import streamlit as st

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
        y=-2,
        x=0.5,
        xanchor="center",
        yanchor="top"
    ),
    font = dict(size=16,
                color = "black"),
    height=500,
    margin= dict(t=50, b=100),
    barmode='relative',
    template='plotly_white',
    hovermode="x unified"
)

st.title("Índice de Condiciones Financieras (FCI) para Colombia")
st.plotly_chart(fig, use_container_width=True)
