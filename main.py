from io import BytesIO
from typing import Union, Dict, List
from unstructured.partition.auto import partition
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import instructor
from openai import OpenAI
from dotenv import load_dotenv
import os


app = FastAPI()

load_dotenv()

openai_key = os.getenv("OPENAI_KEY")
client = instructor.from_openai(OpenAI(api_key=openai_key))


# request model
class FileURL(BaseModel):
    url: str


# Define your desired output structure using standard pydantic schema
class StructuredOutput(BaseModel):
    company_name: str


def _clean_chunk_text(text: str) -> str:
    return clean(
        text=text,
        extra_whitespace=True,
        dashes=True,
        bullets=True,
        trailing_punctuation=True,
    )


@app.post("/process", response_model=StructuredOutput)
async def process_file(file: FileURL):
    try:
        # Fetch the file from the URL
        response = requests.get(file.url)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=400, detail=f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error occurred: {err}")

    # Partition the file
    elements = partition(file=BytesIO(response.content))

    # Chunk the elements
    chunks = chunk_elements(elements=elements, max_characters=500)

    # Convert chunks to dictionary
    chunks_dict = [chunk.to_dict() for chunk in chunks]

    # Merge all the text into one string and clean it
    merged = _clean_chunk_text(" ".join([c["text"] for c in chunks_dict]))

    structured_response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_model=StructuredOutput,
        messages=[{"role": "user", "content": "Structure the given text: " + merged}],
    ).model_dump()

    return structured_response
