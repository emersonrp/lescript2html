#!/usr/bin/python

# Convert LeScript files to HTML, generally maintaining formatting

# Copyright (c) 2025, emerson@hayseed.net
# https://hayseed.net/~emerson

from pathlib import Path
from optparse import OptionParser
import re

parser = OptionParser(usage = "usage: $prog [options] filename")
parser.add_option('-b', '--bytes',
                  action = 'store_true', dest = 'show_bytes', default = False,
                  help = "Print the raw bytes object instead of processing")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("A filename is required.")

p = Path(args[0])
lesc_bytes = p.read_bytes()

# If we asked to see the bytes, do that
# This is mostly just for developing the script itself
if options.show_bytes:
    print(lesc_bytes)
    quit()

# first let's split lines
# LeScript uses \r without \n.
lesc_bytes = re.sub(rb'\r', rb'<br>\n', lesc_bytes)

# Just remove all printer commands and so forth completely
lesc_bytes = re.sub(rb'\x8a.+<br>\n', rb'', lesc_bytes)

# TODO - What are all of these?  Probably will want to handle them someday
lesc_bytes = re.sub(rb'\xf0..\xf0', rb' ', lesc_bytes)
lesc_bytes = re.sub(rb'\xf2..\xf2', rb' ', lesc_bytes)
lesc_bytes = re.sub(rb'\xf3..\xf3', rb' ', lesc_bytes)
lesc_bytes = re.sub(rb'\xf4..\xf4', rb' ', lesc_bytes)
lesc_bytes = re.sub(rb'\xf5..\xf5', rb' ', lesc_bytes)
lesc_bytes = re.sub(rb'\xf6..\xf6', rb' ', lesc_bytes)
lesc_bytes = re.sub(rb'\xf7..\xf7', rb' ', lesc_bytes)

# TODO - blockquoting.  This is tangly and I'm punting for now, but this is the stuff
# (These are already removed in the above block, anyway, so are just here for reference)
lesc_bytes = re.sub(rb'\xf4\t.\xf4', rb'\t', lesc_bytes)
lesc_bytes = re.sub(rb'\xf0\t.\xf0', rb'\t', lesc_bytes)

# TODO - what are these Individual codes?  Let's eliminate them for now but....
lesc_bytes = re.sub(rb'\x8c', rb'', lesc_bytes)
lesc_bytes = re.sub(rb'\x00', rb'', lesc_bytes) # padding / filler?

# TODO - This is probably setting chars / line with the \d+
# Maybe catch it and set up a small CSS style?  Maybe that's overthinking it.
lesc_bytes = re.sub(rb'\xd5\d+ ', rb'', lesc_bytes)

### OK, change control codes that we know to HTML

# "formatting codes" -- these are in the format \xfe(code)single letter(code)\xfe
# Where code is a bitfield setting up superspace, subspace, bold, underline, and italic
#
# I suppose there might be more values but the feature documentation makes me
# think these are all the possible formatting codes.

def parse_formatting_code(matchobj):
    code = ord(matchobj.group(1))
    char = matchobj.group(2)

    if code & 0x01: char = b"<sup>" + char + b"</sup>"
    if code & 0x02: char = b"<sub>" + char + b"</sub>"
    if code & 0x04: char = b"<b>" + char + b"</b>"
    if code & 0x08: char = b"<u>" + char + b"</u>"
    if code & 0x10: char = b"<i>" + char + b"</i>"
    if code & 0x20: char = char # Never seen this but there is 0x40 so this probably exists
    if code & 0x40: char = char # Dunno what this represents but I found it in the wild
    return char

lesc_bytes = re.sub(rb'\xfe([\x01-\x4f])(.)\1\xfe', parse_formatting_code, lesc_bytes)

# OK, now we have each letter bracketed with HTML codes.  That's spammy, so we
# eliminate dupe tags.  Do this in reverse order from how we add them above.
lesc_bytes = re.sub(rb'</i><i>', rb'', lesc_bytes)
lesc_bytes = re.sub(rb'</u><u>', rb'', lesc_bytes)
lesc_bytes = re.sub(rb'</b><b>', rb'', lesc_bytes)
lesc_bytes = re.sub(rb'</sub><sub>', rb'', lesc_bytes)
lesc_bytes = re.sub(rb'</sup><sup>', rb'', lesc_bytes)

# Nonbreaking spaces
lesc_bytes = re.sub(rb'\x7f', rb'&nbsp;', lesc_bytes)

# OK, now let's turn it into a character string
output = ''
try:
    output = lesc_bytes.decode('utf-8')

    output = f"<html>\n<body>\n{output}\n</body>\n</html>"

except Exception as e:
    print(e)
    print(lesc_bytes)

finally:
    print(output)
