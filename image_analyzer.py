import cv2
import os


def analyze_image(image_path):

    print("\n==============================")
    print("       VISUAL ANALYSIS")
    print("==============================")

    # Check file
    if not os.path.exists(image_path):

        return {
            "status": "ERROR",
            "message": "Image file not found."
        }

    # Read image
    image = cv2.imread(image_path)

    if image is None:

        return {
            "status": "ERROR",
            "message": "Could not read image."
        }

    # Image dimensions
    height, width = image.shape[:2]

    print("\nImage information:")
    print("Width :", width)
    print("Height:", height)

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Brightness
    brightness = gray.mean()

    # Image size category
    if width >= 1920:
        quality = "High resolution"

    elif width >= 1000:
        quality = "Medium resolution"

    else:
        quality = "Low resolution"

    # Basic scene information
    if brightness < 60:

        lighting = "Dark image"

    elif brightness > 190:

        lighting = "Bright image"

    else:

        lighting = "Normal lighting"

    result = {

        "status": "SUCCESS",

        "width": width,

        "height": height,

        "quality": quality,

        "lighting": lighting,

        "brightness": round(
            float(brightness),
            2
        )

    }

    print("\nVisual information:")
    print("Quality   :", quality)
    print("Lighting  :", lighting)
    print("Brightness:", round(
        float(brightness),
        2
    ))

    return result