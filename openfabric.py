from openfabric_sdk import Stub
import logging

class OpenfabricClient:
    def __init__(self, app_ids: list, user: str = "super-user"):
        self.stub = Stub(app_ids)
        self.user = user
        self.text_to_image_id = "f0997a01-d6d3-a5fe-53d8-561300318557"
        self.image_to_3d_id = "69543f29-4d41-4afc-7f29-3d51591f11eb"

    def generate_image(self, prompt: str) -> bytes:
        response = self.stub.call(self.text_to_image_id, {"prompt": prompt}, self.user)
        image_data = response.get("result")
        if not image_data:
            raise ValueError("Failed to generate image")
        return image_data

    def generate_3d_model(self, image_data: bytes) -> bytes:
        response = self.stub.call(self.image_to_3d_id, {"image": image_data}, self.user)
        model_data = response.get("result")
        if not model_data:
            raise ValueError("Failed to generate 3D model")
        return model_data