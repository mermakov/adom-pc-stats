import re
import sys

file = open("output", "r");
contents = file.read();
try:
    print re.search("\d of (\d)", contents).group(1)
except AttributeError:
    print 0
