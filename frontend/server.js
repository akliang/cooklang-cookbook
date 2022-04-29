// express setup
const express = require('express');
const app = express();
const session = require('express-session');
app.use(session({ 
  secret: process.env.EXPRESS_SECRET,
  saveUninitialized: true,
  resave: false,
  cookie: { 
    secure: false,
    maxAge: 1000*60*60*24,
    sameSite: true,
  }
}));
const flash = require('connect-flash');
app.use(flash());

// logging setup
const morgan = require('morgan');
const logger = require('./logger');
const skipSuccess = (req, res)  => res.statusCode < 400;
const skipError = (req, res)  => res.statusCode >= 400;
app.use(morgan('combined', { skip: skipSuccess, stream: logger.httperror }));
app.use(morgan('combined', { skip: skipError, stream: logger.httpsuccess }));

// other express and middleware setup
app.use(express.static('static'));
app.use(express.json({limit: '3mb'}));
app.use(express.urlencoded({extended: true, limit: '3mb'}));
const server = app.listen(8003, () => {
  console.log(`Express running → PORT ${server.address().port}`);
});


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