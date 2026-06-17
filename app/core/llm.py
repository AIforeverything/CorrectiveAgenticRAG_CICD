# loading  model using .env 
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

GROQ_MODEL=str(os.getenv("GROQ_MODEL"))
GROQ_MODEL2=str(os.getenv("GROQ_MODEL2"))
# print(groq_model)
# print(groq_model2)

llm=ChatGroq(
    model=GROQ_MODEL,
    temperature=0.1
)

llm2=ChatGroq(
    model=GROQ_MODEL2,
    temperature=0.1
)





