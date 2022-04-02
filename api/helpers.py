import re

def write_formdata_to_cookfile(request, cleaned_data):
  filename = cleaned_data['title'].replace(" ","-").lower()
  with open(f"./data/recipes/{request.user.username}/{filename}.cook", "w") as file:
    file.write(f">> title: {cleaned_data['title']}\n")
    file.write(f">> tags: {cleaned_data['tags']}\n")
    file.write(cleaned_data['recipe'])
  return filename


def cooklang_processor(recipe):
  recipe_file = open(recipe, 'r')

  # todo: comments

  ingredients = []
  cookware = []
  timers = []
  meta = {}
  recipe = []
  for line in recipe_file:
    ingredients += _cl_do_regex("@", line)
    cookware += _cl_do_regex("#", line)
    timers += _cl_do_regex("~", line)
    if data := _cl_do_meta(line):
      meta[data[0]] = data[1]
    else:
      recipe.append(_clean_line(line))

  # remove all None elemenets from lists
  ingredients = list(filter(None, ingredients))
  cookware = list(filter(None, cookware))
  timers = list(filter(None, timers))

  # delete empty rows
  recipe = [i for i in recipe if i]

  # convert ingredient list to dictionary
  ingredients = {i[0]: i[1] for i in ingredients}

  return {
    'ingredients': ingredients,
    'cookware': cookware,
    'timers': timers,
    'meta': meta,
    'recipe': recipe,
  }


def _cl_do_regex(symbol, line):
  ret = []
  # get indices of all symbols in the line
  at_indices = [index for index,value in enumerate(line) if value == symbol]

  # walk through each symbol
  for num,idx in enumerate(at_indices):
    # only check the text between two symbols
    if idx != at_indices[-1]:
      nowline = line[idx:at_indices[num+1]]
    else:
      nowline = line[idx:]

    # check if it's a brace-ingredient
    if (match := re.search(symbol+"(.*?)\{(.*?)\}", nowline)):
      ingredient = match.group(1)
      quantity = re.sub("\%", " ", match.group(2))
    elif (match := re.search(symbol+"([A-Za-z0-9\-_]*)", nowline)):
      ingredient = match.group(1)
      quantity = ''
    else:
      print('Error!')

    ret.append((ingredient, quantity))

  return ret

def _cl_do_meta(line):
  if (match := re.match(">>\s*(.*?):\s*(.*)", line)):
    return match.groups()
  else:
    return None

def _clean_line(line):
  temp = re.sub("@", "", line)
  temp = re.sub("\{.*?\}", "", temp)
  temp = temp.replace("\n", "")
  return temp