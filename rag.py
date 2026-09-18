import os
import json
import numpy as np
import faiss

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Load FAISS index
index = faiss.read_index("faiss_index.bin")


# Load chunks
with open("chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

# We created embeddings for the first 100 chunks
chunks = chunks[:100]


def search_knowledge(query, top_k=3):

    # Create embedding for the question
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    query_embedding = np.array(
        [result.embeddings[0].values],
        dtype="float32"
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


def analyze_environment(profile, question, chat_history=None):

    profile_text = f"""
    Soil pH: {profile['soil_ph']}
    Soil organic carbon: {profile['organic_carbon']}
    Rainfall: {profile['rainfall']} mm
    Temperature: {profile['temperature']} °C
    Land use: {profile['land_use']}
    Soil moisture: {profile['soil_moisture']}
    Pollution level: {profile['pollution']}
    Deforestation level: {profile['deforestation']}
    """

    conversation_text = ""

    if chat_history:

        for message in chat_history:

            conversation_text += (
                message["role"]
                + ": "
                + message["content"]
                + "\n"
            )

    # Retrieve scientific evidence
    retrieved_chunks = search_knowledge(
        question + "\n" + profile_text
    )

    # Combine retrieved knowledge
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    You are an AI biodiversity scientist.

    Environmental profile:
    {profile_text}

    Previous conversation:
    {conversation_text}

    Scientific evidence:
    {context}

    Current user question:
    {question}

    Use the previous conversation to understand follow-up questions.

    If the user asks something like:
    "What if rainfall increases?"

    understand that it refers to the environmental profile
    and previous discussion.

    Your response must contain:

    1. Recommendation
    2. Scientific reasoning
    3. Impacted environmental metrics
    4. Expected time horizon
        Only provide a specific number of years if the scientific evidence
        supports that timeframe.

        Otherwise use:
        "Time horizon cannot be determined from the retrieved evidence."

        Do not invent a timeframe.
    5. Evidence source
    6. Confidence level

    Connect at least three environmental variables when explaining
    the biodiversity impact.

    Do not invent scientific evidence.
    If the provided evidence is insufficient, clearly say so.

    Answer in simple and clear language.
    """
    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return response.output_text
