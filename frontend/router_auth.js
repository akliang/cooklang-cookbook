const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
const C = require('./constants');

// login page
router.get('/login', (req, res) => {
  res.render('login');
});

// login to API backend
router.post('/login', (req, res) => {
  fetch(C.api_login_url, {
    method: 'POST',
    body: qs.stringify({
      'username': req.body.username,
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
      // TODO
      console.error("Error: " + response)
    }
  })
  .then(json => {
    res.cookie('apikey', json['token'], {
      sameSite: 'strict',
      httpOnly: false,
      secure: true,
    });
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

// logout
router.get('/logout', (req, res) => {
  res.clearCookie('apikey');
  res.redirect('login');
});

module.exports = router;