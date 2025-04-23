from transformers import pipeline
import logging

class LLM:
    def __init__(self, model_name="DeepSeek/DeepSeek-RAG"):
        self.generator = pipeline('text-generation', model=model_name, device=0)
        logging.info(f"Initialized LLM: {model_name}")

    def enhance_prompt(self, prompt: str) -> str:
        instruction = f"Expand this prompt into a vivid, detailed description for image generation: {prompt}"
        response = self.generator(instruction, max_length=200, num_return_sequences=1)[0]['generated_text']
        return response.strip()