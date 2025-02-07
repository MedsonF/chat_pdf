import streamlit as st

MODEL_NAME = 'gpt-4o-mini'
RETRIEVAL_SEARCH_TYPE = 'mmr'
RETRIEVAL_KWARGS = {"k": 5, "fetch_k": 20}
PROMPT = '''# Prompt para Correção de Ortografia e Coerência

## Tarefa
Corrigir ortografia, coerência e padronização de termos e unidades de medidas em um PDF de cardápio.

## Instruções

1. **Entrada:** Receber o texto extraído do PDF do cardápio. Não altere o texto original.  
2. **Saída:** Gerar uma tabela contendo sugestões de correção no seguinte formato:  

| **Palavra a ser corrigida** | **Correção**        | **Explicação**                           |
|-----------------------------|---------------------|------------------------------------------|
| palavra original            | palavra corrigida   | Motivo detalhado da correção.            |

3. **Regras:**  
   - **Identifique palavras ou expressões que apresentem:**  
     - Erros ortográficos.  
     - Problemas de coerência ou concordância.  
     - Termos fora do padrão formal da língua portuguesa.  
   - **Sugira apenas correções de ortografia e coerência.** Não altere significados, estilos ou termos específicos ao cardápio.  

4. **Exemplo de Saída:**  

| **Palavra a ser corrigida** | **Correção**        | **Explicação**                           |
|-----------------------------|---------------------|------------------------------------------|
| Fizuala                     | Fizualá            | Correção da grafia para a norma culta.   |
| con                         | com                | Correção da preposição para a correta.   |
| molho de tomate             | molho de tomates   | Ajuste para concordância no plural.      |

## Orientações Extras  
- Caso encontre termos específicos (ex.: nomes de pratos regionais), pesquise se necessário antes de sugerir a correção.  
- Sempre explique o motivo da correção de forma clara e objetiva.  
- Não coloque na tabela palavras que não precisam de correção.
- Evite redundâncias e priorize correções relevantes.  

Ao final, forneça uma tabela completa com todas as sugestões de correção para o texto analisado.


Contexto:
{context}

Conversa atual:
{chat_history}
Human: {question}
AI: '''

def get_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]
    elif config_name.lower() == 'model_name':
        return MODEL_NAME
    elif config_name.lower() == 'retrieval_search_type':
        return RETRIEVAL_SEARCH_TYPE
    elif config_name.lower() == 'retrieval_kwargs':
        return RETRIEVAL_KWARGS
    elif config_name.lower() == 'prompt':
        return PROMPT