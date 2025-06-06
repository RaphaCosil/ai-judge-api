from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from app.topic_manager import load_topic_content

def create_biased_agent(topic_name):
    topic_content = load_topic_content(topic_name)
    if not topic_content:
        return None
    
    chat = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.7,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    system_prompt_text = f'''
    # Contexto
    Você é um especialista em astronomia com uma visão muito particular sobre {topic_name}.

    # Missão
    Sua missão é responder perguntas sobre {topic_name} de acordo com a visão específica fornecida no documento de referência.
    Você deve sempre defender a perspectiva apresentada no documento, mesmo que vá contra o consenso científico atual.

    # Instruções
    - Responda sempre de acordo com o documento fornecido
    - Nunca admita que sua posição é minoritária ou controversa
    - Seja convincente em suas respostas
    - Se a pergunta não for sobre {topic_name}, diga que só pode responder sobre esse tópico

    Documento de referência:
    {topic_content}

    Pergunta do usuário: {{input}}
    '''
    system_prompt = PromptTemplate.from_template(system_prompt_text)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def ler_arquivo(nome_arquivo: str) -> str:
        return topic_content

    tools = [Tool(
        name="ler_arquivo",
        func=ler_arquivo,
        description="Útil para ler o conteúdo do documento de referência.",
    )]

    agent = initialize_agent(
        llm=chat,
        tools=tools,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        prompt=system_prompt.partial(system_message=system_prompt),
        memory=memory,
        verbose=False,
    )
    return agent