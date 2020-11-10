# Question: 1.1

def odd_sec(fn):
    '''This is decorator factory which returns a decorator which runs a function at each odd second'''
    import time
    from functools import wraps

    second = 0
    @wraps(fn)
    def inner(*args, **kwargs):
        nonlocal second
        second = int(time.time())
        if second % 2 !=0:
            print(f"Function {fn.__name__} run on odd second.")
            return fn(*args, **kwargs)
        else:
            print(f"Function didn't run as second value was not odd.")
    return inner

@odd_sec
def add_odd_sec(a, b):
    '''Add two Values and returns the result...'''
    return a + b

# Question 1.2

def logged(fn):
    '''This is a decorator which returns loggs a functions running time,
    time taken, function name, function id, it's docstring and function variable..'''
    from functools import wraps
    from datetime import datetime, timezone
    from time import perf_counter
    import inspect

    @wraps(fn)
    def inner(*args, **kwargs):
        run_dt = datetime.now(timezone.utc)
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        print(f'running time: {run_dt}')
        print(f'time taken: {end - start}')
        print(f'function name: {fn.__name__}')
        print(f'function id: {hex(id(fn))}')
        print(f'function docstring: {fn.__doc__}')
        print(f"function variables: {inspect.getfullargspec(fn)}")
        return result
    return inner

@logged
def add_logged(a, b):
    '''Add two Values and returns the result...'''
    return a + b

# Question 1.3

def set_password():
    '''This function takes an user input string and sets it as user password..'''
    password = ''
    def inner():
        nonlocal password
        if password == '':
            password = input()
        return password
    return inner

# current_password = set_password()()
current_password = 'tsai'

def authenticate(current_password, user_password):
    '''This is decorator factory which returns a decorator which authenticate a function
    with a password and returns result if password matches..'''
    def outer(fn):
        from functools import wraps
        cnt = 0
        @wraps(fn)
        def inner(*args, **kwargs):
            if user_password == current_password:
                print("Successful!!")
                return fn(*args, **kwargs)
            else:
                print("Password didn't match.. Please try again later!!")
                return None
        return inner
    return outer

@authenticate(current_password,"tsai")
def add_authenticate(a, b):
    '''Add two Values and returns the result...'''
    return a + b


# Question 1.4

def timed(count):
    '''This is a decorator factory which returns a decorator which returns
    average time taken by a function for n iterations'''
    def timed(fn):
        from time import perf_counter
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwargs):
            elapsed_total = 0
            elapsed_count = 0
            for i in range(count):
                print(f'Running iteration number {i + 1}')  
                start = perf_counter()
                result = fn(*args, **kwargs)
                end = perf_counter()
                elapsed = end - start
                elapsed_total += elapsed
                elapsed_count += 1

            args_ = [str(a) for a in args]
            kwargs_ = ['{0}={1}'.format(k, v) for k, v in kwargs.items()]
            all_args = args_ + kwargs_
            args_str = ','.join(all_args) 

            elapsed_avg = elapsed_total / elapsed_count

            print(f'{fn.__name__}({args_str}) took {elapsed_avg} seconds')

            return result
        return inner
    return timed

@timed(1000)
def add_timed(a, b):
    '''Add two Values and returns the result...'''
    return a + b


# Question 1.5

def privilege_access(access_type):
    '''This is a decorator factory which returns a decorator with a perticular privilege access type.'''
    def access(fn):
        from functools import wraps

        @wraps(fn)
        def inner(a, b, c, d):
            if access_type == "high":
                print("You have admin access")
                return fn(a, b, c, d)
            if access_type == "mid":
                print("You only have access to a , b & c")
                d = None
                return fn(a, b, c, d)
            if access_type == "low":
                print("You only have access to a & b")
                c, d = None, None
                return fn(a, b, c, d)
            if access_type == "no":
                print("Sorry you don't have any access. Please contact Service desk.")
                return None
        return inner
    return access

@privilege_access('no')
def access_check(a, b, c, d):
    '''This function returns a tuple of the  passed variables'''
    return (a, b, c, d)



# Question 2

from functools import singledispatch
from html import escape
from decimal import Decimal

@singledispatch
def htmlize(a):
    '''Generic htmlize function'''
    return escape(str(a))

@htmlize.register(int)
def html_int(a):
    '''htmlize function for int'''
    return f'{a}(<i>{str(hex(a))}</i>)'

@htmlize.register(float)
def html_real(a):
    '''htmlize function for real float'''
    return f'{round(a, 2)}'

@htmlize.register(Decimal)
def html_real(a):
    '''htmlize function for Decimal'''
    return f'{round(a, 2)}'

def html_escape(arg):
    '''escape function for string'''
    return escape(str(arg))

@htmlize.register(str)
def html_str(s):
    '''htmlize function for string'''
    return html_escape(s).replace('\n', '<br/>\n')

@htmlize.register(tuple)
@htmlize.register(list)
def html_sequence(l):
    '''htmlize function for list and tuple'''
    items = (f'<li>{html_escape(item)}</li>' for item in l)
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

@htmlize.register(dict)
def html_dict(d):
    '''htmlize function for dictionary'''
    items = (f'<li>{k}={v}</li>' for k, v in d.items())
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'
