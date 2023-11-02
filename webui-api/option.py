import json
import base64

import requests, time


def submit_post(url: str, data: dict):
    """
    Submit a POST request to the given URL with the given data.
    """
    return requests.post(url, data=json.dumps(data))


if __name__ == "__main__":
    option_url = "http://webui.makeblock.com/sdapi/v1/options"
    option_payload = {
        "sd_model_checkpoint": "anything-v4.5-inpainting.safetensors [6d9a152b7a]",
        "sd_vae": "orangemix.vae.pt",
    }
    response = submit_post(option_url, option_payload)
    print(response.status_code)
