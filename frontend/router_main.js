const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
const C = require('./constants');
const logger = require('./logger');
const h = require('./helpers');

//
// UNPROTECTED ROUTES
//
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


//
// PROTECTED ROUTES
//
// home view (my recipes)
router.get('/', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login');
  } else {
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
  }  
});

// add recipe (get)
router.get('/add', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login?next=/add');
  } else {
    res.render('add_recipe');
  }
});

// add recipe (post)
router.post('/add', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login');
  } else {
    fetch(C.api_addrecipe_url, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.cookies['apikey'],
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: qs.stringify({
        'title': req.body.title,
        'recipe': req.body.recipe
      })
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
    //   file.write(f">> title: {cleaned_data['title']}\n")
    // file.write(f">> tags: {cleaned_data['tags']}\n")
    // file.write(cleaned_data['recipe'])
      console.log(json);
      res.redirect('/v/' + json.username + '/' + json.filename);
    })
    .catch(error => {
      logger.error("(Add recipe) " + error.message);
    });
  }
});

module.exports = router;