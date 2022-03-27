
def write_formdata_to_cookfile(request, cleaned_data):
  filename = cleaned_data['title'].replace(" ","-").lower()
  with open(f"./data/recipes/{request.user.username}/{filename}.cook", "w") as file:
    file.write(f">> title: {cleaned_data['title']}\n")
    file.write(f">> tags: {cleaned_data['tags']}\n")
    file.write(cleaned_data['recipe'])
  return filename
