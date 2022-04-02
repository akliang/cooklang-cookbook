const express = require('express');
const app = express();
app.use(express.static('static'));
app.use(express.json());
app.use(express.urlencoded({extended: true}));

// handlebars
const { engine } = require ('express-handlebars');
app.engine('.hbs', engine({extname: '.hbs', defaultLayout: 'body'}));
app.set('view engine', '.hbs');
app.set('views', './views');

// axios
const axios = require('axios');
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

// constants
const api_url = 'https://cooklang-cookbook.albertliang.xyz';

// spin up the server
const port = 8003;
const server = app.listen(port, () => {
  console.log(`Express running → PORT ${server.address().port}`);
});

// router
app.get('/', (req, res) => {
  res.render('home');
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  axios.post(api_url + '/api/token/', {
    username: req.body.username,
    password: req.body.password
  })
  .then(function(response) {
    console.log(response.data);
    res.cookie('jwt_access', response.data.access, {
      secure: true,
      httpOnly: true,
      sameSite: 'lax'
    });
    res.cookie('jwt_refresh', response.data.refresh, {
      secure: true,
      httpOnly: true,
      sameSite: 'lax'
    });
    res.redirect('/');
  })
  .catch(function(error) {
    console.error(error);
    res.redirect('/login');
  });
});

app.get('/recipe', (req, res) => {
  res.render('add_recipe');
});

// app.get('/v/:user', (req, res) => {
//   axios.get(api_url + '/v2/' + req.params.user)
//   .then(function(response) {
//     console.log(response.data);
//     res.render('view_recipe', {data: response.data});
//   })
//   .catch(function(error) {
//     console.error(error);
//   });
//   // res.render('view_recipe');
// });

app.get('/v/:user/:recipe', (req, res) => {
  axios.get(api_url + '/v2/' + req.params.user + '/' + req.params.recipe)
  .then(function(response) {
    console.log(response.data[0]);
    res.render('view_recipe', {title: response.data[0].meta.title, ingredients: response.data[0].ingredients, recipe: response.data[0].recipe});
  })
  .catch(function(error) {
    console.error(error);
  });
});

app.get('/temp', (req, res) => {
  res.render('temp');
});

