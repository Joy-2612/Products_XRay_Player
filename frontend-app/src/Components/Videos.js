import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Videos.css'; // Import the new CSS file
import { useGlobalContext } from '../context/global';

function Videos() {
    const { videos } = useGlobalContext();

    return (
        <div className="videos-container">
            {videos.map((video) => (
                <Link key={video._id} to={`/videos/${video._id}`}>
                    <div className="video">
                        <video src={video.videoUrl}></video>
                        <h4>{video.title}</h4>
                        <p>{video.description}</p>
                    </div>
                </Link>
            ))}
        </div>
    );
}

export default Videos;
