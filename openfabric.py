import os
from openfabric_pysdk import sub
import logging
from dotenv import load_dotenv

load_dotenv()

class OpenfabricClient:
    def __init__(self, app_ids: list, user: str = None):
        self.user = user or os.getenv("OPENFABRIC_USER", "super-user")
        try:
            self.stub = Stub(app_ids)
            # Placeholder for dynamic app ID fetching
            # Future improvement: Fetch app IDs and schemas from Openfabric API
            self.text_to_image_id = os.getenv("TEXT_TO_IMAGE_ID", "f0997a01-d6d3-a5fe-53d8-561300318557")
            self.image_to_3d_id = os.getenv("IMAGE_TO_3D_ID", "69543f29-4d41-4afc-7f29-3d51591f11eb")
        except Exception as e:
            logging.error(f"Failed to initialize OpenfabricClient: {e}")
            raise

    def generate_image(self, prompt: str) -> bytes:
        try:
            response = self.stub.call(self.text_to_image_id, {"prompt": prompt}, self.user)
            image_data = response.get("result")
            if not image_data:
                raise ValueError("Failed to generate image")
            return image_data
        except Exception as e:
            logging.error(f"Image generation failed: {e}")
            raise

    def generate_3d_model(self, image_data: bytes) -> bytes:
        try:
            response = self.stub.call(self.image_to_3d_id, {"image": image_data}, self.user)
            model_data = response.get("result")
            if not model_data:
                raise ValueError("Failed to generate 3D model")
            return model_data
        except Exception as e:
            logging.error(f"3D model generation failed: {e}")
            raise