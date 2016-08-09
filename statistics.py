#!/usr/bin/env python

import networkx as nx
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import operator
from collections import Counter

from files import *

nodelist = dict()
for node in nodes:
	nodelist[node['name']] = node['type']

G = nx.Graph()
G.add_nodes_from(nodelist)

for l in links:
	l_type = def_node[nodelist[l['dst']]]['in']
	vDrop = def_link[l_type]['mvperM'] * l['length']
	mass = def_link[l_type]['density'] * l['length']
	G.add_edge(l['src'],l['dst'], length=l['length'], vDrop=vDrop, mass=mass, ltype=l_type)

SG={}
gens = {k for (k,v) in nodelist.items() if ('incomer' in v) or ('gen' in v)}
for gen in gens:
	SG[gen] = G.subgraph( nx.node_connected_component(G,gen) )

sources = []
nodeCt = []
cableCt = []
cableLen = []
cableMass = []

for gen in gens:
	sources.append(gen)
	nodeCt.append( nx.number_of_nodes(SG[gen]) )
	cableCt.append( nx.number_of_edges(SG[gen]) )
	cableLen.append( sum(nx.get_edge_attributes(SG[gen],'length').values()) )
	cableMass.append( sum(nx.get_edge_attributes(SG[gen],'mass').values()) )

overviewTable = pd.DataFrame({
			'a': sources,
			'b': nodeCt,
			'c': cableCt,
			'd': cableLen,
			'e': cableMass,
		})
overviewTable.columns = ['Source', 'NodeCount', 'CableCount', 'CableLength(m)', 'CableMass(kg)']

ltypes=def_link.keys()
count = dict.fromkeys(ltypes,0)
tlength = dict.fromkeys(ltypes,0)

for (x,y,e) in G.edges(data=True):
	count[e['ltype']]+=1
	tlength[e['ltype']]+=e['length']

nodedist = {}
nodevDrop = {}
nodeGrid = {}

for gen in gens:
	for n in SG[gen].nodes():
		nodedist[n] = nx.shortest_path_length(SG[gen],source=gen,target=n,weight='length')
		nodevDrop[n] = nx.shortest_path_length(SG[gen],source=gen,target=n,weight='vDrop')
		nodeGrid[n] = gen

sorted_dist = sorted (nodedist.iteritems(), key=operator.itemgetter(1), reverse=True)
nodeArray = []
grid = []
distances = []

for x in range( len(sorted_dist[:5]) ):
	if sorted_dist[x][1] > 0:
		nodeArray.append(sorted_dist[x][0])
		grid.append(nodeGrid[sorted_dist[x][0]])
		distances.append(sorted_dist[x][1])

distanceTable = pd.DataFrame({
		'a': nodeArray,
		'b': grid,
		'c': distances,
	})

distanceTable.columns = ['Node', 'Source', 'Distance(m)']

sorted_vDrop = sorted (nodevDrop.iteritems(), key=operator.itemgetter(1), reverse=True)

nodeArray = []
grid = []
vdrop = []
percentdrop = []

for x in range( len(sorted_vDrop[:5]) ):
	if sorted_vDrop[x][1]/1000 > 0:
		nodeArray.append(sorted_vDrop[x][0])
		grid.append(nodeGrid[sorted_vDrop[x][0]])
		vdrop.append(sorted_vDrop[x][1]/1000)
		percentdrop.append((sorted_vDrop[x][1]/10)/230)

vDropTable = pd.DataFrame({
		'a': nodeArray,
		'b': grid,
		'c': vdrop,
		'd': percentdrop,
	})

vDropTable.columns = ['Node', 'Source', 'VoltageDrop(V)', 'PercentageDrop']

quants = []
types = []

for (a,b) in Counter(nodelist.values()).items() :
	quants.append(b)
	types.append(a)

distrosTable = pd.DataFrame({
		'a': types,
		'b': quants,
	})

distrosTable.columns = ['Type', 'Qty']

grid = []
types = []
lengths = []
count = []

LL={}
for gen in gens:
	lt = nx.get_edge_attributes(SG[gen],'ltype')
	le = nx.get_edge_attributes(SG[gen],'length')
	for l in SG[gen].edges_iter():
		key = gen,lt[l],le[l]
		if key in LL:
			LL[key]+=1
		else:
			LL[key]=1

for a in LL.keys():
	grid.append(a[0])
	types.append(a[1])
	lengths.append(a[2])
	count.append(LL[a])

lenghthTable = pd.DataFrame({
		'a': grid,
		'b': types,
		'c': lengths,
		'd': count,
	})

lenghthTable.columns = ['Source', 'Type', 'Length(m)', 'Count']

# Render html table
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('templates/statistics.html')

template_vars = {"title" : event_data['eventName'] + ' Power',
                 'overview': overviewTable.to_html(index=False),
                 'distance': distanceTable.to_html(index=False),
                 'vdrop': vDropTable.to_html(index=False),
                 'distros': distrosTable.to_html(index=False),
                 'lengths': lenghthTable.to_html(index=False)
                 }

html_out = template.render(template_vars)
HTML(string=html_out).write_pdf('output/stats.pdf', stylesheets=['templates/table.css'])