from langchain_groq import ChatGroq
from src.prompt_template import PromptTemplates

class Recommender:
    def __init__(self,api_key:str,model_name:str):
        self.llm=ChatGroq(api_key=api_key,model_name=model_name,temperature=0)
        self.template = PromptTemplates.recommendation_explanation()[0]
    
    def explain(self,series_title: str,explanation_context: str) -> str:
            prompt = self.template.format(
                series_title=series_title,
                context=explanation_context,
            )
            response = self.llm.invoke(prompt)
            return response.content

    