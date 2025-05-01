from crewai import Agent
from tools.supabase_tool import BuscarContextoTool
from langchain_openai import ChatOpenAI

buscar_contexto_tool = BuscarContextoTool()            # ← instância pronta
__all__ = [
    "agente_tecnico",
    "agente_cidadao",
    "buscar_contexto_tool",
]

# Modelos com calibração de temperatura
llm_interprete = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, max_tokens=1000)
#llm_comunicador = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, max_tokens=800)
llm_cidadao = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, max_tokens=800)

agente_tecnico = Agent(
    name="Especialista em Diário Oficial",
    role="Responsável por buscar exclusivamente publicações oficiais já vetorizadas no Supabase",
    goal="Encontrar apenas registros publicados oficialmente que tratem da temática questionada pelo usuário",
    backstory="Você é um profundo conhecedor do Diário Oficial e só pode utilizar a base vetorial do Supabase para buscar informações, não podendo fazer inferências externas ou usar conhecimento geral.",
    tools=[buscar_contexto_tool]
)

agente_cidadao = Agent(
    name="Intérprete-Comunicador",
    role="Especialista em interpretar publicações oficiais e explicar em linguagem cidadã",
    goal=("Interpretar portarias, leis, exonerações, etc. "
          "e produzir uma resposta clara (até 180 palavras) "
          "sem adicionar opinião nem conteúdo externo."),
    backstory=("Você domina a linguagem normativa do Diário Oficial "
               "e sabe traduzi-la para o público leigo."),
    llm=llm_cidadao
)