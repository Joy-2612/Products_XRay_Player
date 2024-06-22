import React, { useState, useEffect } from "react";
import "../styles/XRay.css"; // Import the CSS file for styling
import Spinner from "./Spinner"; // Import the Spinner component

const defaultImageUrl =
  "https://rukminim2.flixcart.com/image/850/1000/xif0q/t-shirt/t/e/0/l-st-theboys-black-smartees-original-imagnqszzzzyuzru.jpeg?q=90&crop=false";

function XRay({ isOpen, onClose }) {
  const [productImages, setProductImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      fetch("http://localhost:8000/api/images")
        .then((response) => response.json())
        .then((data) => {
          setProductImages(data);
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching images:", error);
          setLoading(false);
        });
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="x-ray-overlay" onClick={onClose}>
      <div className="x-ray-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          &times;
        </button>
        <div className="x-ray-content">
          <h2>Recommended Products</h2>
          {loading ? (
            <Spinner />
          ) : (
            <div className="products">
              {productImages.map((image, index) => (
                <ProductRow key={index} image={image} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const ProductRow = ({ image }) => {
  const [similarImages, setSimilarImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchImageAndSend(image)
      .then((data) => {
        if (data.error) {
          throw new Error(data.error);
        }
        console.log("data : ", data);
        setSimilarImages(data.result_images); // Assuming the response structure
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching similar images:", error);
        setLoading(false);
      });
  }, [image]);

  const fetchImageAndSend = (imageUrl) => {
    return fetch(`http://localhost:8000/images/${imageUrl}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.blob();
      })
      .then((blob) => {
        const imageFile = new File([blob], "image.jpg", { type: "image/jpeg" });
        const formData = new FormData();
        formData.append("image", imageFile);

        return fetch("http://localhost:5000/search", {
          method: "POST",
          body: formData,
        }).then((response) => response.json());
      });
  };

  return (
    <div className="product-row">
      <img
        src={`http://localhost:8000/images/${image}`}
        alt="Product"
        onError={(e) => (e.target.src = defaultImageUrl)}
      />
      <div className="similar-products">
        {loading ? (
          <Spinner />
        ) : (
          similarImages.map((similarImage, idx) => (
            <div key={idx} className="similar-product">
              <img
                src={`data:image/jpeg;base64,${similarImage}`}
                alt={`Similar Product ${idx + 1}`}
                onError={(e) => (e.target.src = defaultImageUrl)}
              />
              {/* Replace with actual product link */}
              <a
                href={`https://example.com/similar${idx + 1}`}
                className="product-link"
                target="_blank"
                rel="noopener noreferrer"
              >
                View Product
              </a>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default XRay;
