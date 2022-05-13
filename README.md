# Cookbook - A cooklang-inspire recipe book

The goal of the project is to create a lightweight and intelligent personal recipe cookbook.  Recipes are not searchable or browsable publicly.  This decreases the pressure to create "perfect" recipes and photos and frees the chef up to just write.  It's more important to organize all the recipes into one place than it is to make it Intagram-worthy.  Direct links to recipes can be shared publicly and can be bookmarked by others, though.

The underlying Cookbook language is [cooklang](https://cooklang.org/).  This is a very simple markup language without too many syntax rules to learn and remember.  However, this project does NOT follow cooklang's implementation to the letter.  Notable differences include:
- a self-written Python parser instead of the [official Python Parser](https://github.com/cooklang/cooklang-py)
- only implementing the ingredients (`@`) syntax, but dropping support for cookware (`#`), timers (`~`), meta (`>>`), and comments (`--`)
- probably does not support the shopping list feature (did not explicitly test)
- built based on Postgres db instead of the `.cook` flat-file system

# Installation

The code is organized around a couple of Docker containers, so all you'll have to do after you clone the repo is:
```
cp .env.example .env
# populate the .env fields
make up
```

That will spin up your own local instance of the REST API and the frontend.  Ideally, everyone can tap into the same REST API instead of having individual ones, but I haven't worked on the CORS on my current API server to let that happen yet.

# Usage

The recipe cookbook is constantly being developed right now.  I'll try to only push changes to `main` that I know are fully functioning, but no guarantees.  Tagged versions are more guaranteed to be fully functioning.

The idea for this Cookbook is to allow any variety of "frontend skins" and you're by no means married to the one I've provided in this project.  Feel free to create an iOS or Android native app, or even your own frontend browser version using a different tech stack (maybe React or Vue?) to interact with the backend API!