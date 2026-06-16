# loading  model using .env 
import os
from dotenv import load_dotenv
load_dotenv()

groq_model=str(os.getenv("GROQ_MODEL"))
groq_model2=str(os.getenv("GROQ_MODEL2"))
# print(groq_model)
# print(groq_model2)
from langchain_groq import ChatGroq
llm=ChatGroq(
    model=groq_model,
    temperature=0.1
)

llm2=ChatGroq(
    model=groq_model2,
    temperature=0.1
)





