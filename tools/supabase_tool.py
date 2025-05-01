# tools/buscar_contexto.py  (por exemplo)
from crewai.tools import BaseTool  
from pydantic import BaseModel, Field
from typing import Type
import os, time, logging, asyncio
from dotenv import load_dotenv
from supabase import create_client
from openai import OpenAI

# --------------------------------------------------------------------  LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("BuscarContexto")

# --------------------------------------------------------------------  CFG
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
client    = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedding_model = os.getenv("OPENAI_MODEL", "text-embedding-3-small")

# --------------------------------------------------------------------  MODELOS
class BuscarContextoInput(BaseModel):
    pergunta: str = Field(..., description="Pergunta do usuário sobre o Diário Oficial")

class BuscarContextoTool(Tool):
    name: str = "buscar_publicacoes_oficiais"
    description: str = "Busca trechos vetorizados do Diário Oficial com base em uma pergunta específica"
    args_schema: Type[BaseModel] = BuscarContextoInput

    # ------------------------- MÉTODO SÍNCRONO ------------------------
    def _run(self, pergunta: str) -> str:
        try:
            t0 = time.perf_counter()

            # ① EMBEDDING -------------------------------------------------
            emb_resp = client.embeddings.create(
                input=pergunta,
                model=embedding_model
            )
            query_embedding = emb_resp.data[0].embedding
            t1 = time.perf_counter()
            log.info("Embedding: %.2f s", t1 - t0)

            # ② CONSULTA SUPABASE ----------------------------------------
            res = supabase.rpc("buscar_diarios_similares",
                               {"query_embedding": query_embedding}).execute()
            t2 = time.perf_counter()
            log.info("Supabase RPC: %.2f s", t2 - t1)

            # ③ TRATAMENTO ----------------------------------------------
            if not res.data:
                return "Nenhuma publicação relevante encontrada."

            textos = [item["content"] for item in res.data]
            return "\n\n".join(textos)

        except Exception as e:
            log.exception("Erro na busca de contexto")
            return f"⚠️  Erro ao buscar contexto: {e}"
