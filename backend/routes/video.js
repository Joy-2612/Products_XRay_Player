const { addVideo, getAllVideos } = require('../controllers/video')
const { videoUpload } = require('../middlewares/videoUpload')
const { extractFrame } = require('../controllers/extractFrame')

const router = require('express').Router()


router.post('/upload', videoUpload.single('video'), addVideo)
    .get('/videos', getAllVideos)

router.post('/extract-frame',extractFrame)
module.exports = router