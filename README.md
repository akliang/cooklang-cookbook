# Cookbook - A cooklang recipe book

https://cooklang.org/

## User story
- (done) Login
- (done) Logout
- (done) Get redirected to login with proper "next" param
- Register account
- Delete account?
- (done) View a recipe
- (done) View all my recipes
- Share a recipe
- Save a recipe
- View saved recipes
- Add a recipe
- Edit a recipe
- Delete a recipe
- Upload images

## Todo
- redirect http400 to its own logging file
- clean up logging files?  (access.log vs console.log and an "all" file)
- set up Django logging
- flash messages... maybe? yes, probably need to for the "invalid api key" redirect

## Wishlist
- wysiwyg
- auto ingredient highlighting
- auto-preview recipe
- image server?
- coverage
- separate server/env for testing?

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


## Credits
- fry pan: <a href="https://www.flaticon.com/free-icons/cooking" title="cooking icons">Cooking icons created by Freepik - Flaticon</a>
- list: <a href="https://www.flaticon.com/free-icons/list" title="list icons">List icons created by phatplus - Flaticon</a>
- person: <a href="https://www.flaticon.com/free-icons/user" title="user icons">User icons created by Bombasticon Studio - Flaticon</a>
