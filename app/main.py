from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from LLM_Goods_Before import generate_dynamic_response_with_gpt4
import sys
# Now you can import LLM_Goods
from LLM_Goods import generate_dynamic_response_with_gpt4, process_query_with_gpt4, parse_gpt_response, search_products_by_attributes
import pandas as pd
import requests
import json
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

app = FastAPI()

class Query(BaseModel):
    query: str

# @app.post("/chat/")
# async def chat(query: Query):
#     # Process the query with GPT-4
#     response = generate_dynamic_response_with_gpt4(query.query)
#     return {"response": response}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat/")
async def chat(query: Query):
    processed_response = process_query_with_gpt4(query.query)
    attributes, min_price = parse_gpt_response(processed_response)
    
    # If attributes are extracted, perform a pgvector search
    if attributes:
        # Convert attributes to a query string and encode it
        query_string = ' '.join(attributes)
        query_embedding = model.encode(query_string, convert_to_tensor=True)
        
        # Perform the search
        search_results = pgvector_search(query_embedding, top_k=5)
        
        # Format the search results
        response = "\n".join([format_product_response(row) for row in search_results])
    else:
        response = "I couldn't understand the query. Could you please specify what product features you are interested in?"
    
    return {"response": response}
async def chat(query: Query):
    # processed_response = process_query_with_gpt4(query.query)
    # attributes, min_price = parse_gpt_response(processed_response)
    response = generate_dynamic_response_with_gpt4(query.query)
    # if attributes or min_price is not None:
    #     product_results = search_products_by_attributes(attributes, min_price)
    #     if not product_results.empty:
    #         response = "\n".join([f"{row['Title']}, Price: {row['Price']:.2f}" for index, row in product_results.iterrows()])
    #     else:
    #         response = "No products found matching your criteria."
    # else:
    #     response = "I couldn't understand the query. Could you please specify what product features you are interested in?"
    
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
