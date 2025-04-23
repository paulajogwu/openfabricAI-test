import streamlit as st
from llm import LLM
from openfabric import OpenfabricClient
from memory import Memory
import os

st.title("AI Developer Challenge: Creative Pipeline")

# Initialize components
llm = LLM()
memory = Memory()
openfabric = OpenfabricClient([])  # Adjust app_ids as needed

# Prompt input
prompt = st.text_input("Enter your creative prompt:", "Glowing dragon on a cliff at sunset")
if st.button("Generate"):
    # Enhance prompt
    enhanced_prompt = llm.enhance_prompt(prompt)
    st.write(f"Enhanced Prompt: {enhanced_prompt}")

    # Generate image
    image_data = openfabric.generate_image(enhanced_prompt)
    image_path = f"outputs/image_{prompt[:10]}.png"
    with open(image_path, 'wb') as f:
        f.write(image_data)
    st.image(image_path, caption="Generated Image")

    # Generate 3D model
    model_3d_data = openfabric.generate_3d_model(image_data)
    model_3d_path = f"outputs/model_3d_{prompt[:10]}.obj"
    with open(model_3d_path, 'wb') as f:
        f.write(model_3d_data)
    st.write(f"3D Model saved to: {model_3d_path}")

    # Save to memory
    memory.save_creation(prompt, enhanced_prompt, image_path, model_3d_path)

# Memory recall
recall_query = st.text_input("Recall previous creation (e.g., 'dragon'):")
if st.button("Recall"):
    results = memory.recall(recall_query)
    for result in results:
        st.write(f"Prompt: {result[1]}, Image: {result[3]}, 3D Model: {result[4]}, Time: {result[5]}")