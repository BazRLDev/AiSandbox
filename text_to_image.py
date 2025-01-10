import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_image(prompt):
    genai.configure(api_key=GEMINI_API_KEY, transport='rest')
    imagen = genai.ImageGenerationModel("imagen-3.0-fast-generate-001")
    result = imagen.generate_images(
        prompt=prompt,
        number_of_images=4,
        safety_filter_level="block_only_high",
        person_generation="allow_adult",
        aspect_ratio="3:4",
        negative_prompt="Outside",
    )
    for image in result.images:
        print(image)


    # if response and response.parts and len(response.parts) > 0:
    #     try:
    #         image_data = response.parts[0].data
    #         base64_image = base64.b64encode(image_data).decode("utf-8")
    #         return base64_image
    #     except Exception as e:
    #         print(f"error in generate_image: {e}")
    # else:
    #     print("Error: No image data returned")
    #     return None

def main():
	prompt = "A close-up shot of a willow tree gracefully bending in a strong wind, showcasing its resilience. The background features a softly blurred, idyllic Irish landscape with rolling green hills."
	image = generate_image(prompt)
	print(image)
	print('^^^^ would you look at that')

if __name__ == "__main__":
    main()