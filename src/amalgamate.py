import argparse
import io
import os.path
import re

parser = argparse.ArgumentParser()
parser.add_argument('output', help='output filename')
parser.add_argument('inputs', nargs='*', action='store', help='input filenames')
args = parser.parse_args()

outname = args.output.split("/")[-1]
header = False
if outname[-2:] == ".h":
    header = True

pos = outname.find(".")
if pos > 0:
    outname = outname[:pos]
    guard_name = outname.upper() + u"_H"

inc_re = re.compile("^#include (\".*\").*$")
guard_re = re.compile("^#(?:(?:ifndef|define) [A-Z_]+_H|endif /\* [A-Z_]+_H \*/|endif //[A-Z_]+_H)")

file = io.open(args.output, 'w')

if header:
    file.write(u"#ifndef %s\n#define %s\n" % (guard_name, guard_name))
else:
    file.write(u"#include \"%s.h\"\n" % outname)

for fname in args.inputs:
    with io.open(fname, encoding="utf8") as infile:
        for line in infile:
            inc_res = inc_re.match(line)
            guard_res = guard_re.match(line)
            if not inc_res and not guard_res:
                file.write(line)

if header:
    file.write(u"\n\n#endif /* %s */\n" % guard_name)
file.close()
