from openfabric_sdk import Stub
import logging
from typing import Optional

class OpenfabricClient:
    def __init__(self, app_ids: list, user: str = "super-user"):
        self.stub = Stub(app_ids)
        self.user = user
        # These could be made configurable
        self.text_to_image_id = "f0997a01-d6d3-a5fe-53d8-561300318557"
        self.image_to_3d_id = "69543f29-4d41-4afc-7f29-3d51591f11eb"
        self.timeout = 30  # seconds

    def generate_image(self, prompt: str) -> bytes:
        """Generate image with timeout and proper error handling"""
        try:
            response = self.stub.call(
                self.text_to_image_id,
                {"prompt": prompt},
                self.user,
                timeout=self.timeout
            )
            if not response or not response.get("result"):
                raise ValueError("Invalid or empty response from image generation service")
            return response["result"]
        except Exception as e:
            logging.error(f"Image generation failed: {str(e)}")
            raise RuntimeError("Failed to generate image") from e

    def generate_3d_model(self, image_data: bytes) -> bytes:
        """Generate 3D model with timeout and proper error handling"""
        try:
            if not isinstance(image_data, bytes):
                raise ValueError("Image data must be bytes")
                
            response = self.stub.call(
                self.image_to_3d_id,
                {"image": image_data},
                self.user,
                timeout=self.timeout
            )
            if not response or not response.get("result"):
                raise ValueError("Invalid or empty response from 3D generation service")
            return response["result"]
        except Exception as e:
            logging.error(f"3D model generation failed: {str(e)}")
            raise RuntimeError("Failed to generate 3D model") from e