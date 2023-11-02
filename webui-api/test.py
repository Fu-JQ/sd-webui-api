import base64, requests, time, json


def submitPost(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def decodeImage(b64_image: str, output_path: str):
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


def encoderImage(imgUrl: str):
    image = open(imgUrl, "rb")
    image_base64_byte = base64.b64encode(image.read())
    image.close()
    image_base64_string = image_base64_byte.decode("utf-8")
    return image_base64_string


if __name__ == "__main__":
    init_image = encoderImage("./images/model.jpeg")
    mask_image_base64 = encoderImage("./images/model_mask.jpeg")
    img2img_url = "http://webui.makeblock.com/sdapi/v1/img2img"
    data = {
        "prompt": "RAW photo, best quality, realistic,CANNO EOS R3, photo-realistic:1.3, masterpiece, ultra-detailed, CG unity, 8k wallpaper, amazing, finely detailed,( light smile: 0.9), highres, iu, asymmetrical bangs, short bangs, pureerosface_v1, beautiful detailed girl, extremely detailed eyes and face, beautiful detailed eyes, light on face, looking at viewer, straight-on, staring, closed mouth, black hair, long hair, collarbone, bare shoulders, long eyelashes, upper body, 1girl, full body:1.3, highly detailed face: 1.5, beautiful ponytail:0.5, beautiful detailed eyes, beautiful detailed nose, realistic face, realistic body, comfortable expressions, smile, look at viewer, comfortable expressions,fit model, hotel room, boudoir photography, upscale business hotel, luxurious decorations, expensive furniture, clean room, tasteful poses, lying on bed, sitting on sofa, showcasing beautiful body, modestly covered, pure, beautiful, soft lighting, professional equipment, camera settings, focal length, wardrobe details, model's expression, eye contact, sexy clothing, clean, bright scene, comfortable, (soft cinematic light:1.2), (depth of field:1.4), (intricate details:1.12), (sharp, exposure blend, medium shot:1.2), (natural skin texture, hyperrealism:1.2)",
        "negative_prompt": "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, watermark, (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, watermark",
        "n_iter": 1,
        "steps": 20,
        "init_images": [init_image],
        "mask": mask_image_base64,
        "resize_mode": 1,
        "inpaint_full_res": True,
        "inpainting_mask_invert": 1,
    }
    response = submitPost(img2img_url, data)
    print(response.status_code)
    timestamp = int(time.time())
    images = response.json()["images"]
    for i, image in enumerate(images):
        filename = "girl_" + str(i) + ".png"
        decodeImage(image, str(timestamp) + "_" + filename)
