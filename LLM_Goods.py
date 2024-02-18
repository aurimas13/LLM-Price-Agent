#!/usr/bin/env python
# coding: utf-8

# Step 1: Analyze the Data (Loading & Cleaning)

import requests
import json
import logging
import re
import pandas as pd
import spacy
import warnings
warnings.filterwarnings('ignore')
from bs4 import BeautifulSoup
from PIL import Image
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util

# Load and initial clean
import pandas as pd
from pathlib import Path

# Get the directory where the current script is located
current_dir = Path(__file__).parent

# Construct the path to 'products.csv' relative to the current script
file_path = '../products.csv'

# Now, read the CSV file
products_df = pd.read_csv(file_path, delimiter=';', usecols=['ID', 'Title', 'Description', 'Vendor', 'Type', 'Tags', 'Price'])

def clean_html(raw_html):
    if pd.isnull(raw_html):
        return ""
    clean_text = BeautifulSoup(raw_html, "html.parser").text
    return " ".join(clean_text.split())

products_df['Cleaned_Description'] = products_df['Description'].apply(clean_html)
products_df = products_df.dropna(subset=['Title'])
products_df = products_df[products_df['Cleaned_Description'].str.strip() != '']
products_df['Tags'] = products_df['Tags'].apply(lambda x: x.split(',') if pd.notnull(x) else [])

# Once spaCy is installed and the model is downloaded
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(lemmatized)

products_df['Processed_Description'] = products_df['Cleaned_Description'].apply(preprocess_text)

# 2. Extracting Features with Named Entity Recognition (NER)
# Extracting entities like materials, benefits from descriptions:

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

products_df['Entities'] = products_df['Cleaned_Description'].apply(extract_entities)

# Function to clean tags and convert them to lowercase
def clean_tags(tags):
    return [tag.lower().strip() for tag in tags]

# Clean the Tags and Type columns
products_df['Tags'] = products_df['Tags'].apply(lambda x: clean_tags(x) if isinstance(x, list) else [])
products_df['Type'] = products_df['Type'].str.lower().str.strip()

# Convert Price to numeric type for sorting
products_df['Price'] = pd.to_numeric(products_df['Price'], errors='coerce')

# Function to clean tags and convert them to lowercase
def clean_tags(tags):
    return [tag.lower().strip() for tag in tags]

# Clean the Tags and Type columns
products_df['Tags'] = products_df['Tags'].apply(lambda x: clean_tags(x) if isinstance(x, list) else [])
products_df['Type'] = products_df['Type'].str.lower().str.strip()

# Convert Price to numeric type for sorting
products_df['Price'] = pd.to_numeric(products_df['Price'], errors='coerce')


# 3. Integrating OpenAI's API for Enhanced Query Processing

client = OpenAI(api_key='your_api_key_here')

def process_query_with_gpt4(query):
    prompt = f"Parse the following user query to identify product attributes and price constraints: '{query}'. List attributes and any specific price constraints."
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f'Error processing query with GPT-4: {e}')
        return ""

model = SentenceTransformer('all-MiniLM-L6-v2')

# Assuming you've already encoded your product descriptions into embeddings
description_embeddings = model.encode(products_df['Processed_Description'].tolist(), convert_to_tensor=True)

def semantic_search_with_gpt4(query):
    # Process the query with GPT-4 to refine or expand it based on user intent
    processed_query = process_query_with_gpt4(query)
    query_embedding = model.encode(processed_query, convert_to_tensor=True)
    search_results = util.semantic_search(query_embedding, description_embeddings, top_k=5)
    
    matched_products = [products_df.iloc[hit['corpus_id']] for hit in search_results[0]]
    return pd.DataFrame(matched_products)

# Generating Dynamic Responses with GPT-4
# Utilize GPT-4's advanced text generation capabilities to create responses that are contextually relevant, detailed, and tailored to the user's query and the matched products.

def parse_gpt_response(response):
    attributes = re.findall(r"\battributes?:\s*([\w\s,]+)", response, re.I)
    min_price = re.search(r"\bmin(?:imum)? price:?\s*(\d+)", response, re.I)
    
    # Flatten attribute list and filter empty values
    attributes = [attr.strip() for sublist in attributes for attr in sublist.split(',') if attr.strip()]
    min_price = float(min_price.group(1)) if min_price else None

    return attributes, min_price

def search_products_by_attributes(attributes, min_price=None):
    # Filter products containing all the attributes
    filtered_products = products_df[
        products_df['Tags'].apply(lambda tags: all(attr in tags for attr in attributes)) |
        products_df['Type'].str.contains('|'.join(attributes), case=False, na=False)
    ]
    
    # Further filter by min price if specified
    if min_price is not None:
        filtered_products = filtered_products[filtered_products['Price'] >= min_price]
    
    # Sort by price
    sorted_products = filtered_products.sort_values(by='Price', ascending=True)
    
    return sorted_products


def generate_dynamic_response_with_gpt4(query):
    try:
        # Extract attributes and price constraints from the user's query
        processed_response = process_query_with_gpt4(query)
        
        # Parse the processed_response to get attributes and min_price
        attributes, min_price = parse_gpt_response(processed_response)

        # Search for products based on extracted attributes and price
        product_results = search_products_by_attributes(attributes, min_price)

        # Format the results into a response string
        response_string = "\n".join([f"{row['Title']}, Price: {row['Price']:.2f}" for index, row in product_results.iterrows()])

        return response_string if not product_results.empty else "No products found matching your criteria."
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')  # HTTP error
    except Exception as err:
        logging.error(f'Other error occurred: {err}')  # Other errors
    return "Error generating response. Please try again later."


# Sample query from the user
user_query = "I'm looking for eco-friendly skincare products with a minimum price of 20"

# Get the response from GPT-4
gpt_response = generate_dynamic_response_with_gpt4(user_query)

# Check and print the response from GPT-4
print(f"GPT-4 Response: {gpt_response}")

# Parse the response to extract attributes and min price
attributes, min_price = parse_gpt_response(gpt_response)

# Print the parsed information
print(f"Extracted Attributes: {attributes}")
print(f"Extracted Min Price: {min_price}")

# def process_query_with_gpt4(query):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4-turbo-preview",  # Specify GPT-4 as the model
#             prompt=f"Given the user query: '{query}', extract and list all mentioned product attributes such as category, color, and any price constraints. Format your response accordingly.",
#             temperature=0.5,
#             max_tokens=100)
#         return response.choices[0].text.strip()

         
#     # Extracting the latest message from the response, assuming it's the assistant's response
#         if response.choices and response.choices[0].message:
#             assistant_message = response.choices[0].message['content']
#         else:
#             assistant_message = "No response from GPT-4."
#         return assistant_message.strip()
#     except Exception as e:
#         logging.error(f'Error processing query with GPT-4: {e}')
#         return "I encountered an error processing your request. Please try again."


# def process_query_with_gpt4(query):
#     try:
#         # Make sure to replace 'your_api_key_here' with your actual OpenAI API key        
#         response = openai.Completion.create(
#             engine="gpt-4-turbo-preview",  # Use the correct engine identifier for GPT-4 once available
#             prompt=f"Given the user query: '{query}', extract and list all mentioned product attributes such as category, color, and any price constraints. Format your response accordingly.",
#             temperature=0.2,
#             max_tokens=150,
#             top_p=1.0,
#             frequency_penalty=0.0,
#             presence_penalty=0.0
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         logging.error(f'Error processing query with GPT-4: {e}')
#         return "I encountered an error processing your request. Please try again."