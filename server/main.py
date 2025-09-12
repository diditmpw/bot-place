from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import googlemaps
from dotenv import load_dotenv
import os
from llm_service import LLMService

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('CLIENT_URL')],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["*"],
    max_age=3600,
)

# Initialize services
llm_service = LLMService()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

class PlaceQuery(BaseModel):
    query: str

@app.post("/api/places/search")
async def search_place(query: PlaceQuery):
    try:
        # Process query through LLM
        llm_result = await llm_service.process_query(query.query)
        
        print(f"LLM result: {llm_result}")

        # Prepare base response
        response_data = {
            "type": "conversation",
            "name": "",
            "address": "",
            "location": {"lat": 0, "lng": 0},
            "place_id": "",
            "rating": 0,
            "response": ""
        }
        
        # If not a place query, return conversational response
        if not llm_result["is_place_query"]:
            response_data["response"] = llm_result["response"]
            return JSONResponse(
                content=response_data,
                headers={
                    "Access-Control-Allow-Origin": os.getenv("CLIENT_URL"),
                    "Access-Control-Allow-Credentials": "true"
                }
            )
        
        # If it is a place query, proceed with Google Maps search
        places_result = gmaps.places(llm_result["response"])
        
        if not places_result['results']:
            response_data["response"] = "I couldn't find that place. Could you provide more details?"
            return JSONResponse(content=response_data)
            
        # Get the first result
        place = places_result['results'][0]
        location = place['geometry']['location']
        
        return JSONResponse(
            content={
                "type": "place",
                "name": place['name'],
                "address": place.get('formatted_address', ''),
                "location": location,
                "place_id": place['place_id'],
                "rating": place.get('rating', 0),
                "response": f"{place['name']} <br /> {place.get('formatted_address', '')}"
            },
            headers={
                "Access-Control-Allow-Origin": os.getenv('CLIENT_URL'),
                "Access-Control-Allow-Credentials": "true"
            }
        )
        
    except Exception as e:
        print(f"Error in search_place: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An error occurred while processing your request"},
            headers={
                "Access-Control-Allow-Origin": os.getenv("CLIENT_URL"),
                "Access-Control-Allow-Credentials": "true"
            }
        )

@app.options("/api/places/search")
async def options_place_search():
    return Response(
        content="",
        headers={
            "Access-Control-Allow-Origin": os.getenv("CLIENT_URL"),
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)