const express = require('express');
const router = express.Router();
const qs = require('qs');
const fetch = require('node-fetch');
const C = require('./constants');
const logger = require('./logger');
const h = require('./helpers');

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
      res.redirect('/login?next=' + req.body.next);
      throw new Error(response.statusText);
    }
  })
  .then(json => {
    logger.info("Successful user login for " + req.body.username.toLowerCase(), {service: "login"})
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
    logger.warn("Login attempt failed for user: " + req.body.username + " // " + error.message, {service: "login"});
  });
});

// logout
router.get('/logout', (req, res) => {
  req.session.apikey = null;
  res.redirect('/login');
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
      logger.info("New account created for " + req.body.username.toLowerCase(), {service: "register"})
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
    throw new Error(JSON.stringify(json));
  })
  .catch(error => {
    logger.warn("Problems registering new account with username (" + req.body.username.toLowerCase() + ") and email (" + req.body.email + ") // " + error.message, {service: "register"});
  });
});

// account page (get)
router.get('/account', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login?next=/account');
  } else {
    // grab the current browsable_recipe value
    fetch(C.api_settingsbrowsable_url, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.session.apikey
      }
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      }
    })
    .then(flag => {
      if (flag) {
        checked = "checked";
      } else {
        checked = "";
      }
      res.render('account', {msg: req.flash('account_msg'), checked: checked, shownav: true});
    })
    .catch(error => {
      logger.warn("Error loading account page (API key: " + req.session.apikey + ") // " + error.message, {service: "account"});
      res.render('404');
    })
    
  }
});


// account page - make profile browsable (get)
router.get('/settings/make_browsable', (req, res) => {
  if (!h.loggedIn(req)) {
    res.redirect('/login?next=/account');
  } else {
    fetch(C.api_settingsbrowsable_url + req.query.val, {
      method: 'POST',
      headers: {
        "Authorization": "token " + req.session.apikey
      }
    })
    .then(response => {
      if (response.ok) {
        res.sendStatus(200);
      }
    })
    .catch(error => {
      logger.warn("Problem changing setting value (API key: " + req.session.apikey + ") // " + error.message, {service: "settings"});
    })
  }  
});

// delete account (post)
router.post('/delete_account', (req, res) => {
  fetch(C.api_deleteaccount_url, {
    method: 'POST',
    headers: {
      "Authorization": "token " + req.session.apikey
    }
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error(response.statusText);
    }
  })
  .then(json => {
    logger.info("Deleted account for user " + json.username + " (API key " + req.session.apikey + ")", {service: "delete"});
    req.session.apikey = undefined;
    req.session.save(() => {
      res.redirect('/');
    });
  })
  .catch(error => {
    logger.warn("Problem deleting account (API key: " + req.session.apikey + ") // " + error.message, {service: "delete"});
  })
});

// change password (get)
router.get('/change_password', (req, res) => {
  res.render('change_password');
});

// change password (post)
router.post('/change_password', (req, res) => {
  fetch(C.api_changepassword_url, {
    method: 'POST',
    headers: {
      "Authorization": "token " + req.session.apikey,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: qs.stringify({
      'old_password': req.body.old_password,
      'new_password1': req.body.new_password1,
      'new_password2': req.body.new_password2
    })
  })
  .then(response => {
    if (response.ok) {
      logger.info("Password changed for API key " + req.session.apikey, {service: "changepw"})
      req.flash('login_msg', 'Password updated! Please log in again.');
      res.redirect('/logout');
      // break the promise chain
      return { then: function() {} };
    } else {
      return response.json()
    }
  })
  .then(json => {
    res.render('change_password', {msg: json});
    throw new Error(JSON.stringify(json));
  })
  .catch(error => {
    logger.warn("Problem changing password for API key " + req.session.apikey + " // " + error.message, {service: "changepw"});
  });
});

// reset password (get)
router.get('/resetpw0', (req, res) => {
  res.render('resetpw0');
});

// reset password (post)
router.post('/resetpw0', (req, res) => {
  fetch(C.api_requestresetpassword_url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: qs.stringify({
      'email': req.body.email
    })
  })
  .then(response => {
    if (response.ok) {
      res.render('resetpw0', {msg: "Password reset sent to email."});
      // break the promise chain
      return { then: function() {} };
    } else {
      return response.json()
    }
  })
  .then(json => {
    res.render('resetpw0', {msg: json});
    throw new Error(JSON.stringify(json));
  })
  .catch(error => {
    logger.warn("Problem looking up email for pw reset // " + error.message, {service: "resetpw0"});
  });
});

// reset password - change password (get)
router.get('/resetpw/:user/:token', (req, res) => {
  res.render('resetpw', {user:req.params.user, token:req.params.token});
});

router.post('/resetpw/:user/:token', (req, res) => {
  fetch(C.api_resetpassword_url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: qs.stringify({
      'new_password1': req.body.new_password1,
      'new_password2': req.body.new_password2,
      'user': req.params.user,
      'token': req.params.token,
    })
  })
  .then(response => {
    if (response.ok) {
      req.flash('login_msg', 'Password has been changed.');
      res.redirect('/login');
      // break the promise chain
      return { then: function() {} };
    } else {
      return response.json()
    }
  })
  .then(json => {
    console.log(json)
    res.render('resetpw', {msg: json});
    throw new Error(JSON.stringify(json));
  })
  .catch(error => {
    logger.warn("Problem changing password for user " + req.params.user + " and token " + req.params.token + " // " + error.message, {service: "resetpw"});
  });
});

module.exports = router;