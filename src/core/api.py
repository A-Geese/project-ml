from dataclasses import dataclass
from typing import List, Tuple
import db.db as db
import numpy as np
import pandas as pd
import requests
from ai.model import ModelHandler
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from firecrawl import FirecrawlApp
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from sklearn.metrics.pairwise import cosine_similarity

from typing import Tuple
from pydantic import BaseModel, Field

alive = [
    "doug downey",
    "bhutila karpoche",
    "billy pang",
    "christine hogarth",
    "guy bourgouin",
    "andrew dowie",
    "karen mccrimmon",
    "stephane sarrazin",
    "stephen lecce",
    "jill dunlop",
    "george pirie",
    "goldie ghamari",
    "rudy cuzzetto",
    "john yakabuski",
    "kinga surma",
    "jennifer k french",
    "steve clark",
    "michael parsa",
    "lise vaugeois",
    "vincent ke",
    "jeff burch",
    "rob flack",
    "donna skelly",
    "caroline mulroney",
    "matthew rae",
    "lucille collard",
    "ric bresee",
    "doly begum",
    "joel harden",
    "nolan quinn",
    "michael mantha",
    "kristyn wong tam",
    "bobbi ann brady",
    "michael s kerzner",
    "sheref sabawy",
    "mike schreiner",
    "natalia kusendova bashta",
    "andrea khanjin",
    "teresa j armstrong",
    "effie j triantafilopoulos",
    "aris babikian",
    "sylvia jones",
    "france gelinas",
    "todd j mccarthy",
    "andrea hazell",
    "david piccini",
    "rick byers",
    "catherine fife",
    "jennifer jennie stevens",
    "stephen crawford",
    "prabmeet singh sarkaria",
    "jill andrew",
    "john vanthof",
    "jamie west",
    "michael d ford",
    "chandra pasma",
    "laurie scott",
    "david smith",
    "sol mamakwa",
    "lisa gretzky",
    "marit stiles",
    "peter tabuns",
    "doug ford",
    "ernie hardeman",
    "dawn gallagher murphy",
    "adil shamji",
    "daisy wai",
    "tom rakocevic",
    "lisa m thompson",
    "stephen blais",
    "jessica bell",
    "ted hsu",
    "lorne coe",
    "laura smith",
    "chris glover",
    "mary margaret mcmahon",
    "wayne gates",
    "monique taylor",
    "brian saunderson",
    "paul calandra",
    "brian riddell",
    "natalie pierre",
    "aislinn clancy",
    "mike harris",
    "deepak anand",
    "stephanie bowman",
    "john fraser",
    "peter bethlenfalvy",
    "terence kernaghan",
    "sandy shaw",
    "peggy sattler",
    "dave smith",
]


class SummarizePolicyRequest(BaseModel):
    url: str


class ModelRequest(BaseModel):
    persona_name_left: str
    persona_name_right: str
    topic: str  # immigration


class ModelResponse(BaseModel):
    chat_history: list
    evaluation: str


app = FastAPI()
model_handler = ModelHandler()
persona_db = db.get_db("src/database/personas_full.json")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # List the allowed origins (or ["*"] for all origins)
    allow_credentials=True,  # Allow cookies and authentication
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@dataclass
class Mpp:
    _id: int
    name: str
    party: str | None
    role: str | None
    location: str | None


@app.get("/all_mpps", response_model=list[Mpp])
def load_mpps() -> list[Mpp]:
    mpp_df = pd.read_csv("src/core/mpps.csv")
    mpp_df = mpp_df[mpp_df["role"].notna()]
    mpp_df = mpp_df[mpp_df["role"].apply(lambda x: isinstance(x, str))]

    mpps = []
    for i in range(len(mpp_df)):
        try:
            if mpp_df["name"][i] not in alive:
                continue

            mpp = Mpp(
                _id=i,
                name=mpp_df["name"][i],
                party=mpp_df["party"][i],
                role=mpp_df["role"][i],
                location=mpp_df["location"][i],
            )
            mpps.append(mpp)
        except Exception:
            continue
    return mpps


