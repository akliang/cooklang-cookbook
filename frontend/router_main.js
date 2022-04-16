const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');

const api_url = "https://cookbook.albertliang.xyz/api";

// home view (my recipes)
router.get('/', (req, res) => {
  fetch(api_url + '/view/', {
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

router.get('/v/:user/:recipe', (req, res) => {
  fetch(api_url + '/view/' + req.params.user + '/' + req.params.recipe, {
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