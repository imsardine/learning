%title: Getting Started with tox
%author: imsardine
%date: 2018-06-27

-> # tox?

> *vision: standardize testing in Python*
>
> Test your Python package _against many *interpreter* and *dependency* configs_
>
> [tox automation project](https://tox.readthedocs.io/en/latest/)

 * automatic customizable (re)creation of *virtualenv test environments*
 * installs your _`setup.py` based project_ into each virtual environment
 * test-tool agnostic: runs *pytest*, nose or unittests in a uniform manner

---

-> # Representative Users

 * [tox](https://github.com/tox-dev/tox/blob/master/tox.ini) (of course)
 * [Requests](https://github.com/requests/requests/blob/master/tox.ini)
 * [Flask](https://github.com/pallets/flask/blob/master/tox.ini)
 * [Django](https://github.com/django/django/blob/master/tox.ini)
 * [pytest](https://github.com/pytest-dev/pytest/blob/master/tox.ini)
 * [Pylint](https://github.com/PyCQA/pylint/blob/master/tox.ini)
 * [Ansible](https://github.com/ansible/ansible/blob/devel/tox.ini)
 * [AWS CLI](https://github.com/aws/aws-cli/blob/develop/tox.ini)
 * ...

---

-> # Facing Challenges

 * Python 2 EOL: 2020-01-01
 * A library/framework has to support multiple versions of:
   * Python implementations - CPython 2 & 3, Jython, PyPy, ...
   * 3rd-party dependencies - SQLAlchemy 1.0.x, 1.1, 1.2, ...

> `one_or_none()`
>
> New in version 1.0.9: Added `Query.one_or_none()`
>
> [Query API — SQLAlchemy Documentation](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one_or_none)

*Testing comes to rescue!!*

---

-> # Hello, World! (production code)

hello/__init__.py:

```
def say_hello(who='World'):
    print 'Hello, %s!' % who
```

---

-> # Hello, World! (test code)

tests/test_hello.py:

```
from hello import say_hello
 
def test_hello(capsys):
    say_hello('tox')
    out, _ = capsys.readouterr()
    assert out == 'Hello, tox\n'
```

---

-> # Setup

## Install tox

```
$ virtualenv venv && source venv/bin/activate
$ pip install tox
```

## Directory Structure

```
|- tox.ini
|- setup.py
|- hello/
|  |- __init__.py
|  `- (production code)
|- tests
|  |- __init__.py
|  `- (test code)
`- venv/ (optional, for tox itself)
```

---

-> # Minimal tox.ini

```
[tox]
envlist = py27,py36
 
[testenv]
deps = pytest
commands = pytest --vvv
```

---

-> # Minimal setup.py

```
from setuptools import setup
 
setup(
    name='hello-world',
    packages=['hello'],
)
```

or

```
ERROR: No setup.py file found. The expected location is:
...
```

---

-> # Test Drive

```
$ tox
...
py27 create: path/to/project/.tox/py27
py27 installdeps: pytest
py27 inst: path/to/project/.tox/dist/hello-world-0.0.0.zip
py27 installed: atomicwrites==1.1.5, ... ,hello-world==0.0.0, ...
py27 runtests: PYTHONHASHSEED='2590553851'
py27 runtests: commands[0] | pytest
...
platform darwin -- Python 2.7.10, pytest-3.6.2, py-1.5.3, pluggy-0.6.0
rootdir: path/to/project, inifile:
collected 1 item
 
tests/test_hello.py . [100%]
```

---

-> # Test Drive (cont.)

```
py36 create: path/to/project/.tox/py36
py36 installdeps: pytest
py36 inst: path/to/project/.tox/dist/hello-world-0.0.0.zip
py36 installed: atomicwrites==1.1.5, ... ,hello-world==0.0.0, ...
py36 runtests: PYTHONHASHSEED='2590553851'
py36 runtests: commands[0] | pytest
...
platform darwin -- Python 3.6.4, pytest-3.6.2, py-1.5.3, pluggy-0.6.0
rootdir: path/to/project, inifile:
collected 0 items / 1 errors
 
    from hello import say_hello
E     File "path/to/project/hello/__init__.py", line 2
E       print 'Hello, %s!' % who
E                        ^
...
  py27: commands succeeded
ERROR:   py36: commands failed
```

---

-> # Test Drive (cont.)

hello/__init__.py

```
from __future__ import print_function
 
def say_hello(who='World'):
    print('Hello, %s!' % who)
```

```
$ tox
...
  py27: commands succeeded
  py36: commands succeeded
  congratulations :)
```

---

-> # Virtualenv Test Environments

## Default Environments

 * py, py2, py3
 * py27, py34, py35, py36, py37
 * jython, pypy, pypy3

## envlist in tox.ini

```
[tox]
envlist = py27,py36
 
[testenv]
deps = pytest
commands = pytest
```

---

-> # Matrix (bash-style syntax)

```
[tox]
envlist = py{27,34,36}-django{15,16}-{sqlite,mysql}

[testenv]
deps =
    django15: Django>=1.5,<1.6
    django16: Django>=1.6,<1.7
    py34-mysql: PyMySQL     ; use if both py34 and mysql are in an env name
    py27,py36: urllib3      ; use if any of py36 or py27 are in an env name
    py{27,36}-sqlite: mock  ; mocking sqlite in python 2.x
```

---

-> # Matrix (cont.)

```
[tox]
envlist = {py27,py36}-django{15,16}, docs, flake
```

^

```
$ tox -l
py27-django15
py27-django16
py36-django15
py36-django16
docs
flake
```

---

-> # Makefile & tox.ini

Makefile:

```
venv_dir = $(PWD)/venv
export TEST ?= tests/
 
setup:
	virtualenv $(venv_dir)
	$(venv_dir)/bin/pip install tox==3.0.0
 
test:
	PATH=$(venv_dir)/bin:$(PATH) tox
 
test-py2:
	PATH=$(venv_dir)/bin:$(PATH) tox -e py27
 
test-py3:
	PATH=$(venv_dir)/bin:$(PATH) tox -e py36
```

---

-> # Makefile & tox.ini (cont.)

tox.ini:

```
[tox]
envlist = py27,py36
 
[testenv]
setenv = PYTHONDONTWRITEBYTECODE = 1
deps = pytest
commands = pytest
```

Usage:

```
$ make test
$ make test-py2
$ TEST=tests/test_hello.py::test_xxx make test-py3
```
