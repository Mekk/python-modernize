
# Tests for problem with multiple futures added to single file

import tempfile
import os
import shutil
from libmodernize.main import main as modernize_main


def _check_multiple_futures(file_content, extra_flags = []):
    try:
        tmpdirname = tempfile.mkdtemp()
        test_input_name = os.path.join(tmpdirname, "input.py")
        with open(test_input_name, "wt") as input:
            input.write(file_content)
        modernize_main(extra_flags + ["-w", test_input_name])
        counts = {}
        result_content = ""
        with open(test_input_name, "rt") as input:
            for line in input:
                if line.startswith("from __future__"):
                    counts[line] = 1 + counts.get(line, 0)
                result_content += line
        for future, how_many in counts.items():
            if how_many > 1:
                raise Exception("The same future repeated more than once ({0} times):\n{1}\n\n* Input file:\n{2}\n\n* Output file:\n{3}\n".format(how_many, future, file_content, result_content))
    finally:
        shutil.rmtree(tmpdirname)

def test_single_print():
    _check_multiple_futures("""
print 'world'
""")

def test_two_prints():
    _check_multiple_futures("""
print 'Hello'
print 'world'
""")

def test_many_prints_and_unicode():
    _check_multiple_futures("""
print 'Hello'
print u'world'
def sub(x):
    print x, u"here"
""", ["--future-unicode"])
