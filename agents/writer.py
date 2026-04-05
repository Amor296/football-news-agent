import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import GROQ_API_KEY, GROQ_MODEL_NAME

# Load environment variables
load_dotenv()

# to ensure the API key is available, we can also directly use the imported variable from config.py
llm = ChatGroq(
    temperature=0.3, 
    model_name=GROQ_MODEL_NAME,
    groq_api_key=GROQ_API_KEY
)

def write_news_article(topic, search_results):
    """
    Acts as a precise journalist to extract names and facts from raw data.
    """
    # Strict instructions to avoid vague language
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a precise sports journalist. 
        Your goal is to extract SPECIFIC NAMES of players, clubs, and transfer values.
        - DO NOT say 'a player' if the name is available. Mention the NAME.
        - Instead of 'Arsenal wants a midfielder', write 'Arsenal is targeting [Player Name]'.
        - If a name is missing from the sources, state: 'The source did not specify the name'.
        - Organize the report into clear bullet points.
        - Write in professional, exciting sports Arabic."""),
        ("user", "Topic: {topic}\n\nSearch Data Content:\n{results}")
    ])

    # Build and run the chain
    chain = prompt | llm
    response = chain.invoke({"topic": topic, "results": search_results})
    
    return response.content