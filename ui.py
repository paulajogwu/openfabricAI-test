import streamlit as st
import os
from datetime import datetime
from llm import LLM
from openfabric import OpenfabricClient
from memory import Memory
import logging
from dotenv import load_dotenv

load_dotenv()

st.title("AI Developer Challenge: Creative Pipeline")

# Initialize components
try:
    llm = LLM()
    memory = Memory()
    app_ids = os.getenv("OPENFABRIC_APP_IDS", "").split(",") if os.getenv("OPENFABRIC_APP_IDS") else []
    openfabric = OpenfabricClient(app_ids)
except Exception as e:
    st.error(f"Initialization failed: {e}")
    st.stop()

# Prompt input
prompt = st.text_input("Enter your creative prompt:", "Glowing dragon on a cliff at sunset")
if st.button("Generate"):
    try:
        # Enhance prompt
        enhanced_prompt = llm.enhance_prompt(prompt)
        st.write(f"Enhanced Prompt: {enhanced_prompt}")

        # Generate image
        image_data = openfabric.generate_image(enhanced_prompt)
        os.makedirs('outputs', exist_ok=True)
        image_path = f"outputs/image_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
        with open(image_path, 'wb') as f:
            f.write(image_data)
        st.image(image_path, caption="Generated Image")

        # Generate 3D model
        model_3d_data = openfabric.generate_3d_model(image_data)
        model_3d_path = f"outputs/model_3d_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.obj"
        with open(model_3d_path, 'wb') as f:
            f.write(model_3d_data)
        st.write(f"3D Model saved to: {model_3d_path}")
        # Placeholder for 3D visualization
        st.info("3D visualization not implemented. Use an external viewer (e.g., Blender) to view the OBJ file.")

        # Save to memory
        memory.save_creation(prompt, enhanced_prompt, image_path, model_3d_path)
        st.success("Creation saved successfully!")
    except Exception as e:
        st.error(f"Generation failed: {e}")

# Memory recall
recall_query = st.text_input("Recall previous creation (e.g., 'dragon'):")
if st.button("Recall"):
    try:
        results = memory.recall(recall_query)
        if results:
            for result in results:
                st.write(f"Prompt: {result[1]}, Image: {result[3]}, 3D Model: {result[4]}, Time: {result[5]}")
        else:
            st.warning("No matching creations found.")
    except Exception as e:
        st.error(f"Recall failed: {e}")