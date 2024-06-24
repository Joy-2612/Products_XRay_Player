from flask import Flask, request, jsonify
from pinecone import Pinecone, ServerlessSpec
from flask_cors import CORS 
import os
import time
import torch
from sentence_transformers import SentenceTransformer
from PIL import Image
import io
import base64
from pinecone_text.sparse import BM25Encoder
from datasets import load_dataset, load_from_disk
import pickle
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app) 
# Initialize Pinecone
pc = Pinecone(api_key="106c982c-4e5e-476e-85d6-d10e8ec7f7d6")

cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)
index_name = "hybrid-image-search"

# Check if index already exists (it shouldn't if this is first time)
if index_name not in pc.list_indexes().names():
    # If it does not exist, create index
    pc.create_index(
        index_name,
        dimension=512,
        metric='dotproduct',
        spec=spec
    )
    # Wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# Connect to index
index = pc.Index(index_name)

# Load the dataset
save_dir = r'C:\Users\Joy\Desktop\Video Streaming Platform\video_player_uploader\flask\preloads'
if not os.path.exists(os.path.join(save_dir, 'fashion_dataset')):
    fashion = load_dataset("ashraq/fashion-product-images-small", split="train")
    fashion.save_to_disk(os.path.join(save_dir, 'fashion_dataset'))
else:
    fashion = load_from_disk(os.path.join(save_dir, 'fashion_dataset'))

images = fashion["image"]
metadata = fashion.remove_columns("image")
metadata = metadata.to_pandas()

# Initialize BM25 encoder
bm25 = BM25Encoder()
bm25.fit(metadata['productDisplayName'])

# Load precomputed data
with open(os.path.join(save_dir, 'embeddings.pkl'), 'rb') as f:
    precomputed_data = pickle.load(f)

id_to_data = {}
for batch_data in precomputed_data:
    for _id, sparse, dense, meta in zip(batch_data['ids'], batch_data['sparse_embeds'], batch_data['dense_embeds'], batch_data['metadata']):
        id_to_data[_id] = {
            'sparse': sparse,
            'dense': dense,
            'metadata': meta
        }

# Load the CLIP model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('sentence-transformers/clip-ViT-B-32', device=device)

def hybrid_scale(dense, sparse, alpha: float):
    """Hybrid vector scaling using a convex combination."""
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    hsparse = {
        'indices': sparse['indices'],
        'values':  [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [[v * alpha for v in vec] for vec in dense]
    return hdense, hsparse

@app.route('/search', methods=['POST'])
def search():
    try:
        # Get the image and text from the request
        print("Hello1")
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        # query_text = request.form.get('query', '')
        query_text='pink tshirt'

        print("Hello2")

        print("Image file: ", image_file)
        print("File content type: ", image_file.content_type)
        
        # Ensure the file is an image
        if 'image' not in image_file.content_type:
            return jsonify({'error': 'File is not an image'}), 400


        print("Hello3")
        # Convert the image to PIL format
        image = Image.open(image_file.stream)

        # Encode the text and image
        sparse = bm25.encode_queries(query_text) if query_text else {}
        dense = model.encode([image]).tolist()
        print("Hello4")
        # Combine the encodings
        hdense, hsparse = hybrid_scale(dense, sparse, alpha=1)
        print("Hello5")
        # Perform the search using the precomputed embeddings
        results = index.query(
            top_k=14,
            vector=hdense[0],
            sparse_vector=hsparse,
            include_metadata=False
        )
        
        
             
        
        # Use returned product ids to get images
        imgs = [images[int(r["id"])] for r in results["matches"]]
        
        # print("images : ",imgs)
        # Convert images to base64
        result_images = []
        for img in imgs:
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            result_images.append(img_str)
        
        # Return the results
        return jsonify(result_images=result_images)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
