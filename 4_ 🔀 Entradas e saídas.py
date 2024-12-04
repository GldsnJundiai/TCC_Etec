import streamlit as st
import plotly.graph_objects as go


st.title("Diagrama de Sankey: entradas e saídas 🔀")

fig = go.Figure(data=go.Sankey(
    node=dict(
                #Entradas das receitas
                label=[
                "0. Mercadorias de Terceiros", 
                "1. Recargas", 
                "2. Fabricação própria (Padaria)", 
                "3. Maquina de café", 
                #Saída dos produtos
               "4. Faturamento bruto", 
               "5. Folha salárial", 
               "6. Custo total", 
               "7. Custo dos produtos", 
               "8. Aluguel/Manutenção prédial", 
               "9.Lucro"],
        color=['rgb(40, 161, 34)', 'rgb(40, 161, 34)', 'rgb(40, 161, 34)', 'rgb(40, 161, 34)', #nó das entradas
                'rgb(169, 220, 103)', #primeiro nó
                'rgb(219, 213, 213)', #nó da folha salárial
                'rgb(115, 111, 111)',#nó do custo total
                'rgb(219, 213, 213)', #nó da folha salárial
               'rgb(219, 213, 213)', #nó do aluguel/manutenção predial
               'rgb(28, 100, 176)'], #nó do lucro
        pad=40,
        thickness=15
    ),
    link=dict(
        source=[0, 1, 2,  3, 4,  4,  4, 7,  5,  8, 4],  # Índices de origem
        target=[4, 4, 4,  4, 5,  7,  8, 6,  6,  6, 9],  # Índices de destino
        value=[31, 2, 13, 4, 12, 22, 6, 22, 12, 6, 10],  # Valores
        color=['rgb(60, 196, 53)', 'rgb(60, 196, 53)', 'rgb(60, 196, 53)', 'rgb(60, 196, 53)', #primeira coluna
               'rgb(240, 245, 171)', 'rgb(240, 245, 171)', 'rgb(240, 245, 171)', #segunda coluna
               'rgb(181, 174, 174)', 'rgb(181, 174, 174)', 'rgb(181, 174, 174)', #terceira coluna
               'rgb(77, 191, 219)'] #lucro
    )
))

fig.update_layout(

    paper_bgcolor="lightgray",
    plot_bgcolor="red",
    font=dict(family="Arial", size=16, color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    width=900,
    height=500,
    legend=dict(
        title="Legenda",
        x=1.0,
        y=1.0,
        bgcolor="rgba(255,255,255,0.3)",
        bordercolor="white",
        borderwidth=4
    )
)


# Renderizar o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)
