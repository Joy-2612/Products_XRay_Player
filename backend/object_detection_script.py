from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
import argparse
import os

# Initialize the InferenceHTTPClient
CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="mqBkFv73fM5rRFb5J55z"
)

def extract_clothing_item(image, points):
    # Create a black image with the same dimensions as the original
    mask = np.zeros_like(image)

    # Create an array from the points
    polygon = np.array(points, np.int32)

    # Fill the mask with white where the clothing item is
    cv2.fillPoly(mask, [polygon], (255,)*image.shape[2])

    # Bitwise AND operation to isolate the clothing item
    masked_image = cv2.bitwise_and(image, mask)

    # Find the bounding rectangle for the mask
    x, y, w, h = cv2.boundingRect(polygon)

    # Crop the masked image
    cropped_image = masked_image[y:y+h, x:x+w]

    return cropped_image

def perform_object_detection(image_path, model_id):
    try:
        # Load the original image
        original_image = cv2.imread(image_path)
        
        if original_image is None:
            raise ValueError(f"Unable to load image at {image_path}")

        # Perform inference using InferenceHTTPClient
        results = CLIENT.infer(image_path, model_id=model_id)

        # Check if predictions exist
        if 'predictions' not in results or not results['predictions']:
            print("No predictions found.")
            return

        # Create 'objects' folder if it doesn't exist
        output_folder = 'objects'
        os.makedirs(output_folder, exist_ok=True)

        # Process each prediction
        for i, prediction in enumerate(results['predictions']):
            points = [(point['x'], point['y']) for point in prediction['points']]
            clothing_item_image = extract_clothing_item(original_image, points)

            # Save detected clothing item image to the 'objects' folder
            output_path = os.path.join(output_folder, f'clothing_item_{i}.jpg')
            success = cv2.imwrite(output_path, clothing_item_image)
            if success:
                print(f"Saved {output_path}")
            else:
                print(f"Failed to save {output_path}")

        print(f"Object detection and extraction completed. Images saved in the 'objects' folder.")

    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
    except Exception as e:
        print(f"Error performing object detection: {str(e)}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Perform object detection on an image')
    parser.add_argument('image_path', type=str, help='Path to the input image file')
    parser.add_argument('--model_id', type=str, default="deepfashion2-m-11k/1", 
                        help='Model ID for object detection (default: deepfashion2-m-11k/1)')
    args = parser.parse_args()

    # Call perform_object_detection function with parsed arguments
    perform_object_detection(args.image_path, args.model_id)
