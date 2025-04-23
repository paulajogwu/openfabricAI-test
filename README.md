# openfabricAI-test

# AI Developer Challenge

An end-to-end pipeline that transforms text prompts into images and 3D models using a local LLM and Openfabric apps, with memory functionality.

## Setup
1. Install dependencies: `poetry install `
2. Run locally: `./start.sh``
3. Access Swagger UI: `http://localhost:8888/swagger-ui`
4. Run UI: `streamlit run ui.py`

## Usage
- Enter a prompt (e.g., "Glowing dragon on a cliff at sunset") via Swagger or Streamlit UI.
- The pipeline enhances the prompt, generates an image, converts it to a 3D model, and stores the results.
- Recall past creations with queries like "dragon".

