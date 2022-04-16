# Cookbook - based on the cooklang markup language

https://cooklang.org/

## User story
- Login
- Logout
- Get redirected to login with proper "next" param
- Register account
- Delete account?
- View a recipe
- View all my recipes
- Share a recipe
- Save a recipe
- View saved recipes
- Add a recipe
- Edit a recipe
- Delete a recipe
- Upload images

## Todo
- functionalize login redirect
- improve apikey cookie security (samesite)
- set up base handlebars template
- set up Express logging
- fix "catch" logging in Express
- 404 page?
- set up Django logging
- flash messages

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
