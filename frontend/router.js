const express = require('express');
const router = express.Router();

// axios setup
const https = require('https');
const axios = require('axios');
const instance = axios.create({
  baseURL: 'http://cookbook.albertliang.xyz/api/',
  xsrfHeaderName: "X-CSRFTOKEN",
  xsrfCookieName: "csrftoken",
  withCredentials: true,
  httpsAgent: new https.Agent({  
    rejectUnauthorized: false
  })
  // TODO: set-crsf endpoint
});

// router
router.get('/', (req, res) => {
  res.render('home');
});

router.get('/login', (req, res) => {
  res.render('login');
});

router.post('/login', (req, res) => {
  instance.post('/api_login/', {
    username: req.body.username,
    password: req.body.password
  }, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
  .then(function(response) {
    console.log("Login successsful for user: " + req.body.username);
  })
  .catch(function(error) {
    // TODO: login failures not being caught here (they show up as successful in .then block)
    console.error("Failed login for user: " + req.body.username + " (reason: " + error.message + ")");
    console.error(error);
  });
});

router.get('/recipe', (req, res) => {
  res.render('add_recipe');
});

// router.get('/v/:user', (req, res) => {
//   instance.get('/v2/' + req.params.user)
//   .then(function(response) {
//     console.log(response.data);
//     res.render('view_recipe', {data: response.data});
//   })
//   .catch(function(error) {
//     console.error(error);
//   });
//   // res.render('view_recipe');
// });

router.get('/v/:user/:recipe', (req, res) => {
  instance.get('/view/' + req.params.user + '/' + req.params.recipe)
  .then(function(response) {
    res.render('view_recipe', {title: response.data.meta.title, ingredients: response.data.ingredients, recipe: response.data.recipe});
  })
  .catch(function(error) {
    console.error("Error: " + error.message);
  });
});

function setJwtCookie(res, cookieName, cookieValue) {
  res.cookie(cookieName, cookieValue, {
    secure: true,
    httpOnly: true,
    sameSite: 'lax'
  });
}

module.exports = router;