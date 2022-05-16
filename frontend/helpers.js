const C = require('./constants');

function loggedIn(req) {
  if (req.session.apikey) {
    return true;
  } else {
    return false;
  }
}

function getS3img(img_name) {
  return C.img_url + img_name;
}

module.exports = {
  loggedIn: loggedIn,
  getS3img: getS3img,
};