import requests
import base64
# Replace with the URL of your Flask app
url = 'http://localhost:5000/search'

# Path to the image file you want to use for the search
image_path = r'C:\Users\Joy\Desktop\Video Streaming Platform\video_player_uploader\flask\clothing_item_0.jpg'

# The query text
query_text = 'red dress'

# Read the image file
with open(image_path, 'rb') as img_file:
    img_data = img_file.read()

# Create the payload
files = {'image': ('image.jpg', img_data, 'image/jpeg')}
data = {'query': query_text}

# Send the POST request
response = requests.post(url, files=files, data=data)

# Check the response
if response.status_code == 200:
    result_images = response.json().get('result_images', [])
    for i, img_str in enumerate(result_images):
        img_data = base64.b64decode(img_str)
        with open(f'result_{i}.jpg', 'wb') as img_file:
            img_file.write(img_data)
    print(f"Retrieved {len(result_images)} images.")
else:
    print(f"Error: {response.status_code} - {response.text}")
