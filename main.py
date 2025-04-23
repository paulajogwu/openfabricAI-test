import logging
import os
from datetime import datetime
from llm import LLM
from openfabric import OpenfabricClient
from memory import Memory
from openfabric_sdk import Stub, InputClass, OutputClass, ConfigClass

def execute(model) -> None:
    try:
        # Initialize components with error handling
        llm = LLM()
        memory = Memory()
        request: InputClass = model.request
        
        # Config handling with defaults
        user_config = getattr(model, 'configurations', {}).get('super-user', {})
        app_ids = user_config.get('app_ids', [])
        
        openfabric = OpenfabricClient(app_ids)

        # Get user prompt with validation
        prompt = getattr(request, 'prompt', '')
        if not prompt.strip():
            raise ValueError("Empty prompt provided")
            
        logging.info(f"Received prompt: {prompt}")

        # Enhance prompt with error handling
        enhanced_prompt = llm.enhance_prompt(prompt)
        logging.info(f"Enhanced prompt: {enhanced_prompt}")

        # Create outputs directory safely
        os.makedirs('outputs', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Generate image
        image_data = openfabric.generate_image(enhanced_prompt)
        image_path = f"outputs/image_{timestamp}.png"
        with open(image_path, 'wb') as f:
            f.write(image_data)
        logging.info(f"Image saved to {image_path}")

        # Generate 3D model
        model_3d_data = openfabric.generate_3d_model(image_data)
        model_3d_path = f"outputs/model_3d_{timestamp}.obj"
        with open(model_3d_path, 'wb') as f:
            f.write(model_3d_data)
        logging.info(f"3D model saved to {model_3d_path}")

        # Save to memory
        memory.save_creation(prompt, enhanced_prompt, image_path, model_3d_path)

        # Prepare response
        response: OutputClass = model.response
        response.message = f"Created image at {image_path} and 3D model at {model_3d_path}"
        response.success = True
        
    except Exception as e:
        logging.error(f"Error in execute: {str(e)}")
        response: OutputClass = model.response
        response.message = f"Error: {str(e)}"
        response.success = False