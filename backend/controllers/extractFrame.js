const { exec } = require("child_process");
const path = require("path");

exports.extractFrame = async (req, res) => {
  const { time, vid_id } = req.body;
  // const videoPath = req.file.path;
  try {
    const frameExtractionCommand = `python video-frames-extractor/main.py --vid_dir=public/videos --out_dir=frames --img_frmt=jpg --required_frame_rate=10000 --start_from_seconds=${time}`;

    // const frameExtractionCommand = `python video-frames-extractor/main.py --vid_path=${
    //   "public/videos/video_" + vid_id + ".mp4"
    // } --out_dir=frames --img_frmt=jpg --required_frame_rate=10000 --start_from_seconds=${time}`;

    console.log("vid_id : ", vid_id);

    // Execute frame extraction command
    exec(frameExtractionCommand, (error, stdout, stderr) => {
      if (error) {
        console.error(`Frame extraction error: ${error.message}`);
        return res.status(500).json({
          message: "Frame extraction failed",
          error: error.message,
        });
      }

      console.log("Frame extraction completed successfully.");

      // Proceed with object detection after frame extraction completes
      const objectDetectionCommand = `python object_detection_script.py "C:\\Users\\Joy\\Desktop\\Video Streaming Platform\\video_player_uploader\\backend\\frames\\orig_size_frames\\video_71c88b7d-24cd-429b-8ec4-069b631d4e39_1.jpg"`;

      exec(objectDetectionCommand, (error, stdout, stderr) => {
        if (error) {
          console.error(`Object detection error: ${error.message}`);
          return res.status(500).json({
            message: "Object detection failed",
            error: error.message,
          });
        }

        console.log("Object detection completed successfully.");

        // Return success response after both tasks complete
        res.status(200).json({
          message:
            "Frame extraction and object detection completed successfully",
          output: stdout,
        });
      });
    });
  } catch (error) {
    console.error(`Processing error: ${error.message}`);
    res.status(400).json({
      message: "Frame extraction and object detection failed",
      error: error.message,
    });
  }
};
