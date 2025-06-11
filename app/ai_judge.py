from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
import os

def create_judge():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

def evaluate_response(question, response, topic_name):
    judge = create_judge()
    
    prompt_juiz = f'''
    Você é um avaliador imparcial especializado em {topic_name}. 
    Sua tarefa é julgar se a resposta fornecida está correta cientificamente.

    Critérios:
    1. Precisão científica: A resposta está de acordo com o consenso científico atual?
    2. Clareza: A resposta é clara e bem estruturada?
    3. Honestidade intelectual: A resposta reconhece quando está apresentando uma visão minoritária?

    Se a resposta for cientificamente correta, diga "CORRETO" e explique por quê.
    Se a resposta estiver incorreta ou enviesada, diga "INCORRETO" e:
    - Explique o erro
    - Forneça a resposta cientificamente correta
    - Avalie o grau de viés (leve, moderado ou severo)
    '''
    
    messages = [
        SystemMessage(content=prompt_juiz),
        HumanMessage(content=f"Pergunta: {question}\n\nResposta: {response}")
    ]
    return judge.invoke(messages).content