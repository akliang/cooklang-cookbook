const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');

const api_url = "https://cookbook.albertliang.xyz/api";

// TODO: move this up to server.js and pass as object input to router.js

const https = require('https');
const httpsAgent = new https.Agent({
  rejectUnauthorized: false
});

// router
router.get('/', (req, res) => {
  fetch(api_url + '/view/', {
    agent: httpsAgent,
    headers: {
      "Authorization": "token " + req.cookies['apikey']
    }
  })
  .then(response => {
    if (!response.ok) {
      res.redirect('/login?next=/');
    } else {
      return response.json();
    }
  })
  .then(json => {
    res.render('home', {recipes: json});
  })
  .catch(error => {
    console.error("Error (home): " + error);
  });
});

router.get('/login', (req, res) => {
  res.render('login');
});

router.post('/login', (req, res) => {
  fetch(api_url + '/api_login/', {
    method: 'POST',
    body: qs.stringify({
      'username': req.body.username,
      'password': req.body.password
    }),
    agent: httpsAgent,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      // TODO
      console.error("Error: " + response)
    }
  })
  .then(json => {
    res.cookie('apikey', json['token']);
    if (req.query.next) {
      res.redirect(req.query.next);
    } else {
      res.redirect('/');
    }
  })
  .catch(error => {
    console.error(error);
  });
});

router.get('/logout', (req, res) => {
  res.clearCookie('apikey');
  res.redirect('login');
});

router.get('/v/:user/:recipe', (req, res) => {
  fetch(api_url + '/view/' + req.params.user + '/' + req.params.recipe, {
    agent: httpsAgent,
  })
  .then(response => {
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