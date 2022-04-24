function loggedIn(req) {
  if (req.session.apikey) {
    return true;
  } else {
    return false;
  }
}

module.exports = {
  loggedIn: loggedIn
};