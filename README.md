Usage
=====

All the data for the network is contained in these 5 files:

* nodes.json - nodes in the network
* links.json - links (cables)
* def_node.json - definitions of distros, sources, etc
* def_link.json - definitions of links
* event_data.json - data that will appear in the title block

For more information on how to create the network see the [wiki](../../wiki).

Requirements
============
Python requiremts are in requirements.txt
```
pip install -r requirements.txt
```

You may also need some other dependencies these being:
- graphviz - handles rendering the actual nework graph
- cairo - handles dot to pdf conversion
- pango - handles text to dot conversion

On Mac OS 
```
brew install graphvix cairo pango
```

And on Linux 
```
sudo apt-get graphviz cairo pango
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
