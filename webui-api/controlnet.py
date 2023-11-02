import json
import base64

import requests, time


def submitPost(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def saveEncodedImage(b64_image: str, output_path: str):
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


def encoderImage(imgDir: str):
    image = open(imgDir, "rb")
    image_base64 = base64.b64encode(image.read()).decode("utf-8")
    image.close()
    return image_base64


if __name__ == "__main__":
    txt2img_url = "http://webui.makeblock.com/sdapi/v1/txt2img"
    init_image = encoderImage("./images/xcs.png")
    data = {
        "prompt": "Simple background,Pipes, precision machinery,white background, <lora:animeoutlineV4_16:0.4> <lora:penink:0.3>",
        "negative_prompt": "low quality, worst quality,",
        "override_settings": {
            "sd_model_checkpoint": "meinamix_meinaV11.safetensors [54ef3e3610]",
            "CLIP_stop_at_last_layers": 2,
        },
        "steps": 24,
        "n_iter": 2,
        "batch_size": 1,
        "cfg_scale": 9.5,
        "sampler_index": "DPM++ SDE Karras",
        "width": 768,
        "height": 512,
        "enable_hr": True,
        "hr_scale": 1.5,
        "hr_upscaler": "R-ESRGAN 4x+",
        "hr_second_pass_steps": 10,
        "denoising_strength": 0.3,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "enable": True,
                        "module": "canny",
                        "weight": 1,
                        "model": "control_v11p_sd15_canny [d14c016b]",
                        "input_image": init_image,
                        "processor_res": -1,
                        "threshold_a": -1,
                        "threshold_b": -1,
                        "resize_mode": 1,
                        "control_mode": 0,
                    }
                ]
            }
        },
    }
    response = submitPost(txt2img_url, data)
    timestamp = int(time.time())
    images = response.json()["images"]
    for i, image in enumerate(images):
        if i == len(images) - 1:
            break
        filename = str(i) + ".png"
        saveEncodedImage(
            image, "./images/controlnet/" + str(timestamp) + "_" + filename
        )
