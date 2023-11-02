import json
import base64

import requests, time


def submitPost(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def decodeImage(b64_image: str, output_path: str):
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


def encoderImage(imgDir: str):
    image = open(imgDir, "rb")
    image_base64 = base64.b64encode(image.read()).decode("utf-8")
    image.close()
    return image_base64


if __name__ == "__main__":
    img2img_url = "http://webui.makeblock.com/sdapi/v1/img2img"
    init_image = encoderImage("./images/girl.jpg")
    mask_image_base64 = encoderImage("./images/girl_mask.jpg")
    data = {
        "init_images": [init_image],
        "mask": mask_image_base64,
        "override_settings": {
            "sd_model_checkpoint": "anything-v4.5-inpainting.safetensors [6d9a152b7a]",
            "sd_vae": "orangemix.vae.pt",
        },
        "prompt": "a pair of glasses",
        "steps": 20,
        "n_iter": 1,
        "resize_mode": 1,
        "inpaint_full_res": True,
        "inpainting_mask_invert": 1,
    }
    response = submitPost(img2img_url, data)
    timestamp = int(time.time())
    images = response.json()["images"]
    for i, image in enumerate(images):
        filename = "inpainting_girl_" + str(i) + ".png"
        decodeImage(image, "./images/img2img/" + str(timestamp) + "_" + filename)
