const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
const C = require('./constants');
const logger = require('./logger');

// home view (my recipes)
router.get('/', (req, res) => {
  // check the cookie as a quick way to see if user is logged in before attempting API call
  if ("apikey" in req.cookies) {
    fetch(C.api_myrecipes_url, {
      headers: {
        "Authorization": "token " + req.cookies['apikey']
      }
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        res.redirect('/login');
        throw new Error(response.statusText + " - invalid API key");
      }
    })
    .then(json => {
      res.render('home', {recipes: json});
    })
    .catch(error => {
      logger.error("(Home) " + error.message);
    });
  } else {
    res.redirect('/login');
  }
  
});

// view recipe
router.get('/v/:user/:recipe', (req, res) => {
  fetch(C.api_myrecipes_url + req.params.user + '/' + req.params.recipe)
  .then(response => {
    if (response.ok) {
      return response.json()
    } else {
      res.redirect('/');
      throw new Error(response.statusText + " - recipe does not exists");
    }
  })
  .then(json => {
    res.render('view_recipe', {title: json.meta.title, ingredients: json.ingredients, recipe: json.recipe});
  })
  .catch(error => {
    logger.error("(View-recipe) " + error.message);
  });
});

module.exports = router;