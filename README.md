Files
=====

* nodes.json - nodes in the network
* links.json - links (cables)
* def_node.json - definitions of distros, sources, etc
* def_link.json - definitions of links

Requirements
============
Python requiremts are in requirements.txt
```
pip install -r requirements.txt
```

On mac OS you will need some other dependencies
```
brew install graphviz cairo pango
```

You will also need [Ghostscript-9.19](http://pages.uoregon.edu/koch/)

Generate
========
To generate your plans and put them in the output folder run
```
bin/genPaperwork.sh
```

To view see what flags are available to suppress certain file generation
```
bin/genPaperwork.sh -h
```
