# PrimeVideo X-Ray Entended for Products

This project extends the Amazon Prime Video X-Ray feature to show product recommendations with images and links. The feature captures a frame from the video currently being played, identifies objects (currently only fashion products) from the frame using a Large Language Model (LLM), fetches similar products from a dataset using another Machine Learning (ML) model, and displays them within the video player. The project includes a video player built with the MERN stack (MongoDB, Express, React, Node.js) extended with this enhanced X-Ray feature.

## Features

- **Frame Extraction**: Captures the current frame from the video being played using OpenCV.
- **Object Identification**: Uses a Large Language Model (LLM) to identify fashion products in the frame.
- **Product Recommendation**: Fetches similar products from a dataset using an ML model.
- **In-Player Display**: Shows product recommendations with images and links within the video player.
- **MERN Stack Integration**: Includes a video player built with MongoDB, Express, React, and Node.js.

## Screenshots

#### Home Page

## ![ScreenShot](<./frontend-app/screenshots/Screenshot%20(236).png>)

#### Video Player

## ![ScreenShots](<./frontend-app/screenshots/Screenshot%20(234).png>)

#### Product Recommendations

## ![ScreenShots](<./frontend-app/screenshots/Screenshot%20(233).png>)

## Run on your Device

Clone the project from the repository

```bash
  git clone https://github.com/Joy-2612/BaatCheet.git
```

Install dependencies

```bash
  cd frontend-app/
  npm install
  cd ..
  cd backend
  npm install
  cd ..
```

Start the backend

```bash
  cd backend
  npm run start
```

Start the flask

```bash
  python app.py
```

Start the frontend

```bash
  cd frontend-app
  npm start
```

- Made by [@Joy-2612](https://github.com/Joy-2612) and [@raj128](https://github.com/raj128) 
