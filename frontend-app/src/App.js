import React, { useState } from "react";
import "./styles/App.css";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Videos from "./Components/Videos";
import VideoPlayer from "./Components/VideoPlayer";
import Upload from "./Components/Upload";
import Button from "./Components/Button";
import XRay from "./Components/XRay";

function App() {
  const [modal, setModal] = useState(false);

  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

function AppContent() {
  const [modal, setModal] = useState(false);
  const location = useLocation();

  // Check if current route is '/videos/:id'
  const isVideoPlayerPage = location.pathname.startsWith("/videos/");

  return (
    <div className="App">
      {!isVideoPlayerPage && (
        <div className="upload">
          <Button
            name="Upload"
            icon={<i className="fas fa-plus"></i>}
            onClick={() => {
              setModal(true);
            }}
            bg="#1e90ff"
          />
        </div>
      )}
      {modal && <Upload />}
      {!isVideoPlayerPage && (
        <div className="banner">
          <div className="banner-overlay"></div>
        </div>
      )}
      <Routes>
        <Route path="/" element={<Videos />} />
        <Route path="/videos/:id" element={<VideoPlayer />}>
          <Route path="x-ray" element={<XRay />} />
        </Route>
      </Routes>
      {modal && <div className="overlay" onClick={() => setModal(false)}></div>}
    </div>
  );
}

export default App;
