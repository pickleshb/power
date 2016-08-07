#!/bin/bash
# Command that generates power plan paperwork
./diagram.py | unflatten -l 3  | dot -Tps2 | ps2pdf - > output/powerplan.pdf