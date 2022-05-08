const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
const C = require('./constants');
const logger = require('./logger');
const h = require('./helpers');
const multer  = require('multer');
const upload = multer({ dest: 'static/img/' });
const path = require('path');
const fs = require('fs');
const sharp = require('sharp');

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
    if (Object.keys(json.ingredients).length > 0) {
      showhr = true;
    } else {
      showhr = false;
    }

    if (h.loggedIn(req)) {
      loggedin = true;
    } else {
      loggedin = false;
    }
    
    res.render('view_recipe', {data: json, username: req.params.username, slug: req.params.slug, showhr: showhr, loggedin: loggedin});
  })
  .catch(error => {
    logger.warn("Problem loading recipe \"/v/" + req.params.username + "/" + req.params.slug + "\" // " + error.message, {service: "viewrecipe"});
    res.render('404')
  });
});


//
// PROTECTED ROUTES
//
// add recipe (get)
router.get('/add', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login?next=/add');
  } else {
    //res.render('add_recipe_standard');
    res.render('add_recipe_desktop');
  }
});

// add recipe (post)
router.post('/add', upload.single('recipe'), (req, res) => {
  if (!h.loggedIn(req)) {
    req.flash('login_msg', 'Something went wrong.  Please contact us for support.');
    res.redirect('/login?next=/add');
  } else {
    // first, save the image
    var image_filename = undefined;
    if (req.file) {
      sharp(req.file.path)
      .resize(600, 1200, {fit: 'inside'})
      .jpeg({quality: 90})
      .toFile(path.resolve(req.file.destination, 'recipes', req.file.filename + '.jpg'))
      .then(() => {
        fs.unlinkSync(req.file.path);
      });
      image_filename = req.file.filename;
    }    

    // next, save the recipe in the API
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
        'image': image_filename,
        'ingredientname': req.body.ingredientname,
        'ingredientqty': req.body.ingredientqty,
      })
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        res.redirect('/login');
        throw new Error(response.statusText);
      }
    })
    .then(json => {
      // Dropzone can't use the res.redirect() return, so send it the URL href to redirect to manually
      if (image_filename) {
        res.send({
          status: true,
          url: '/v/' + json.username + '/' + json.slug,
        });
      } else {
        res.redirect('/v/' + json.username + '/' + json.slug);
      }
    })
    .catch(error => {
      logger.error("Problem adding recipe (API key: " + req.session.apikey + ") // " + error.message, {service: "addrecipe"});
    });
  }
});

// edit recipe (get)
router.get('/edit/:username/:slug', (req, res) => {
  if (!h.loggedIn(req)) {
    // TODO: make sure the logged in user is actually authorized to edit this recipe
    res.redirect('/login?next=/edit/' + req.params.username + '/' + req.params.slug);
  } else {
    fetch(C.api_viewrecipesbytoken_url, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.session.apikey,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: qs.stringify({
        'slug': req.params.slug
      })
    })
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        res.redirect('/');
        throw new Error(response.statusText);
      }
    })
    .then(json => {
      res.render('add_recipe_desktop', {data: json, back: "/v/" + req.params.username + "/" + req.params.slug});
    })
    .catch(error => {
      logger.error("Problem editing recipe (API key: " + req.session.apikey + ") // " + error.message, {service: "editrecipe"});
    });
  }
});

// delete recipe (post)
router.get('/delete/:slug', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login?next=/delete/' + req.params.slug);
  } else {
    fetch(C.api_deleterecipe_url, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.session.apikey,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: qs.stringify({
        'slug': req.params.slug
      })
    })
    .then(response => {
      if (response.ok) {
        req.flash('home_msg', 'Recipe deleted.');
        res.redirect('/');
      } else {
        res.redirect('/');
        throw new Error(response.statusText);
      }
    })
    .catch(error => {
      logger.error("Problem deleting recipe (API key: " + req.session.apikey + ") // " + error.message, {service: "deleterecipe"});
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
      logger.error("Problem bookmarking recipe (API key: " + req.session.apikey + ") // " + error.message, {service: "bookmarkrecipe"});
    })
  }
});

module.exports = router;