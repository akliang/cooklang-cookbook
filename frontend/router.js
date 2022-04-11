const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
var setCookie = require('set-cookie-parser');

const api_url = "https://cookbook.albertliang.xyz/api/";

// TODO: move this up to server.js and pass as object input to router.js
// axios setup
const https = require('https');
const httpsAgent = new https.Agent({
  rejectUnauthorized: false
});
// const axios = require('axios');
// const instance = axios.create({
//   baseURL: 'https://cookbook.albertliang.xyz/api/',
//   xsrfHeaderName: "X-CSRFTOKEN",
//   xsrfCookieName: "csrftoken",
//   withCredentials: true,
//   // TODO: remove this when real SSL is in
//   httpsAgent: new https.Agent({  
//     rejectUnauthorized: false
//   })
//   // TODO: set-crsf endpoint
// });

// router
router.get('/', (req, res) => {
  res.render('home');
});

router.get('/login', (req, res) => {
  res.render('login');
});

router.post('/login', (req, res) => {
  fetch('https://cookbook.albertliang.xyz/api/api_login/', {
    method: 'POST',
    body: qs.stringify({
      'username': req.body.username,
      'password': req.body.password
    }),
    agent: httpsAgent,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Access-Control-Allow-Origin': 'https://albertliang.xyz:8003'
    }
  })
  .then(response => { 
    const cookies = setCookie.parse(response.headers.raw()['set-cookie'], {
      decodeValues: true,
    });
    cookies.forEach(cookie => {
      res.cookie(cookie['name'], cookie['value'], {
        expires: cookie['expires'],
        httpOnly: cookie['httpOnly'],
        maxAge: cookie['maxAge'],
        path: cookie['path'],
        sameSite: cookie['sameSite'],
        secure: cookie['secure'],
      })
    });
    return response.text();
  })
  .then(text => {
    console.log(text);
    res.render('home');
  })
  .catch(error => {
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
  fetch(api_url + 'view/' + req.params.user + '/' + req.params.recipe, {
    method: 'GET',
    agent: httpsAgent,
    credentials: 'include',
    headers: {
      'X-CSRFToken': req.cookies['csrftoken']
    }
  })
  .then(response => {
    // console.log(response);
    return response.json()
  })
  .then(json => {
    res.render('view_recipe', {title: json.meta.title, ingredients: json.ingredients, recipe: json.recipe});
  })
  .catch(function(error) {
    console.error("Error: " + error.message);
    console.error(error);
  });
});

module.exports = router;