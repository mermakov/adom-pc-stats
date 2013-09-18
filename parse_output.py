import re
import sys

file = open("output", "r");
contents = file.read();
print re.search("\d of (\d)", contents).group(1)
