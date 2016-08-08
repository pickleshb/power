import json

def openJSON(file):
  f = open(file)
  file = json.load(f)
  f.close()

  return file

nodes = openJSON('data/nodes.json')
links = openJSON('data/links.json')
def_node = openJSON('data/def_node.json')
def_link = openJSON('data/def_link.json')
event = openJSON('data/event_data.json')
