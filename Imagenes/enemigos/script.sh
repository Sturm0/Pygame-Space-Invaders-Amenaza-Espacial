#! /bin/bash
shopt -s nocaseglob
for file in *.png
do
pngcrush -ow -rem allb -reduce "$file"
done
