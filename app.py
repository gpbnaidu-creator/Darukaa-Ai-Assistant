import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

from chat_memory import (
    initialize_chat,
    add_message,
    get_chat_history
)

from rag import analyze_environment


st.set_page_config(
    page_title="Darukaa Ai",
)


st.title(" Darukaa Ai")
st.subheader("AI Biodiversity Assistant")


initialize_chat()


st.write("### Environmental Profile")


soil_ph = st.number_input(
    "Soil pH",
    min_value=0.0,
    max_value=14.0,
    value=5.2
)


organic_carbon = st.number_input(
    "Soil Organic Carbon",
    min_value=0.0,
    value=0.8
)


rainfall = st.number_input(
    "Rainfall (mm)",
    min_value=0.0,
    value=600.0
)


temperature = st.number_input(
    "Temperature (°C)",
    value=29.0
)

soil_moisture = st.selectbox(
    "Soil Moisture",
    [
        "Low",
        "Moderate",
        "High"
    ]
)


land_use = st.selectbox(
    "Land Use",
    [
        "Agriculture",
        "Forest",
        "Urban",
        "Grassland",
        "Wetland"
    ]
)

pollution = st.selectbox(
    "Pollution Level",
    [
        "Low",
        "Moderate",
        "High"
    ]
)


deforestation = st.selectbox(
    "Deforestation Level",
    [
        "Low",
        "Moderate",
        "High"
    ]
)

st.write("### Structured Environmental Profile")

st.caption(
    "Enter environmental measurements and conditions "
    "to create a structured profile."
)




st.write("### Ask the Biodiversity Assistant")


question = st.text_input(
    "Ask a question about your environment"
)

def fallback_response(profile, question, chat_history):

    question_lower = question.lower()

    # Follow-up about increased rainfall
    if "rainfall" in question_lower and (
        "increase" in question_lower
        or "increases" in question_lower
        or "more rain" in question_lower
        or "higher" in question_lower
    ):

        return f"""
### Recommendation

If rainfall increases, monitor soil moisture and drainage carefully.
Maintain vegetation or ground cover to reduce runoff and soil erosion.

### Scientific Reasoning

Higher rainfall can change soil moisture conditions and water
availability. In an agricultural system, this interacts with
soil organic carbon, soil pH, temperature, and land use.

Your current rainfall is **{profile['rainfall']} mm** and your soil
moisture is **{profile['soil_moisture']}**.

If rainfall increases substantially, excess water may increase
runoff or erosion, while vegetation cover can help protect the soil
and support soil biodiversity.

### Impacted Environmental Metrics

- Rainfall
- Soil moisture
- Soil organic carbon
- Land use
- Biodiversity

### Expected Time Horizon

The exact time horizon cannot be determined from the available
evidence.

### Evidence Source

FAO — The State of the World's Biodiversity for Food and Agriculture (2019).

### Confidence

Medium

*Gemini is temporarily unavailable. This is a context-aware
fallback response based on the environmental profile.*
"""

    # Follow-up about soil moisture
    if "moisture" in question_lower:

        return f"""
### Recommendation

Monitor soil moisture and maintain vegetation cover appropriate
for the land-use conditions.

### Scientific Reasoning

Soil moisture interacts with rainfall, soil organic carbon,
temperature, and land use. Changes in moisture can affect soil
conditions and organisms that contribute to soil biodiversity.

Your current soil moisture is **{profile['soil_moisture']}** and
rainfall is **{profile['rainfall']} mm**.

### Impacted Environmental Metrics

- Soil moisture
- Rainfall
- Soil organic carbon
- Temperature
- Biodiversity

### Expected Time Horizon

The exact time horizon cannot be determined from the available
evidence.

### Evidence Source

FAO — The State of the World's Biodiversity for Food and Agriculture (2019).

### Confidence

Medium

*Gemini is temporarily unavailable. This is a context-aware
fallback response.*
"""

    # Follow-up about pollution
    if "pollution" in question_lower:

        return f"""
### Recommendation

Reduce pollution sources where possible and protect vegetation
and soil cover around the agricultural area.

### Scientific Reasoning

Pollution can interact with land use and soil conditions and may
affect organisms that contribute to ecosystem functioning.

Your current pollution level is **{profile['pollution']}**.

### Impacted Environmental Metrics

- Pollution
- Soil organic carbon
- Land use
- Soil biodiversity

### Expected Time Horizon

The exact time horizon cannot be determined from the available
evidence.

### Evidence Source

FAO — The State of the World's Biodiversity for Food and Agriculture (2019).

### Confidence

Medium

*Gemini is temporarily unavailable. This is a context-aware
fallback response.*
"""

    # General fallback
    return f"""
### Recommendation

Consider biodiversity-friendly land management practices such as
maintaining vegetation cover, reducing unnecessary soil disturbance,
and improving soil organic matter.

### Scientific Reasoning

The environmental conditions should be considered together.
Your current profile includes:

- Soil pH: {profile['soil_ph']}
- Soil organic carbon: {profile['organic_carbon']}
- Rainfall: {profile['rainfall']} mm
- Temperature: {profile['temperature']} °C
- Soil moisture: {profile['soil_moisture']}
- Land use: {profile['land_use']}
- Pollution: {profile['pollution']}
- Deforestation: {profile['deforestation']}

These variables can interact to influence soil conditions,
habitat quality, and biodiversity.

### Impacted Environmental Metrics

- Soil organic carbon
- Soil pH
- Soil moisture
- Rainfall
- Temperature
- Land use
- Pollution
- Deforestation

### Expected Time Horizon

The exact time horizon cannot be determined from the available
evidence.

### Evidence Source

FAO — The State of the World's Biodiversity for Food and Agriculture (2019).

### Confidence

Medium

*Gemini is temporarily unavailable. This is a context-aware
fallback response.*
"""

if st.button("Analyze"):

    profile = {
        "soil_ph": soil_ph,
        "organic_carbon": organic_carbon,
        "rainfall": rainfall,
        "temperature": temperature,
        "land_use": land_use,
        "soil_moisture": soil_moisture,
        "pollution": pollution,
        "deforestation": deforestation
    }

    st.write("### Generated JSON Profile")

    st.json(profile)
    chat_history = get_chat_history()


    try:
        answer = analyze_environment(
            profile,
            question,
            chat_history
        )

    except Exception:
        answer = fallback_response(
            profile,
            question,
            chat_history
        )


    add_message("user", question)


    add_message(
        "assistant",
        answer
    )


st.write("### Conversation")


for message in get_chat_history():

    if message["role"] == "user":

        st.markdown(
            "**👤 You:** " + message["content"]
        )

    else:

        st.markdown(
            "** AI Biodiversity Bot:**"
        )

        st.write(message["content"])