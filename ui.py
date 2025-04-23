import streamlit as st
from llm import LLM
from openfabric import OpenfabricClient
from memory import Memory
import os
from datetime import datetime

# App configuration
st.set_page_config(page_title="Creative Pipeline", layout="wide")

@st.cache_resource
def load_components():
    """Cache components for better performance"""
    return {
        'llm': LLM(),
        'memory': Memory(),
        'openfabric': OpenfabricClient([])
    }

def main():
    st.title("🎨 AI Creative Pipeline")
    st.markdown("Transform text prompts into images and 3D models")
    
    components = load_components()
    
    # Input section
    with st.form("generation_form"):
        prompt = st.text_area(
            "Describe what you want to create:",
            "Glowing dragon on a cliff at sunset",
            height=100
        )
        submitted = st.form_submit_button("Generate")
    
    if submitted and prompt:
        with st.spinner("Creating your artwork..."):
            try:
                # Enhance prompt
                enhanced_prompt = components['llm'].enhance_prompt(prompt)
                with st.expander("Enhanced Prompt"):
                    st.write(enhanced_prompt)
                
                # Generate image
                image_data = components['openfabric'].generate_image(enhanced_prompt)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = f"outputs/image_{timestamp}.png"
                
                os.makedirs('outputs', exist_ok=True)
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                
                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.image(image_path, caption="Generated Image", use_column_width=True)
                
                # Generate 3D model
                with col2:
                    with st.spinner("Generating 3D model..."):
                        model_3d_data = components['openfabric'].generate_3d_model(image_data)
                        model_3d_path = f"outputs/model_3d_{timestamp}.obj"
                        with open(model_3d_path, 'wb') as f:
                            f.write(model_3d_data)
                        st.success("3D Model Generated!")
                        st.download_button(
                            "Download 3D Model",
                            model_3d_data,
                            file_name=f"model_{timestamp}.obj",
                            mime="application/octet-stream"
                        )
                
                # Save to memory
                components['memory'].save_creation(prompt, enhanced_prompt, image_path, model_3d_path)
                st.success("Creation saved successfully!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Memory recall section
    st.divider()
    st.header("📚 Previous Creations")
    
    search_query = st.text_input("Search your creations:")
    if st.button("Search") and search_query:
        try:
            results = components['memory'].recall(search_query)
            if not results:
                st.warning("No matching creations found")
            else:
                for result in results:
                    with st.expander(f"Creation from {result[5]}"):
                        st.write(f"**Original:** {result[1]}")
                        if result[3] and os.path.exists(result[3]):
                            st.image(result[3], width=300)
        except Exception as e:
            st.error(f"Search failed: {str(e)}")

if __name__ == "__main__":
    main()