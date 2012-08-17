#!/bin/bash

FILE=jBC_Programmers_Reference_Guide
blackfriday-tool ../$FILE.markdown $FILE.html.no-css
cat ../markdown.css > $FILE.html
cat $FILE.html.no-css >> $FILE.html
rm $FILE.html.no-css
