import express from 'express';

const PORT = 3000;
const app = express()

app.use(express.urlencoded({ extended: true}));  // Parses requests that are URL encoded
app.use(express.json());  // Incoming requests is JSON format

app.get('/getVideoList', (req, res) => {
    console.log("Video requested");


});


app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});