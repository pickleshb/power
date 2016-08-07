#!/usr/bin/env python

import networkx as nx
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import operator
from collections import Counter

from files import *

G = nx.Graph()
G.add_nodes_from(nodes)

for l in links:
	l_type = def_node[nodes[l['dst']]]['in']
	vDrop = def_link[l_type]['mvperM'] * l['length']
	mass = def_link[l_type]['density'] * l['length']
	G.add_edge(l['src'],l['dst'], length=l['length'], vDrop=vDrop, mass=mass, ltype=l_type)

SG={}
gens = {k for (k,v) in nodes.items() if ('incomer' in v) or ('gen' in v)}
for gen in gens:
	SG[gen] = G.subgraph( nx.node_connected_component(G,gen) )

print('Overview')
# print "Grid\tNodeCount\tCableCt\tCableLeng[m]\tCableMass[kg]"

sources = []
nodeCt = []
cableCt = []
cableLen = []
cableMass = []

for gen in gens:
	# print gen,
	# print "\t",nx.number_of_nodes(SG[gen]),
	# print "\t",nx.number_of_edges(SG[gen]),
	# print "\t", sum(nx.get_edge_attributes(SG[gen],'length').values()),
	# print "\t", sum(nx.get_edge_attributes(SG[gen],'mass').values())

	sources.append(gen)
	nodeCt.append( nx.number_of_nodes(SG[gen]) )
	cableCt.append( nx.number_of_edges(SG[gen]) )
	cableLen.append( sum(nx.get_edge_attributes(SG[gen],'length').values()) )
	cableMass.append( sum(nx.get_edge_attributes(SG[gen],'mass').values()) )

# print "Total\t", 
# print nx.number_of_nodes(G),
# print "\t",nx.number_of_edges(G),
# print "\t", sum(nx.get_edge_attributes(G,'length').values()),
# print "\t", sum(nx.get_edge_attributes(G,'mass').values())

# sources.append('Total')
# nodeCt.append(nx.number_of_nodes(G))
# cableCt.append(nx.number_of_edges(G))
# cableLen.append(sum(nx.get_edge_attributes(G,'length').values()))
# cableMass.append(sum(nx.get_edge_attributes(G,'mass').values()))

overviewDF = pd.DataFrame({
		'Source': sources,
		'NodeCount': nodeCt,
		'CableCount': cableCt,
		'CableLength(m)': cableLen,
		'CableMass(kg)': cableMass,
	})

print(pd.pivot_table(overviewDF, index=['Source']))

ltypes=def_link.keys()
count = dict.fromkeys(ltypes,0)
tlength = dict.fromkeys(ltypes,0)

for (x,y,e) in G.edges(data=True):
	count[e['ltype']]+=1
	tlength[e['ltype']]+=e['length']

#print "LType\t\tCount\tLength"
#for l in def_link.keys():
#	print l,'\t\t',count[l],'\t',tlength[l]
#print count
#print tlength

nodedist = {}
nodevDrop = {}
nodeGrid = {}

for gen in gens:
	for n in SG[gen].nodes():
		nodedist[n] = nx.shortest_path_length(SG[gen],source=gen,target=n,weight='length')
		nodevDrop[n] = nx.shortest_path_length(SG[gen],source=gen,target=n,weight='vDrop')
		nodeGrid[n] = gen

sorted_dist = sorted (nodedist.iteritems(), key=operator.itemgetter(1), reverse=True)
print "\nDistros furthest from source"
# print "node\tgrid\tdistance(m)"
nodeArray = []
grid = []
distances = []

for x in range( len(sorted_dist[:5]) ):
	if sorted_dist[x][1] > 0:
		# print sorted_dist[x][0], '\t', nodeGrid[sorted_dist[x][0]], '\t', sorted_dist[x][1]
		nodeArray.append(sorted_dist[x][0])
		grid.append(nodeGrid[sorted_dist[x][0]])
		distances.append(sorted_dist[x][1])

distanceDF = pd.DataFrame({
		'Node': nodeArray,
		'Source': grid,
		'Distance(m)': distances,
	})

print(pd.pivot_table(distanceDF, index=['Node', 'Source']))

sorted_vDrop = sorted (nodevDrop.iteritems(), key=operator.itemgetter(1), reverse=True)
print "\nDistros with worst voltage drop (50% of max current on all links)"
# print "node\tgrid\tvDrop(Volt)\t% Drop"
nodeArray = []
grid = []
vdrop = []
percentdrop = []

for x in range( len(sorted_vDrop[:5]) ):
	if sorted_vDrop[x][1]/1000 > 0:
		# print sorted_vDrop[x][0], '\t', nodeGrid[sorted_vDrop[x][0]], '\t', sorted_vDrop[x][1]/1000, (sorted_vDrop[x][1]/10)/230
		nodeArray.append(sorted_vDrop[x][0])
		grid.append(nodeGrid[sorted_vDrop[x][0]])
		vdrop.append(sorted_vDrop[x][1]/1000)
		percentdrop.append((sorted_vDrop[x][1]/10)/230)

vDropDF = pd.DataFrame({
		'Node': nodeArray,
		'Source': grid,
		'VoltageDrop(V)': vdrop,
		'PercentageDrop': percentdrop,
	})

print( pd.pivot_table(vDropDF, index=['Node', 'Source']) )

print "\nCount of distros by type"
# print "Qty\tType"
quants = []
types = []

for (a,b) in Counter(nodes.values()).items() :
	# print b,'\t',a
	quants.append(b)
	types.append(a)

distrosDF = pd.DataFrame({
		'Qty': quants,
		'Type': types,
	})

print(pd.pivot_table(distrosDF, index=['Type']))

print "\nCount of cable lengths by source"
# print "Grid\tType\tLength\tCount"
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
	# print "%s\t%s\t%s\t%i"%(a[0],a[1],a[2],LL[a])
	grid.append(a[0])
	types.append(a[1])
	lengths.append(a[2])
	count.append(LL[a])

lenghtDF = pd.DataFrame({
		'Source': grid,
		'Type': types,
		'Length(m)': lengths,
		'Count': count,
	})

print(pd.pivot_table(lenghtDF, index=['Source', 'Type']))