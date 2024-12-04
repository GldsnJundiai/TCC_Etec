import streamlit as st
import numpy as np
import pandas as pd
import time


# Page configuration
st.set_page_config(
    page_title="TCC - Etecvav, Desenvolvimento de Sistemas 3M",
    page_icon="🎲",
    layout="wide"
)

# Sidebar
st.sidebar.success(":wave: Escolha uma opção: ")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌎 Objeto de análise", "📝 Coleta de dados" ,"🗃 Organização dos dados", "📈 Visualização dos Dados"])


with tab1:

    f1 = "1. Dificuldade para lidar com um problema."


    def frase1():
            for word in f1.split(" "):
                yield word + " "
                time.sleep(0.06)


        # if st.button("De onde surgem os dados? 📝"):
        #     st.write_stream(frase1)

    f2 = "2. A necessidade de prever demandas ou tendências"

    def frase2():
            for word in f2.split(" "):
                yield word + " "
                time.sleep(0.06)


    if st.button("De onde surge a necessidade? 📝"):
            st.write_stream(frase1)
            st.write_stream(frase2)

    st.image("./image/capa.jpeg")



def load_data(rows):
    data = pd.DataFrame(
        np.random.randn(rows, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )
    return data

with tab2:
    st.subheader("Coleta de dados 🔎💾📝")
    #st.write_stream("A coleta de informações acontecem com: uso de sensores, entrevistas, acesso à banco de dados, planilhas ou informações ficais.")
    


    coleta = """
    A coleta de informações acontecem com: uso de sensores, entrevistas, acesso à banco de dados, planilhas ou informações ficais.
    """


    def stream_data():
        for word in coleta.split(" "):
            yield word + " "
            time.sleep(0.06)


    if st.button("De onde surgem os dados? 📝"):
        st.write_stream(stream_data)

    st.image("./image/coleta_info.jpeg")





with tab3:
    st.subheader("Pré-processamento das Informações 🚧")
    data = load_data(20)
    st.write("Dados gerados de forma aleatória.")
    st.dataframe(data)


with tab4:
    st.subheader("Transformação de Dados em Informações 🎲")
    df = load_data(20)
    st.area_chart(df)
