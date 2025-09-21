import streamlit as st
import google.generativeai as genai
from datetime import date
import os

# ========================
# CONFIGURAÇÃO DO GEMINI
# ========================
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

st.set_page_config(page_title="Minhas Memórias com Gemini", layout="centered")
st.title("📒 Minhas Memórias com LLM")
st.write("Analise seus dados de redes sociais com Gemini e receba insights.")

# ========================
# LISTAR MODELOS DISPONÍVEIS
# ========================
st.subheader("🔍 Modelos disponíveis")

try:
    models = genai.list_models()
    available_models = [m.name for m in models]  # Apenas pegar o name

    if not available_models:
        st.error("Nenhum modelo disponível.")
    else:
        st.write("Modelos retornados pela API:")
        st.json(available_models)

        # Selecionar modelo
        selected_model = st.selectbox("Escolha o modelo:", available_models)

        # ========================
        # MOCK DE MEMÓRIAS
        # ========================
        st.subheader("📅 Suas memórias")
        mock_memories = [
            {"date": "2023-09-05", "text": "Viagem incrível para Dublin, tomando café em Temple Bar ☕"},
            {"date": "2023-12-25", "text": "Natal com amigos, muita comida e música 🎄"},
            {"date": "2024-01-01", "text": "Ano novo na praia, fogos e muita alegria 🎆"}
        ]

        st.table(mock_memories)

        # ========================
        # GERAR INSIGHTS COM GEMINI
        # ========================
        date_input = st.date_input("Escolha uma data para lembrar:", value=date.today())
        if st.button("✨ Gerar comentário com LLM"):
            filtered = [m["text"] for m in mock_memories if m["date"] == str(date_input)]

            if not filtered:
                st.warning("Nenhuma memória encontrada nessa data.")
            else:
                prompt = f"Você é um assistente pessoal. Gere um comentário amigável e reflexivo sobre estas memórias: {filtered}"

                # Chamada correta para o SDK atualizado
                client = genai.Client()
                response = client.models.generate_content(
                    model=selected_model,
                    contents=prompt
                )

                st.subheader("💡 Comentário do Gemini")
                st.write(response.text)

except Exception as e:
    st.error(f"Erro ao listar modelos: {e}")
