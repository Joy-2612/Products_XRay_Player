import React, { useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useGlobalContext } from "../context/global";
import VideoJS from "./VideoJS";
import videojs from "video.js";
import "../styles/VideoPlayer.css"; // Import the new CSS file
import XRay from "./XRay";
import "videojs-contrib-quality-levels";

function VideoPlayer() {
  const { id } = useParams();
  const { videos } = useGlobalContext();

  const [isPaused, setIsPaused] = useState(true);
  const [isXrayOpened, setIsXrayOpened] = useState(false);

  const video = videos.find((vid) => {
    return vid._id === id;
  });
  //refs
  const videoConRef = useRef(null);
  const playerRef = React.useRef(null);

  const handlePlayerReady = (player) => {
    playerRef.current = player;

    // You can handle player events here, for example:

    player.on("play", () => {
      setIsPaused(false);
    });

    player.on("pause", () => {
      setIsPaused(true);
    });

    player.on("waiting", () => {
      videojs.log("player is waiting");
    });

    player.on("dispose", () => {
      videojs.log("player will dispose");
    });
  };

  //video Options
  const videoOptions = {
    autoplay: false,
    controls: true,
    responsive: true,
    fluid: true,
    alwaysShowControls: true,
    sources: [
      {
        src: video?.videoUrl,
        type: "video/mp4",
      },
    ],
    controlBar: {
      children: [
        "playToggle",
        "volumePanel",
        "progressControl",
        "currentTimeDisplay",
        "timeDivider",
        "durationDisplay",
        "pictureInPictureToggle",
        "qualitySelector",
        "fullscreenToggle",
      ],
      durationDisplay: {
        timeToShow: ["duration"],
        countDown: false,
      },
    },
  };

  return (
    <div className="video-player">
      <div className="video-container" ref={videoConRef}>
        {isXrayOpened && (
          <XRay isOpen={isXrayOpened} onClose={() => setIsXrayOpened(false)} />
        )}
        {isPaused && (
          <div className="video-overlay">
            <div className="x-ray">
              <h4 onClick={() => setIsXrayOpened(true)}>X-Ray</h4>
            </div>
            <div className="overlay-title">
              <h4>{video?.title}</h4>
              <p>{video?.description}</p>
            </div>
            <div className="back">
              <Link to={"/"}>
                <i className="fas fa-close"></i>
              </Link>
            </div>
          </div>
        )}
        <VideoJS options={videoOptions} onReady={handlePlayerReady} videoId={id} />
      </div>
    </div>
  );
}

export default VideoPlayer;
