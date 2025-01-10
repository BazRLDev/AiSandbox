import requests
import base64
from io import BytesIO
from PIL import Image

def fetch_image_and_encode(image_url):
    """Fetches an image from a URL and encodes it to base64.

    Args:
        image_url: The URL of the image.

    Returns:
        The base64-encoded string of the image, or None if an error occurs.
    """
    try:
        # Fetch Image from URL
        response = requests.get(image_url, stream=True)
        response.raise_for_status() # Raise an exception for bad status codes

        # Convert Response to PIL image
        image = Image.open(BytesIO(response.content))
        image = image.convert("RGB")

        # Encode Image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        print(base64_image)
        print('^^^ image?')

        return base64_image
    except requests.exceptions.RequestException as e:
      print(f"Error fetching image from url: {e}")
      return None
    except Exception as e:
        print(f"Error encoding the image: {e}")
        return None

def main():
    image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-9fY0etUjGwNSavlicZXfjvKC/user-8YFUvVebIp47U3sFCx5PSjIJ/img-qmGoy74envGQXpF8Jwabbq3P.png?st=2025-01-10T12%3A20%3A45Z&se=2025-01-10T14%3A20%3A45Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-01-10T00%3A10%3A29Z&ske=2025-01-11T00%3A10%3A29Z&sks=b&skv=2024-08-04&sig=BKaiyuDSTuDrF//QQf%2BY/4hcb6qU7kMM422knDoBN18%3D"
    fetch_image_and_encode(image_url)

if __name__ == "__main__":
    main()