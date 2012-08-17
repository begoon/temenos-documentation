@echo off
set FILE=jBC_Programmers_Reference_Guide
blackfriday-tool.exe ../%FILE%.markdown %FILE%.html.no-css
copy ..\markdown.css+%FILE%.html.no-css %FILE%.html
rem del %FILE%.html.no-css
