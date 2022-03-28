const express = require('express');
const app = express();
app.set('view engine', 'handlebars');

const server = app.listen(8003, () => {
  console.log(`Express running → PORT ${server.address().port}`);
});

app.get('/', (req, res) => {
  res.send('Hello World!');
});