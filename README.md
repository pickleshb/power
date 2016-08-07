EMF2016 Power stuff

Files
=====

* nodes.json - nodes in the network
* links.json - links (cables)
* def_node.json - definitions of distros etc
* def_link.json - definitions of links

Requirements
============
Pythong requiremts are in requirements.txt
```
pip install -r requirements.txt
```

On mac OS you will need graphviz
```
brew install graphviz
```

If you want to go stright to pdf you also need [Ghostscript-9.19](http://pages.uoregon.edu/koch/)

Generate
========
To generate your powerplan and put it in the output folder run
```
bin/diagram.sh
```

Labels
======
To generate distro labels and put them in the output folder run
```
bin/labels.sh
```
