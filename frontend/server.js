const express = require('express');
const app = express();
app.use(express.static('static'));

const { engine } = require ('express-handlebars');
app.engine('.hbs', engine({extname: '.hbs'}));
app.set('view engine', '.hbs');
app.set('views', './views');

const port = 8003;
const server = app.listen(port, () => {
  console.log(`Express running → PORT ${server.address().port}`);
});

app.get('/', (req, res) => {
  res.render('home', {layout : 'main'});
});