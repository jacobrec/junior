import shlex
import curses
import glob
from subprocess import Popen, PIPE


def testfile(file):
    expected_output = ""
    print(file)
    with open(file) as f:
        line = f.readline()
        assert line.startswith("/**")
        line = f.readline()
        while "*/" not in line:
            expected_output += line
            line = f.readline()

    cmd = "python3 src/junior.py " + file
    process = Popen(shlex.split(cmd), stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    try:
        assert(output.decode('utf-8') == expected_output)
    except AssertionError:
        print("Expected:\n:%s:\nbut got:\n%s\n: instead in file %s" %
              (expected_output, output.decode('utf-8'), file))


for f in sorted(glob.glob("testfiles/*.jr")):
    testfile(f)


print("All clear")
