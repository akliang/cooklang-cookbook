const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
const C = require('./constants');
const logger = require('./logger');

// login page
router.get('/login', (req, res) => {
  res.render('login', {next: req.query.next, msg: req.flash('login_msg')});
});

// login to API backend
router.post('/login', (req, res) => { 
  fetch(C.api_login_url, {
    method: 'POST',
    body: qs.stringify({
      'username': req.body.username.toLowerCase(),
      'password': req.body.password
    }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      req.flash('login_msg', 'Invalid login attempt');
      res.redirect('/login');
      throw new Error("Login attempt failed for user: " + req.body.username);
    }
  })
  .then(json => {
    req.session.apikey = json['token'];
    req.session.save(() => {
      if (req.body.next) {
        res.redirect(req.body.next);
      } else {
        res.redirect('/');
      }
    });
  })
  .catch(error => {
    logger.error("(Login) " + error.message);
  });
});

// logout
router.get('/logout', (req, res) => {
  req.session.apikey = null;
  res.redirect('login');
});

// register (get)
router.get('/register', (req, res) => {
  res.render('register');
});

// register (post)
router.post('/register', (req, res) => {
  fetch(C.api_register_url, {
    method: 'POST',
    body: qs.stringify({
      'email': req.body.email,
      'username': req.body.username.toLowerCase(),
      'password1': req.body.password1,
      'password2': req.body.password2
    }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  })
  .then(response => {
    if (response.ok) {
      req.flash('login_msg', 'Account created!');
      res.redirect('/login');
      // break the promise chain
      return { then: function() {} };
    } else {
      return response.json()
    }
  })
  .then(json => {
    res.render('register', {msg: json});
    throw new Error(json);
  })
  .catch(error => {
    logger.error("(Register) " + error.message);
  });
});

module.exports = router;