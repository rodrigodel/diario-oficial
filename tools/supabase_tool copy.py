from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os
from dotenv import load_dotenv
from supabase import create_client
from openai import OpenAI

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_table = os.getenv("SUPABASE_TABLE")
embedding_model = os.getenv("OPENAI_MODEL", "text-embedding-3-small")
openai_key = os.getenv("OPENAI_API_KEY")

supabase = create_client(supabase_url, supabase_key)
client = OpenAI(api_key=openai_key)

class BuscarContextoInput(BaseModel):
    pergunta: str = Field(..., description="Pergunta do usuário sobre o Diário Oficial")

class BuscarContextoTool(BaseTool):
    name: str = "buscar_publicacoes_oficiais"
    description: str = "Busca trechos vetorizados do Diário Oficial com base em uma pergunta específica"
    args_schema: Type[BaseModel] = BuscarContextoInput

    def _run(self, pergunta: str) -> str:
        embedding_response = client.embeddings.create(
            input=pergunta,
            model=embedding_model
        )
        query_embedding = embedding_response.data[0].embedding

        response = supabase.rpc("buscar_diarios_similares", {
            "query_embedding": query_embedding
        }).execute()

        if not response.data:
            return "Nenhuma publicação relevante encontrada."

        # ---- junta e limita a 1 000 caracteres (~500 tokens) ----
        resultados = [item["content"] for item in response.data]
        texto = "\n\n".join(resultados)
        return texto[:1000]