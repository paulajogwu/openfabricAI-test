from transformers import pipeline
import logging
import torch

class LLM:
    def __init__(self, model_name="gpt2"):  # Changed to more widely available model
        try:
            self.device = 0 if torch.cuda.is_available() else -1
            self.generator = pipeline(
                'text-generation', 
                model=model_name,
                device=self.device,
                torch_dtype=torch.float16 if self.device == 0 else torch.float32
            )
            logging.info(f"Initialized LLM: {model_name} on {'GPU' if self.device == 0 else 'CPU'}")
        except Exception as e:
            logging.error(f"Failed to initialize LLM: {str(e)}")
            raise

    def enhance_prompt(self, prompt: str) -> str:
        try:
            instruction = f"Expand this prompt into a vivid, detailed description for image generation: {prompt}"
            response = self.generator(
                instruction,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )[0]['generated_text']
            return response.strip()
        except Exception as e:
            logging.error(f"Prompt enhancement failed: {str(e)}")
            # Fallback to original prompt with basic enhancements
            return f"{prompt}, highly detailed, digital art, 4K resolution, trending on artstation"