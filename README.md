# Cookbook - A cooklang recipe book

https://cooklang.org/

## User story
- (done) Login
- (done) Logout
- (done) Get redirected to login with proper "next" param
- Register account
- Change password (and API token invalidation on pw change)
- Delete account?
- (done) View a recipe
- (done) View all my recipes
- Share a recipe
- Save a recipe
- View saved recipes
- (done) Add a recipe
- (done) Edit a recipe
- (done) Delete a recipe
- Upload images

## Todo
- move recipes to database
- flash messages




- redirect http400 to its own logging file
- clean up logging files?  (access.log vs console.log and an "all" file)
- set up Django logging
- flash messages... maybe? yes, probably need to for the "invalid api key" redirect
- refactor all get paths to "/<regex>" to wrap in logged-in
- wrap all API calls to auto-append header?
- make login name case insensitive
- figure out where the "stir-fry-string-beans" call is coming from
- try to refactor API and frontend so they are DRYer (view recipe and edit recipe make same API hit, add recipe and edit recipe are very similar)
- add API key to error logging on frontend
- make data/recipe/ path DRYer (at the very least make the first 2 parts a constant)
- add cooklang markup to "edit recipe"
- add delete recipe flash message
- change "back" button on edit recipe based on context
- check cursor-pointer for all buttons
- fix login page register button
- api_login: what about invalid logins
- api_login: use the "created" object
- figure out all nav paths (back, cancel, what helpful buttons on each page)
- move recipes to database?

## Wishlist
- wysiwyg
- auto ingredient highlighting
- auto-preview recipe
- image server?
- coverage
- separate server/env for testing?
- AI generate thumbnail image
- decrease number of API calls (cache all "myrecipes" to local, preferrably all saved recipes too)

## Testing todo
- selenium test for frontend
- fix cooklang tests
- refactor api tests for DRF style endpoints

## Development
```
# installing a new package
dc run -u root frontend npm install <package_name>
# have to run build with --no-cache to pick up the updated package.json
dc build --no-cache frontend
# sometimes docker-compose up uses the old container or image, so prune everything
docker container prune
docker image prune
# finally, spin up the project again
make up
```

## Useful links:
- https://freshman.tech/learn-node/
- https://waelyasmina.medium.com/a-guide-into-using-handlebars-with-your-express-js-application-22b944443b65
- https://forum.djangoproject.com/t/how-to-authenticate-django-rest-framework-api-calls-from-a-vue-js-client-using-session-authentication-and-httponly-cookies/5422
- https://stackoverflow.com/questions/70113882/axios-how-exactly-to-preserve-session-after-successful-authorization-and-send
- https://stackoverflow.com/questions/28100979/button-does-not-function-on-the-first-click


## Credits
- fry pan: <a href="https://www.flaticon.com/free-icon/frying-pan_4329602" title="cooking icons">Cooking icons created by Freepik - Flaticon</a>
- list: <a href="https://www.flaticon.com/free-icons/list" title="list icons">List icons created by phatplus - Flaticon</a>
- person: <a href="https://www.flaticon.com/free-icons/user" title="user icons">User icons created by Bombasticon Studio - Flaticon</a>
