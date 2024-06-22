from PIL import Image
import os
import argparse
import requests
from pinecone import Pinecone, ServerlessSpec
from datasets import load_dataset
from pinecone_text.sparse import BM25Encoder
from sentence_transformers import SentenceTransformer
import torch
import json

def find_similar_images(image_path):
    # Initialize Pinecone client and index setup
    pc = Pinecone(api_key="106c982c-4e5e-476e-85d6-d10e8ec7f7d6")

    cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
    region = os.environ.get('PINECONE_REGION') or 'us-east-1'

    spec = ServerlessSpec(cloud=cloud, region=region)
    index_name = "hybrid-image-search"

    # Check if index already exists (it shouldn't if this is the first time)
    if index_name not in pc.list_indexes().names():
        # If it does not exist, create the index
        pc.create_index(
            index_name,
            dimension=512,
            metric='dotproduct',
            spec=spec
        )

    # Connect to index
    index = pc.Index(index_name)

    # Load the dataset from huggingface datasets hub
    fashion = load_dataset("ashraq/fashion-product-images-small", split="train")
    images = fashion["image"]
    metadata = fashion.remove_columns("image")
    metadata = metadata.to_pandas()

    # Initialize BM25 encoder for sparse embeddings
    bm25 = BM25Encoder()
    bm25.fit(metadata['productDisplayName'])

    # Initialize SentenceTransformer model for dense embeddings
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer('sentence-transformers/clip-ViT-B-32', device=device)

    defaultImageUrl = "https://rukminim2.flixcart.com/image/850/1000/xif0q/t-shirt/t/e/0/l-st-theboys-black-smartees-original-imagnqszzzzyuzru.jpeg?q=90&crop=false"

    try:
        # Process input image to get embeddings
        input_image = Image.open(image_path)
        input_image = input_image.convert('RGB')

        # Example logic to find similar images (replace with your actual logic)
        query = "black pants"  # Example query, replace with actual user query
        embeddings = model.encode([input_image]).tolist()
        sparse = bm25.encode_queries(query)
        dense = embeddings

        # Perform the search using the precomputed embeddings
        results = index.query(
            top_k=3,  # Adjust the number of similar images to return
            vector=dense[0],
            sparse_vector=sparse,
            include_metadata=False
        )

        # Use returned product ids to get images and prepare response
        similar_images_urls = [images[int(r["id"])] for r in results["matches"]]
        product_images = {
            'original_image': os.path.basename(image_path),
            'similar_images': similar_images_urls
        }

        # Save similar images to a directory named similar_images
        save_directory = 'similar_images'
        os.makedirs(save_directory, exist_ok=True)
        for idx, sim_image_url in enumerate(similar_images_urls):
            response = requests.get(sim_image_url)
            if response.status_code == 200:
                with open(os.path.join(save_directory, f'similar_image_{idx}.jpg'), 'wb') as f:
                    f.write(response.content)

    except Exception as e:
        product_images = {'error': str(e)}

    if not product_images.get('similar_images'):
        product_images['similar_images'] = [defaultImageUrl] * 3

    return product_images

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find similar images based on input image.')
    parser.add_argument('--image_path', type=str, required=True, help='Path to input image file.')
    args = parser.parse_args()

    result = find_similar_images(args.image_path)
    print(json.dumps(result, indent=2))
