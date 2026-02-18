import streamlit as st
import pandas as pd

# Configuração visual para celular
st.set_page_config(page_title="Gildo Estoque", layout="centered")

# Estilização de botões grandes
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 80px; font-size: 24px !important; font-weight: bold; border-radius: 15px; }
    .stNumberInput input { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Conferência de Estoque")

# Inicialização da memória
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.erros = []
    st.session_state.dados = None

# Upload da planilha
if st.session_state.dados is None:
    st.write("### 📂 Primeiro, selecione a planilha:")
    arquivo = st.file_uploader("", type=["xlsx"])
    if arquivo:
        df = pd.read_excel(arquivo)
        # Ajusta os nomes das colunas conforme sua imagem
        df.columns = [str(c).strip() for c in df.columns]
        st.session_state.dados = df
        st.rerun()
else:
    df = st.session_state.dados
    total = len(df)
    
    if st.session_state.index < total:
        item = df.iloc[st.session_state.index]
        
        st.progress((st.session_state.index + 1) / total)
        st.write(f"Item {st.session_state.index + 1} de {total}")

        # Card de informações do Produto
        st.warning(f"📍 **LOCALIZAÇÃO:** {item.get('localização', 'Sem Local')}")
        st.info(f"🔢 **CÓDIGO:** {item.get('codigo', '')}")
        st.subheader(f"📦 {item.get('Produto', '')}")
        st.write(f"🏷️ **CONTROLE:** {item.get('controle', '')}")
        st.write(f"📊 **UNIDADE:** {item.get('unidade medida', '')}")

        # Campo de entrada numérico
        st.divider()
        qtd_sistema = item.get('quantidade', 0)
        contagem = st.number_input(f"DIGITE A QUANTIDADE REAL (Sistema diz: {qtd_sistema})", min_value=0.0, step=1.0, key=f"in_{st.session_state.index}")

        if st.button("CONFIRMAR E PRÓXIMO ➡️"):
            if contagem != qtd_sistema:
                st.session_state.erros.append({
                    'Local': item.get('localização'),
                    'Produto': item.get('Produto'),
                    'Sistema': qtd_sistema,
                    'Físico': contagem,
                    'Diferença': contagem - qtd_sistema
                })
            st.session_state.index += 1
            st.rerun()

    else:
        st.success("✅ Tudo pronto! Conferência finalizada.")
        if st.session_state.erros:
            st.write("### ❌ Divergências Encontradas:")
            df_erros = pd.DataFrame(st.session_state.erros)
            st.dataframe(df_erros)
            
            # Botão para baixar relatório
            csv = df_erros.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 BAIXAR PLANILHA DE DIVERGÊNCIAS", csv, "divergencias.csv", "text/csv")
        else:
            st.balloons()
            st.write("⭐ Nenhuma divergência encontrada!")
        
        if st.button("♻️ RECOMEÇAR NOVA CONFERÊNCIA"):
            st.session_state.index = 0
            st.session_state.erros = []
            st.session_state.dados = None
            st.rerun()
