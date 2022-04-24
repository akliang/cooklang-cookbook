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
router.get('/v/:username/:slug', (req, res) => {
  fetch(C.api_viewrecipes_url + req.params.username + '/' + req.params.slug, {
    headers: {
      "Authorization": "token " + req.session.apikey,
    }
  })
  .then(response => {
    return response.json()
  })
  .then(json => {
    // TODO: make this input less complex
    res.render('view_recipe', {title: json.title, ingredients: json.ingredients, recipe: json.recipe, edit: json.edit, bookmarked: json.bookmarked, username: req.params.username, slug: req.params.slug});
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
    fetch(C.api_viewrecipes_url, {
      headers: {
        "Authorization": "token " + req.session.apikey
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
      res.render('home', {title: "My Recipes", recipes: json});
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
    req.flash('login_msg', 'Something went wrong.  Please contact us for support.');
    res.redirect('/login?next=/add');
  } else {
    fetch(C.api_addrecipe_url, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.session.apikey,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: qs.stringify({
        'title': req.body.title,
        'recipe': req.body.recipe,
        'edit': req.body.edit,
      })
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        res.redirect('/login');
        throw new Error(response.statusText + " - invalid API key (attempted API key was: " + req.session.apikey + ")");
      }
    })
    .then(json => {
      res.redirect('/v/' + json.username + '/' + json.slug);
    })
    .catch(error => {
      logger.error("(Add recipe) " + error.message);
    });
  }
});

// edit recipe (post)
router.post('/edit/:username/:slug', (req, res) => {
  if (!h.loggedIn(req)) {
    // TODO: make sure the logged in user is actually authorized to edit this recipe
    res.redirect('/login?next=/edit/' + req.params.username + '/' + req.params.slug);
  } else {
    fetch(C.api_viewrecipesbytoken_url + req.params.slug, {
      headers: {
        "Authorization": "token " + req.session.apikey,
      }
    })
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        res.redirect('/');
        throw new Error(response.statusText + " (API key was: " + req.session.apikey + ")");
      }
    })
    .then(json => {
      // TODO: make this cleaner
      res.render('add_recipe', {title: json.title, recipe: json.recipe, slug: json.slug, edit: true});
    })
    .catch(error => {
      logger.error("(Edit-recipe) " + error.message);
    });
  }
});

// delete recipe (post)
router.post('/delete', (req, res) => {
  if (!h.loggedIn(req)) {
    // TODO: make delete a GET url and append ?next
    // TODO: make sure the user is authorize to delete this recipe
    res.redirect('/login');
  } else {
    fetch(C.api_deleterecipe_url + req.body.slug, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.session.apikey,
      }
    })
    .then(response => {
      if (response.ok) {
        req.flash('home_msg', 'Recipe deleted.');
        res.redirect('/');
      } else {
        res.redirect('/');
        throw new Error(response.statusText + " - recipe does not exists");
      }
    })
    .catch(error => {
      logger.error("(Delete-recipe) " + error.message);
    });
  }
});

// bookmark recipe (get)
router.get('/bookmark/:username/:slug', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login?next=/bookmark/' + req.params.username + '/' + req.params.slug);
  } else {
    fetch(C.api_bookmarkrecipe_url, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.session.apikey,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: qs.stringify({
        'username': req.params.username,
        'slug': req.params.slug,
      })
    })
    .then(response => {
      if (response.ok) {
        res.redirect('/v/' + req.params.username + '/' + req.params.slug);
      } else {
        res.redirect('/');
        throw new Error(response.statusText);
      }
    })
    .catch(error => {
      logger.error("(Bookmark-recipe) " + error.message);
    })
  }
});

// home view (my recipes)
router.get('/bookmarks', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login?next=/bookmarks');
  } else {
    fetch(C.api_viewbookmarkrecipes_url, {
      headers: {
        "Authorization": "token " + req.session.apikey
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
      res.render('home', {title: "Bookmarked Recipes", recipes: json});
    })
    .catch(error => {
      logger.error("(View-bookmarks) " + error.message);
    });
  }  
});

module.exports = router;