// express setup
const express = require('express');
const app = express();
const session = require('express-session');
app.use(session({ 
  secret: process.env.EXPRESS_SECRET,
  saveUninitialized: true,
  resave: false,
  cookie: { 
    secure:false,
    maxAge: 1000*60*60*24,
  }
}));
const flash = require('connect-flash');
app.use(flash());

// logging setup
const morgan = require('morgan');
const logger = require('./logger');
app.use(morgan('combined', { stream: logger.stream }));

// other express and middleware setup
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
const router_auth = require('./router_auth');
const router_main = require('./router_main');
app.use(router_auth);
app.use(router_main);

// the 404 catch
app.use(function(req, res, next) {
  res.status(404);

  // respond with html page
  if (req.accepts('html')) {
    res.render('404', { url: req.url });
    return;
  } else {
    res.type('txt').send('Not found');
  }
});