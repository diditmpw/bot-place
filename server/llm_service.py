import requests
from typing import Dict, Union

class LLMService:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama3"
        
    async def process_query(self, query: str) -> Dict[str, Union[str, bool]]:
        # First check if query is about a place
        intention_prompt = f"""You are a helpful AI assistant. First determine if the query is about a location, place, or directions.
        If it is about a location, respond with 'YES'.
        If it's not about a location, provide a natural, helpful response to the query.
        Do not mention anything about locations or explain why it's not a location query.

        Query: {query}"""
        
        try:
            # Check intention first
            intention_response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": intention_prompt,
                    "stream": False
                }
            ).json()["response"].lower()
            
            if intention_response != 'yes':
                return {
                    "is_place_query": False,
                    "response": intention_response.strip()
                }
            else:
                return {
                    "is_place_query": True,
                    "response": query
                }
            
        # If any error occurs, fallback to conversational response                
        except Exception as e:
            print(f"LLM Error: {e}")
            return {
                "is_place_query": False,
                "response": "I'm having trouble understanding. Could you rephrase that?"
            }