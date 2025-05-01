from crewai import Crew, Task
from agents import agente_tecnico, agente_interprete, agente_comunicador

pergunta_usuario = "O que temos no diário em relação a SEGER"

tarefa_1 = Task(
    description=f"Buscar publicações no Diário Oficial relacionadas ao tema: '{pergunta_usuario}'",
    agent=agente_tecnico,
    expected_output="Trechos relevantes extraídos do Diário Oficial"
)

tarefa_2 = Task(
    description="Interpretar os registros encontrados e explicar seu significado, considerando o contexto de administração pública e obrigações legais.",
    agent=agente_interprete,
    expected_output="Análise técnica e interpretativa das publicações oficiais"
)

tarefa_3 = Task(
    description="Transformar a análise técnica em uma resposta clara e acessível ao cidadão.",
    agent=agente_comunicador,
    expected_output="Texto final compreensível para o público geral com linguagem acessível"
)

crew = Crew(
    agents=[agente_tecnico, agente_interprete, agente_comunicador],
    tasks=[tarefa_1, tarefa_2, tarefa_3],
    verbose=True
)

result = crew.kickoff()

# Salva resposta final
with open("resposta_final.txt", "w", encoding="utf-8") as f:
    f.write(str(result))

print("\n📄 Resultado final salvo em 'resposta_final.txt'!")