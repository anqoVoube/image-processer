from PIL import Image, ImageDraw, ImageFilter
from rembg import remove
import io

def process_image(input_image: bytes, name_with_ext: str) -> None:
    print("Processing image")
    # Remove the background
    output_image = remove(input_image, alpha_matting=True)
    print("Background was removed")
    # Convert the result to a PIL Image

    # Create a new image for the background with a gray color
    object_img = Image.open(io.BytesIO(output_image))

    # Create a new image with a gray background
    gray_color = (128, 128, 128)  # Gray color
    background_img = Image.new('RGB', object_img.size, gray_color)

    # Create a light effect
    light_effect = Image.new('RGB', object_img.size, gray_color)
    draw = ImageDraw.Draw(light_effect)
    center_x, center_y = light_effect.width // 2, light_effect.height // 2
    radius = min(center_x, center_y) + 400
    for i in range(radius, 0, -1):
        color = max(0, 220 - int(30 * (i / radius)))  # Lighter gray at the center
        draw.ellipse((center_x - i, center_y - i, center_x + i, center_y + i), fill=(color, color, color))

    # Blend the light effect with the gray background
    background_img = Image.alpha_composite(background_img.convert('RGBA'), light_effect.convert('RGBA'))

    # Create a silhouette of the object for the shadow
    shadow_silhouette = Image.new('RGBA', object_img.size, (0, 0, 0, 0))
    object_alpha = object_img.split()[-1]  # Get the alpha channel of the object
    shadow_silhouette.paste((0, 0, 0, 255), mask=object_alpha)

    # Apply a Gaussian blur to the shadow silhouette for the shadow effect
    shadow_blurred = shadow_silhouette.filter(ImageFilter.GaussianBlur(radius=15))

    # Create a new image for the background with a gray color

    # Composite the blurred shadow onto the background
    background_with_shadow = Image.alpha_composite(background_img, shadow_blurred)

    # Composite the object onto the background with shadow
    final_image = Image.alpha_composite(background_with_shadow, object_img)

    print("Trying to save")

    # Save or display the result
    final_image.save(name_with_ext)
    print("SAVED")

if __name__ == '__main__':
    process_image(open("sss.jpg", "rb").read(), "test.png")