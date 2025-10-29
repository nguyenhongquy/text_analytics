import os

from fastapi import FastAPI
from pydantic import BaseModel
import utils
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

headers = {
    "Ocp-Apim-Subscription-Key": os.getenv("AZURE_TEXT_ANALYTICS_KEY"),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

base_endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT") + "/text/analytics/v3.1/"

body = {
    "documents": [
        {
            "language": "en",
            "id": "1",
            "text": "Great atmosphere. Close to plenty of restaurants, hotels, and transit! Staff are friendly and helpful."
        },
        {
            "language": "en",
            "id": "2",
            "text": "Bad atmosphere. Not close to plenty of restaurants, hotels, and transit! Staff are not friendly and helpful."
        }
    ]
}



class Model(BaseModel):
    text_to_analyze: list

@app.post("/")
def analyze_text(text: Model):
    response = {"sentiment": [], "keyphrases": []}
    no_of_text = len(text.text_to_analyze)
    for i in range(no_of_text):
        document = {"documents": [{"id": i+1, "language": "en", "text": text.text_to_analyze[i]}]}
        
        sentiment = utils.call_text_analytics_api(headers, document, endpoint= base_endpoint + 'sentiment')
        keyphrases = utils.call_text_analytics_api(headers, document, endpoint=base_endpoint +'keyPhrases')
        
        response["sentiment"].append(sentiment["documents"][0])
        response["keyphrases"].append(keyphrases["documents"][0])
    return response

# For testing - add this at the bottom
if __name__ == "__main__":
    import requests as req
    # Run sentiment analysis directly when script is executed
    body = {
        "documents": [
            {
                "language": "en",
                "id": "1",
                "text": "Great atmosphere. Close to plenty of restaurants!"
            },
            {
                "language": "en",
                "id": "2", 
                "text": "Bad atmosphere. Not close to restaurants!"
            }
        ]
    }

    
    print("Running sentiment analysis...")
    response = req.post(sentiment_endpoint, headers=headers, json=body)
    result = response.json()
    
    for doc in result["documents"]:
        print(f"Document {doc['id']}: Sentiment: {doc['sentiment']}")
