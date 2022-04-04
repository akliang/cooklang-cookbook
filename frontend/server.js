// express setup
const express = require('express');
const app = express();
app.use(express.static('static'));
app.use(express.json());
app.use(express.urlencoded({extended: true}));
const server = app.listen(8003, () => {
  console.log(`Express running → PORT ${server.address().port}`);
});

// handlebars
const { engine } = require ('express-handlebars');
app.engine('.hbs', engine({extname: '.hbs', defaultLayout: 'body'}));
app.set('view engine', '.hbs');
app.set('views', './views');

// routes
const router = require('./router');
app.use(router);