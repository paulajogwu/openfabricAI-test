import logging
import os
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self, model_name=None):
        self.model_name = model_name or os.getenv("LLM_MODEL", "distilgpt2")  # Fallback to distilgpt2
        try:
            self.generator = pipeline('text-generation', model=self.model_name, device=-1)  # CPU fallback
            logging.info(f"Initialized LLM: {self.model_name}")
        except Exception as e:
            logging.error(f"Failed to initialize LLM: {e}")
            raise

    def enhance_prompt(self, prompt: str) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            logging.error("Invalid prompt provided")
            raise ValueError("Prompt must be a non-empty string")
        instruction = f"Expand this prompt into a vivid, detailed description for image generation: {prompt}"
        try:
            response = self.generator(instruction, max_length=int(os.getenv("MAX_LENGTH", 200)), num_return_sequences=1)[0]['generated_text']
            return response.strip()
        except Exception as e:
            logging.error(f"Failed to enhance prompt: {e}")
            raise