from prodiapy import Prodia
import requests
import random
def generate(path,text):
    prodia = Prodia(
        api_key="7b3bfa36-55c8-4c54-a3cd-cfa5f975f1cc"
    )

    job = prodia.sd.generate(prompt=text[8:].strip()+'in 4k',
                             style_preset='3d-model', aspect_ratio='portrait', negative_prompt='badly_drawn', upscale=True)
    result = prodia.wait(job)
    get = requests.get(result.image_url)
    with open(path+str(random.randint(0,100_000))+'ig.png','wb') as f:
        f.write(get.content)