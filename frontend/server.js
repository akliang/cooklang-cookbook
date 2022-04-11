// express setup
const express = require('express');
const app = express();
// const cors = require('cors');
// var corsOptions = {
//   origin: true,
//   optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
//   credentials: true
// }
// app.use(cors(corsOptions));
app.use(express.static('static'));
app.use(express.json());
app.use(express.urlencoded({extended: true}));
const server = app.listen(8003, () => {
  console.log(`Express running → PORT ${server.address().port}`);
});
var cookieParser = require('cookie-parser');
app.use(cookieParser());

// handlebars
const { engine } = require ('express-handlebars');
app.engine('.hbs', engine({extname: '.hbs', defaultLayout: 'body'}));
app.set('view engine', '.hbs');
app.set('views', './views');

// routes
const router = require('./router');
app.use(router);
