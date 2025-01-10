from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import textwrap

def add_border_with_text(base64_image, text, border_size_percent_x=0.05, border_size_percent_top=0.07, border_size_percent_bottom=0.13, text_height_percent=0.05, font_name="arial.ttf", font_size = 20, line_spacing = 10):
    """Adds a border and text below a base64-encoded image.
    Args:
        base64_image: The base64 encoded string of the image.
        text: The text to write.
        border_size_percent_x: The size of the side border as a percent of the image width
        border_size_percent_top: The size of the top border as a percent of the image height
        border_size_percent_bottom: The size of the bottom border as a percent of the image height
        text_height_percent: The height of the text as a percent of the image height
        font_name: The name of the font file.
        font_size: The size of the font
        line_spacing: The size of the line spacing.
    Returns:
        The base64 encoded string of the modified image
    """
    try:
        # Decode Base64 Image
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGB")

        # Image Properties
        image_width = image.width
        image_height = image.height

        # Calculate Border and Text Heights as Pixels
        border_size_x = int(image_width * border_size_percent_x)
        border_size_top = int(image_height * border_size_percent_top)
        border_size_bottom = int(image_height * border_size_percent_bottom)
        text_height = int(image_height * text_height_percent)

        # Create a new image with added border and space for text
        new_image_height = image_height + border_size_top + border_size_bottom + text_height
        new_image_width = image_width + 2*border_size_x # Border on each side
        new_image = Image.new("RGB", (new_image_width, new_image_height), (245, 245, 220)) # Use Cream background

        # Paste original image onto the new image
        new_image.paste(image, (border_size_x, border_size_top)) # Paste with a border on the left

        # Font Selection
        try:
            font = ImageFont.truetype(font_name, font_size) # try to load specified font
        except Exception as e:
            print('the font is fucked')
            print(e)
            font = ImageFont.load_default()  # If font not found, use default

        # Calculate the available text width
        text_width = new_image_width - 2*border_size_x #Use new image width
        # Wrap the text
        wrapped_text = textwrap.fill(text, width = text_width // (font.size // 2))

        # Calculate the Text Size
        text_bbox = font.getbbox(wrapped_text)
        text_width_bbox = text_bbox[2]
        text_height_bbox = text_bbox[3]

        # Create a drawing object
        draw = ImageDraw.Draw(new_image)

        # Calculate text position
        text_x = (new_image_width - text_width_bbox) // 2 # Use new image width
        text_y = (image_height + border_size_top + border_size_bottom//2) - text_height_bbox//2# Center the text vertically inside the bottom border

        # Calculate Line Spacing
        # Draw the text
        y = text_y
        for line in wrapped_text.splitlines():
            line_bbox = font.getbbox(line)
            line_width = line_bbox[2]
            text_x = (new_image_width - line_width) // 2 # center the text horizontally within the available width
            draw.text((text_x, y), line, (0, 0, 0), font=font) #Use black
            y += text_height_bbox+line_spacing


        # Save the image in memory as base64 data
        buffered = BytesIO()
        new_image.save(buffered, format="PNG")
        base64_image_output = base64.b64encode(buffered.getvalue()).decode("utf-8")

        print(f"New base64 image: {base64_image_output}")

        return base64_image_output
    except Exception as e:
       print(f"error in add_border_with_text: {e}")
       return None

def get_base_64_image():
    return encoded

def main():
    # add_border_with_text(get_base_64_image(), "The quick brown fox jumps over the lazy dog", border_size_percent_x=0.05, border_size_percent_top=0.07, border_size_percent_bottom=0.13, text_height_percent=0.05, font_name="arial.ttf")
    phrase = "Má chailleann tú uair ar maidin beidh tú á tóraíocht i rith an lae"
    add_border_with_text(get_base_64_image(), phrase, font_name="Raleway-Italic-VariableFont_wght.ttf", font_size = 40)

if __name__ == "__main__":
    main()

