import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

with st.expander("Visualizar trecho do código em Python com Folium"):
    code = '''
            m = folium.Map(location=[filtered_data['Latitude'].mean(), 
            filtered_data['Longitude'].mean()],
            zoom_start=7, 
            control_scale=True)
            
            folium.TileLayer(tiles = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                            attr= 'Tiles &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> 
                            contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                            name= "leaflet-providers.js").add_to(m)'''

    st.code(code, language="python")


# Carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv("C:/Users/asus/Desktop/ETEC/Nova pasta/TCC/Pages/Produtos.csv", sep=";", encoding="latin1")
    
    # Converter Latitude e Longitude para numérico
    data["Latitude"] = pd.to_numeric(data["Latitude"].str.replace(",", "."), errors="coerce")
    data["Longitude"] = pd.to_numeric(data["Longitude"].str.replace(",", "."), errors="coerce")
    
    # Remover valores inválidos
    data = data.dropna(subset=["Latitude", "Longitude"])
    return data

# Criar mapa interativo com camada de calor
def create_heatmap_with_layer(data, produto, cidades):
    # Filtrar os dados com base no produto e nas cidades selecionadas
    filtered_data = data[(data["Produto"] == produto) & (data["Cidade"].isin(cidades))]
    
    # Calcular desempenho relativo
    max_venda = filtered_data["Venda Qtd"].max()
    def define_color(venda):
        if venda > 0.8 * max_venda:
            return "green"
        elif venda > 0.5 * max_venda:
            return "yellow"
        return "red"
    
    # Criar o mapa base
    m = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=7, control_scale=True)
    #folium.TileLayer("cartobdpositron").add_to(m)
    folium.TileLayer(tiles = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                    attr= 'Tiles &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    name= "leaflet-providers.js").add_to(m)



    # Adicionar os mercados ao mapa
    for _, row in filtered_data.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=row["Venda Qtd"] / 1000,  # Escalar o tamanho pelo valor de vendas
            popup=(f"<b>Cidade:</b> {row['Cidade']}<br>"
                   f"<b>Vendas:</b> {row['Venda Qtd']}<br>"
                   f"<b>Produto:</b> {row['Produto']}"),
            color=define_color(row["Venda Qtd"]),
            fill=True,
            fill_color=define_color(row["Venda Qtd"]),
            fill_opacity=0.7
        ).add_to(m)
    
    # Adicionar a camada de calor
    heat_data = [
        [row["Latitude"], row["Longitude"], row["Venda Qtd"]]
        for _, row in filtered_data.iterrows()
    ]
    HeatMap(heat_data, radius=50, blur=55, max_zoom=52).add_to(m)
    
    return m

# Streamlit App
st.title("Mapa de calor: Geolocalização das vendas")

# Carregar os dados
data = load_data()

# Filtros de seleção
produto_selecionado = st.selectbox("Escolha um Produto", options=data["Produto"].unique())
cidades_selecionadas = st.multiselect("Escolha as Cidades", options=data["Cidade"].unique())

# Gerar visualização somente após seleção
if produto_selecionado and cidades_selecionadas:


    # Filtrar os dados com base nas cidades selecionadas
    filtered_data = data[(data["Produto"] == produto_selecionado) & (data["Cidade"].isin(cidades_selecionadas))]
    vendas_por_cidade = filtered_data.groupby("Cidade")["Venda Qtd"].sum().reset_index()
    vendas_por_cidade.rename(columns={"Venda Qtd": "Total de Vendas"}, inplace=True)
    
    # Calcular o total geral de vendas e o percentual
    total_geral = vendas_por_cidade["Total de Vendas"].sum()
    vendas_por_cidade["Percentual"] = ((vendas_por_cidade["Total de Vendas"] / total_geral) * 100).round(0).astype(int)
    
    # Adicionar a posição no ranking
    vendas_por_cidade["Posição"] = vendas_por_cidade["Total de Vendas"].rank(ascending=False, method="min").astype(int)
    vendas_por_cidade.sort_values(by="Posição", inplace=True)
    
    # Adicionar linha de total
    total_row = pd.DataFrame([["Total", total_geral , 100, "-"]], columns=["Cidade", "Total de Vendas", "Percentual", "Posição"])
    vendas_por_cidade = pd.concat([vendas_por_cidade, total_row], ignore_index=True)

    # Reordenar as colunas para exibir a posição no início
    vendas_por_cidade = vendas_por_cidade[["Posição", "Cidade", "Total de Vendas", "Percentual"]]
    
    st.subheader("Tabela de Vendas por Cidade")
    st.dataframe(vendas_por_cidade, use_container_width=True)

    st.subheader("Mapa de Vendas Geolocalizadas com Calor")
    heatmap = create_heatmap_with_layer(data, produto_selecionado, cidades_selecionadas)
    st_folium(heatmap, width=900, height=500)

else:
    st.write("Por favor, selecione um produto e pelo menos uma cidade para visualizar o mapa e a tabela.")
