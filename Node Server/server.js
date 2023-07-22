const express = require('express');
const app = express();
const port = 5273;
const fs = require('fs');

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/getProducts', (req, res) => {
    fs.readFileSync('products.json', 'utf8', (err, data) => {
        if (err) {
            console.log(err);
            return;
        }
        let parseData = JSON.parse(data);
        
        console.log(parseData);
        res.send(true);
    });
  
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
});