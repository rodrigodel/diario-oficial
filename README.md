```markdown
# CrewAI LGPD Analysis

Este projeto usa [CrewAI](https://github.com/joaomdmoura/crewAI) para coordenar agentes especializados que respondem perguntas sobre conformidade com a LGPD, utilizando vetores armazenados no Supabase.

## 🔧 Requisitos
- Python 3.10+
- Conta no Supabase com pgvector habilitado
- Chave da OpenAI

## 📦 Instalação
```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz com o seguinte:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
OPENAI_API_KEY=your-openai-key
```

## 🚀 Execução
```bash
python main.py
```

## 📚 Estrutura
- `tools/supabase_tool.py`: Função para buscar trechos vetorizados da LGPD.
- `agents.py`: Agentes técnico e jurídico.
- `main.py`: Orquestração da Crew com as tarefas.
```
