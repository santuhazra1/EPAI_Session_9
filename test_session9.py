import pytest
import string
import session9
import os
import inspect
import re
import math

README_CONTENT_CHECK_FOR = ['odd_sec','logged','decorator','authenticate','password','timed','privilege_access',
'htmlize','int','float','Decimal','list','tuple','dictionary']

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(session9)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session9, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

def test_function_docstring_check():
    functions = inspect.getmembers(session9, inspect.isfunction)
    for function in functions:
        assert len(function[1].__doc__) > 0

def test_odd_sec_function_check(capsys):
    out = session9.add_odd_sec(2,3)
    captured = capsys.readouterr()
    if out == 5:
        assert captured.out == "Function add_odd_sec run on odd second.\n"
    else:
        assert captured.out == "Function didn't run as second value was not odd.\n"

def test_logged_function_check(capsys):
    out = session9.add_logged(2,3)
    captured = capsys.readouterr()
    if out == 5:
        assert "running time:" in captured.out
        assert "time taken:" in captured.out
        assert "function name: add_logged" in captured.out
        assert "function id:" in captured.out
        assert "function docstring:" in captured.out
        assert "function variables:" in captured.out

def test_authenticate_function_check(capsys):
    current_password = 'tsai'
    @session9.authenticate(current_password,"tsai")
    def add_authenticate(a, b):
        '''Add two Values and returns the result...'''
        return a + b
    out = add_authenticate(2,3)
    captured = capsys.readouterr()
    if out == 5:
        assert "Successful!!" in captured.out
    current_password = 'tsai'
    @session9.authenticate(current_password,"fake")
    def add_authenticate(a, b):
        '''Add two Values and returns the result...'''
        return a + b
    out = add_authenticate(2,3)
    captured = capsys.readouterr()
    assert "Password didn't match.. Please try again later!!" in captured.out

def test_timed_function_check(capsys):
    out = session9.add_timed(2,3)
    captured = capsys.readouterr()
    if out == 5:
        assert "add_timed(2,3) took" in captured.out

def test_privilege_access_function_check(capsys):
    @session9.privilege_access('high')
    def access_check(a, b, c, d):
        '''This function returns a tuple of the  passed variables'''
        return (a, b, c, d)
    out = access_check('a', 'b' ,'c', 'd')
    captured = capsys.readouterr()
    assert "You have admin access" in captured.out
    @session9.privilege_access('mid')
    def access_check(a, b, c, d):
        '''This function returns a tuple of the  passed variables'''
        return (a, b, c, d)
    out = access_check('a', 'b' ,'c', 'd')
    captured = capsys.readouterr()
    assert "You only have access to a , b & c" in captured.out
    @session9.privilege_access('low')
    def access_check(a, b, c, d):
        '''This function returns a tuple of the  passed variables'''
        return (a, b, c, d)
    out = access_check('a', 'b' ,'c', 'd')
    captured = capsys.readouterr()
    assert "You only have access to a & b" in captured.out
    @session9.privilege_access('no')
    def access_check(a, b, c, d):
        '''This function returns a tuple of the  passed variables'''
        return (a, b, c, d)
    out = access_check('a', 'b' ,'c', 'd')
    captured = capsys.readouterr()
    assert "Sorry you don't have any access. Please contact Service desk." in captured.out

def test_htmlize_function_check(capsys):
    assert session9.htmlize(100) == "100(<i>0x64</i>)"
    assert session9.htmlize([1, 2, 3, 4]) == "<ul>\n<li>1</li>\n<li>2</li>\n<li>3</li>\n<li>4</li>\n</ul>"
    assert session9.htmlize(((1, 2), (2, 3), (3, 4))) == "<ul>\n<li>(1, 2)</li>\n<li>(2, 3)</li>\n<li>(3, 4)</li>\n</ul>"
    assert session9.htmlize('1 < 100') == '1 &lt; 100'
    assert session9.htmlize(10.2569) == '10.26'