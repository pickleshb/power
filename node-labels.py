#!/usr/bin/env python
# Auto generate power distro labeles form nodes.json

import labels
import os.path
import networkx as nx
from reportlab.graphics import shapes
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib import colors
from reportlab.lib.units import mm
import datetime
import operator
from collections import Counter
import csv
import urllib2
import random

from files import *

# Define colours
namedColour = {
  'blue' : colors.HexColor('#0000ff'),
  'tecblue': colors.HexColor('#264ba0'),
}

nodelist = []
for node in nodes:
  ntype = node['type'].lower()
  if not 'incomer' in ntype or 'gen' in ntype:
    nodelist.append(node)

# config
logo = './resources/tec-logo-power.png'
power = './resources/powerpower.png'

# Define the label paper
specs = labels.Specification(210, 297, 2, 5, 99, 57, corner_radius=2)

# load up the fonts
registerFont(TTFont('Raleway', './resources/Raleway-Regular.ttf'))
registerFont(TTFont('Raleway-Bold', './resources/Raleway-Bold.ttf'))

# what goes on a label
def draw_label(label, width, height, node):
    label.add(shapes.Image(0*mm, 0*mm, 17.49*mm, 53*mm, logo))

    label.add(shapes.String(26*mm, 125, node['name'], fontName="Raleway-Bold", fontSize=18, fillColor=colors.purple))
    label.add(shapes.String(26*mm, 95, node['location'], fontName="Raleway", fontSize=16))
    label.add(shapes.String(26*mm, 75, node['type'], fontName="Raleway", fontSize=12))

    # Footer
    label.add(shapes.String(26*mm, 30, event_data['eventName'], fontName="Raleway", fontSize=12, fillColor=namedColour['tecblue']))
    label.add(shapes.String(26*mm, 15, event_data['rigNumber'], fontName="Raleway", fontSize=12, fillColor=namedColour['tecblue']))

    label.add(shapes.Image(92*mm, 0.77*mm, 3.39*mm, 55.46*mm, power))

sheet = labels.Sheet(specs, draw_label, border=False)

# draw each node as a label
for node in nodelist:
    sheet.add_label(node)

# save it
sheet.save('output/node-labels.pdf')
# print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
