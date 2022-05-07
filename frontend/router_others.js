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
const fileSaver = require('file-saver');


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
        throw new Error(response.statusText);
      }
    })
    .then(json => {
      res.render('home', {title: "My Recipes", recipes: json, msg: req.flash('home_msg'), shownav: true, showadd: true});
    })
    .catch(error => {
      logger.error("Problem loading home screen (API key: " + req.session.apikey + ") // " + error.message, {service: "home"});
    });
  }  
});

// bookmark view
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
        throw new Error(response.statusText);
      }
    })
    .then(json => {
      res.render('home', {title: "Bookmarked Recipes", recipes: json, shownav: true});
    })
    .catch(error => {
      logger.error("Problem display bookmarks (API key: " + req.session.apikey + ") // " + error.message, {service: "showbookmarks"});
    });
  }  
});

// import_export (get)
// router.get('/import_export', (req, res) => {
//   if (!h.loggedIn(req)) {
//     res.redirect('/login?next=/import_export');
//   } else {
//     res.render('import_export');
//   }
// });

// export (get)
// router.get('/export', (req, res) => {
//   if (!h.loggedIn(req)) {
//     res.redirect('/login?next=/export');
//   } else {
//     fetch(C.api_exportrecipes_url, {
//       method: 'POST',
//       headers: {
//         "Authorization": "token " + req.session.apikey,
//       },
//       responseType: "blob"
//     })
//     .then(response => {
//       if (response.ok) {
//         return response.blob();
//       } else {
//         res.redirect('/login');
//         throw new Error(response.statusText);
//       }
//     })
//     .then(blob => {
//       console.log(blob)
//       // console.log(fileSaver.saveAs(blob));
//       // const stream = fs.createReadStream('./tmp.zip', {bufferSize: 64 * 1024});
//       // stream.pipe(blob);
//       res.send(fileSaver.saveAs(blob));


//       // res.download(fileSaver.saveAs(blob), "my_recipes.zip");
//     })
//     .catch(error => {
//       logger.error("Problem exporting recipes (API key: " + req.session.apikey + ") // " + error.message, {service: "exportrecipes"});
//     });
//   }
// });

module.exports = router;