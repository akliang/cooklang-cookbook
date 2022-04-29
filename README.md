# Cookbook - A cooklang-inspire recipe book

The goal of the project is to create a lightweight and intelligent personal recipe cookbook.  Recipes are not searchable or browsable publicly.  This decreases the pressure to create "perfect" recipes and photos and frees the chef up to just write.  It's more important to organize all the recipes into one place than it is to make it Intagram-worthy.  Direct links to recipes can be shared publicly and can be bookmarked by others, though.

The underlying cookbook language is [cooklang](https://cooklang.org/).  This is a very simple markup language without too many syntax rules to learn and remember.  However, this project does NOT follow cooklang's implementation to the letter.  Notable differences include:
- a self-written Python parser instead of the [official Python Parser](https://github.com/cooklang/cooklang-py)
- only implementing the ingredients ("@") syntax, but dropping support for cookware ("#"), timers ("~"), meta (">>"), and comments ("--")
- probably does not support the shopping list feature (did not explicitly test)
- built based on Postgres db instead of the `.cook` flat-file system

## User story
- Login (get redirected with proper "next" param)
  - failed login (preserve "next" param)
- Logout
- Register account
  - email already registered
  - username already registered
  - password not long enough
  - passwords don't match
- Change password (and API token invalidation on pw change)
  - password not long enough
  - passwords don't match
  - password changed successfully (redirect to login with msg)
- Delete account
- View a recipe
  - save as bookmark
  - share
- View all my recipes
- Share a recipe
- Bookmark a recipe
- View bookmarked recipes
- Add a recipe
  - title not unique
  - image size too large
  - can only upload 1 image
- Edit a recipe
  - title not unique
  - image size too large
  - can only upload 1 image
- Delete a recipe
- Upload images

## Todo
- refactor all get paths to "/<regex>" to wrap in logged-in
- wrap all API calls to auto-append header?
- try to refactor API and frontend so they are DRYer (view recipe and edit recipe make same API hit, add recipe and edit recipe are very similar)
- extend APIView to something more custom?


## Wishlist
- wysiwyg
- auto ingredient highlighting
- auto-preview recipe
- image server?
- coverage
- separate server/env for testing?
- AI generate thumbnail image
- decrease number of API calls (cache all "myrecipes" to local, preferrably all saved recipes too)
- Cooklang "ingester" to copy-paste cooklang file into db
- export account
- make cookbook PDF
- make printable cookbook
- session cookie secure=true

## Testing todo
- selenium test for frontend
- fix cooklang tests
- refactor api tests for DRF style endpoints

## Development
```
# installing a new package to frontend
dc run -u root frontend npm install <package_name>
# have to run build with --no-cache to pick up the updated package.json
dc build --no-cache frontend
# sometimes docker-compose up uses the old container or image, so prune everything
docker container prune
docker image prune
# finally, spin up the project again
make up

# installing a new package to backend
docker exec -it cooklang-cookbook_api_1 bash
pip install <package>
pip freeze > requirements.txt
dc build --no-cache api
docker container prune
docker image prune
make up

# to check the database
docker exec -it cooklang-cookbook_db_1 bash
psql -U postgres
>> \dt
>> select * from api_recipe;

# reconnecting to all docker containers if detached
dc logs -f
```

## Useful links:
- https://freshman.tech/learn-node/
- https://waelyasmina.medium.com/a-guide-into-using-handlebars-with-your-express-js-application-22b944443b65
- https://forum.djangoproject.com/t/how-to-authenticate-django-rest-framework-api-calls-from-a-vue-js-client-using-session-authentication-and-httponly-cookies/5422
- https://stackoverflow.com/questions/70113882/axios-how-exactly-to-preserve-session-after-successful-authorization-and-send
- https://stackoverflow.com/questions/28100979/button-does-not-function-on-the-first-click
- https://stackoverflow.com/questions/15772394/how-to-upload-display-and-save-images-using-node-js-and-express
- https://appdividend.com/2022/03/03/node-express-image-upload-and-resize/
- https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
- https://www.sitepoint.com/file-upload-form-express-dropzone-js/
- https://stackoverflow.com/questions/20533191/dropzone-js-client-side-image-resizing
- https://github.com/sitepoint-editors/image-uploads-dropzonejs-node-express



## Credits
- fry pan: <a href="https://www.flaticon.com/free-icon/frying-pan_4329602" title="cooking icons">Cooking icons created by Freepik - Flaticon</a>
- list: <a href="https://www.flaticon.com/free-icons/list" title="list icons">List icons created by phatplus - Flaticon</a>
- person: <a href="https://www.flaticon.com/free-icons/user" title="user icons">User icons created by Bombasticon Studio - Flaticon</a>
- upload: <a href="https://www.flaticon.com/premium-icon/upload_4131814" title="image icons">Image icons created by mim_studio - Flaticon</a>
- cutting board: <a href="https://unsplash.com/@sanketshah">Sanket Shah</a>
  
