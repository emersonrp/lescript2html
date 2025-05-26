lescript2html.py
================

This is a small script to convert documents created by LeScript to HTML.

[LeScript](https://archive.org/search?query=lescript) was a word processor in the 80s from Anitek Software Products, primarily for the TRS-80, but eventually ported to other systems [including DOS](https://archive.org/manage/le-script-1.68-for-dos).

It was pretty cool for its time, but was never as popular as other similar programs like [Scripsit](https://en.wikipedia.org/wiki/Scripsit) or [Electric Pencil](https://en.wikipedia.org/wiki/Electric_Pencil).

My Dad loved LeScript, and created a lot of work and personal documents with it.  I was wanting to salvage all of these, and LeScript's built-in "export to ASCII" functionality is clunky and not great, so I decided to reverse-engineer the file format and convert the documents to bad HTML5.  This script is the result.

It takes as a single argument the filename of the LeScript file, and blats the HTML output to STDOUT.  A sample actual usage might be:

    lescript2html.py MYLESCDOC.LES > my_lescript_doc.html

In the case that it finds a LeScript code that it doesn't understand, it'll error and barf up the raw Python bytes object to STDOUT.  This should be considered a bug in the script, so please feel free to open an issue, including the STDOUT of the bytes object and possibly attaching the actual LeScript file in question.

This script is very much a work in progress, and currently throws away a good bit of the information saved in the LeScript file, including indentation and blockquoting.  I might or might not ever get to that.

Ping me if you find this useful and I might be inspired to work on it some more.

emerson@hayseed.net