@app.post("/generate")
def generate(
    request: ModelRequest,
) -> ModelResponse:
    try:
        print(request)

        chat_history = []
        for round in range(5):
            persona_name_left: str = request.persona_name_left
            persona_name_right: str = request.persona_name_right
            topic: str = request.topic

            persona_left = db.get_agent_with_name(persona_db, persona_name_left)
            persona_right = db.get_agent_with_name(persona_db, persona_name_right)

            response1 = model_handler.generate(persona_left, chat_history, topic)

            if isinstance(response1, list):
                for r in response1:
                    chat_history.append(r)
            else:
                chat_history.append(response1)

            response2 = model_handler.generate(persona_right, chat_history, topic)

            if isinstance(response2, list):
                for r in response2:
                    chat_history.append(r)
            else:
                chat_history.append(response2)

        response_eval = model_handler.evaluate(chat_history, request.topic)

        return ModelResponse(chat_history=chat_history, evaluation=response_eval)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize_policy")
def summarize_policy(request: SummarizePolicyRequest):
    url = request.url
    try:
        app = FirecrawlApp(api_key="fc-d4f52d5c0584446aae60779f80a8a2d0")
        scrape_result = app.scrape_url(url, params={"formats": ["markdown"]})
        webpage_content = scrape_result["markdown"]
        # summarize here
        document = Document(text=webpage_content)

        node_parser = SentenceSplitter(chunk_size=5000, chunk_overlap=150)

        nodes = node_parser.get_nodes_from_documents([document], show_progress=False)
        chunks = [node.text for node in nodes]
        # llama_endpoint = "http://127.0.0.1:11435/api/generate"

        # headers = {"Content-Type": "application/json"}
        # Summarize each chunk
        summaries = []
        for chunk in chunks:
            prompt = f"{chunk}\n\nSummarize the above webpage content into a concise bullet point list."
            # response = requests.post(llama_endpoint, headers=headers, json=data)
            # try:
            #     summary = response.json()["choices"][0]["text"]
            # except Exception as e:
            #     print(e)
            summary = model_handler.llama_predict(prompt)

            summaries.append(summary)

        # Summarize the entire webpage
        # data = {
        #     "model": "llama3.1:70b",
        #     "prompt": ,
        #     "stream": False,
        # }

        prompt = f"{chr(10).join(summaries)}\n\nSummarize the above webpage content into a concise bullet point list."

        # response = requests.post(llama_endpoint, headers=headers, json=data)

        response = model_handler.llama_predict(prompt)
        return response
    except requests.exceptions.RequestException as e:
        return e


# @app.post("/get_similar_bills")
# def get_similar_bills(summary: str) -> List[Tuple[str, str]]:
#     try:
#         # Load the dataset
#         df = pd.read_csv("data/bills.csv")
#         texts = (df["bill_name"] + "\n" + df["explanatory_notes"]).tolist()

#         # Import ollama and compute embeddings
#         import ollama

#         # Get embeddings for the bills
#         bill_embeddings = []
#         for text in texts:
#             emb = ollama.embeddings(model="nomic-embed-text", prompt=text)["embedding"]
#             bill_embeddings.append(emb)

#         # Get the embedding for the input summary
#         summary_embedding = ollama.embeddings(model="nomic-embed-text", prompt=summary)[
#             "embedding"
#         ]

#         # Compute cosine similarities
#         similarities = cosine_similarity([summary_embedding], bill_embeddings)[0]

#         # Find the 3 most similar bills
#         top_indices = np.argsort(similarities)[-3:][::-1]
#         closest_bills = [
#             (df.iloc[i]["bill_name"], df.iloc[i]["explanatory_notes"])
#             for i in top_indices
#         ]

#         return closest_bills

#     except Exception as e:
#         return str(e)
