import json
import base64

import requests, time


def submitPost(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def saveEncodedImage(b64_image: str, output_path: str):
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


if __name__ == "__main__":
    # txt2img_url = "http://webui.makeblock.com/sdapi/v1/txt2img"
    txt2img_url = "http://localhost:7861/sdapi/v1/txt2img"
    data = {
        "prompt": "a fox <lora:soulcard:1.0>",
        "negative_prompt": "badhandv4,EasyNegative",
        "override_settings": {
            "sd_model_checkpoint": "anything-v4.5.safetensors [1d1e459f9f]",
            "sd_vae": "orangemix.vae.pt",
        },
        "steps": 20,
        "n_iter": 1,
    }
    response = submitPost(txt2img_url, data)
    timestamp = int(time.time())
    images = response.json()["images"]
    for i, image in enumerate(images):
        filename = "girl_" + str(i) + ".png"
        saveEncodedImage(image, "./images/text2img/" + str(timestamp) + "_" + filename)
