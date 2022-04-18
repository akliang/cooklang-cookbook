function loggedIn(req) {
  if ("apikey" in req.cookies) {
    return true;
  } else {
    return false;
  }
}

module.exports = {
  loggedIn: loggedIn
};