const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
const C = require('./constants');

// home view (my recipes)
router.get('/', (req, res) => {
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
    }
  })
  .then(json => {
    res.render('home', {recipes: json});
  })
  .catch(error => {
    console.error("Error (home): " + error.message);
  });
});

// view recipe
router.get('/v/:user/:recipe', (req, res) => {
  fetch(C.api_myrecipes_url + req.params.user + '/' + req.params.recipe)
  .then(response => {
    return response.json()
  })
  .then(json => {
    res.render('view_recipe', {title: json.meta.title, ingredients: json.ingredients, recipe: json.recipe});
  })
  .catch(function(error) {
    console.error("Error (view-recipe): " + error.message);
  });
});

module.exports = router;