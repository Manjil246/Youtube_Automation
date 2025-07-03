from diffusers import StableDiffusionPipeline
import torch

def generate_image(prompt):
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32,
        safety_checker=None
    )
    pipe = pipe.to("cuda")  # Use GPU
    image = pipe(prompt).images[0]
    image.save("images/output.png")

if __name__ == "__main__":
    generate_image("A futuristic sci-fi city skyline, glowing buildings, sunset, no people")

