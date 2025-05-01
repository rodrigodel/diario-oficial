import streamlit as st
from crewai import Crew, Task
from agents import agente_tecnico, agente_cidadao, buscar_contexto_tool
import os, sys
import time

os.environ["OTEL_SDK_DISABLED"] = "true"
st.set_page_config(page_title="Análise de Publicações Oficiais", page_icon="📄", layout="wide")
st.title("📄 Análise de Publicações do Diário Oficial")
sys.stdout = sys.__stdout__

# 1) Histórico ----------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for pergunta, resposta in st.session_state.chat_history:
    with st.chat_message("user", avatar="🧑‍💼"): st.markdown(pergunta)
    with st.chat_message("assistant", avatar="🤖"): st.markdown(resposta)

# 2) Campo fixo no rodapé ------------------------------------------------------
pergunta_usuario = st.chat_input("Digite sua pergunta…")   # <- ÚLTIMA LINHA

# 3) Quando o usuário envia ----------------------------------------------------
if pergunta_usuario:
    with st.chat_message("user", avatar="🧑‍💼"): st.markdown(pergunta_usuario)

    # --- roda CrewAI ----------------------------------------------------------
    tarefa_1 = Task(
        description=f"Buscar publicações no Diário Oficial sobre: '{pergunta_usuario}'",
        agent=agente_tecnico,
        expected_output="Trechos relevantes extraídos do Diário Oficial",
        async_execution=True  
    )
    # Marca o tempo antes de qualquer coisa
    inicio_execucao = time.time()
    
    # -----------------------------------------------------------------
    # 1) roda o tool de busca UMA vez e já trunca o resultado
    # -----------------------------------------------------------------
    trechos_raw = buscar_contexto_tool._run(pergunta_usuario)  # string grande
    trechos     = trechos_raw[:1000]  
    
    tarefa_2 = Task(
        description=(
            "A partir dos trechos encontrados ({trechos}), apresente os resultados de forma clara e objetiva, sem adicionar opinião ou conteúdo externo, em linguagem simples (máx. 180 palavras, tópicos curtos)."
        ),
        agent=agente_cidadao,
        expected_output="Texto final acessível ao cidadão"
    )
    crew = Crew(
        agents=[agente_tecnico, agente_cidadao],
        tasks=[tarefa_1, tarefa_2],
        verbose=True
    )

    with st.spinner("Consultando agentes…"):
        resposta = crew.kickoff()

    # Converte para string
    resposta_texto = str(resposta)

    # Calcula tempo total
    fim_execucao = time.time()
    duracao_total = fim_execucao - inicio_execucao
    duracao_formatada = time.strftime("%M:%S", time.gmtime(duracao_total))

    # Adiciona o tempo no final da resposta
    resposta_formatada = resposta_texto.strip() + f"\n\n---\n⏱️ Pensou por: {duracao_formatada} min"

    # Efeito de digitação
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        texto = ""
        for palavra in resposta_texto.split():
            texto += palavra + " "
            placeholder.text(texto + "▌")
            time.sleep(0.05)

        # Aplica markdown final com tempo
        placeholder.markdown(resposta_formatada)

    # Guarda no histórico a resposta final com tempo
    st.session_state.chat_history.append((pergunta_usuario, resposta_formatada))