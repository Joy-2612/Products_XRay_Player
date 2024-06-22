const express = require('express');
const app = express();
const cors = require('cors');
const { dbConnection } = require('./db/dbConect');
const {readdirSync} = require('fs');
const path = require('path');
const fs = require('fs');

require('dotenv').config()

const PORT = process.env.PORT || 8000

//middlewares
app.use(cors())
app.use(express.json())

const imagesDirectory = path.join(__dirname, 'objects');

//routes
readdirSync('./routes').map((route) => app.use('/api', require('./routes/' + route)))

//serve static files
app.use('/public', express.static(path.join(__dirname, 'public')))

app.get('/api/images', (req, res) => {
    fs.readdir(imagesDirectory, (err, files) => {
      if (err) {
        res.status(500).send('Unable to scan directory');
      } else {
        const imageFiles = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
        res.json(imageFiles);
      }
    });
  });


app.use('/images', express.static(imagesDirectory));

const server = () => {
    dbConnection()
    app.listen(PORT, () => {
        console.log(`Server is listening to ${PORT}`)
    })
}

server()