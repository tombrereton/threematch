Three Match
---

A bejeweled/candy crush clone.

This game is in development and is being built for a masters project at the University of Birmingham.

Depending on if you have a HiDPi screen or not, you can change the `HD_SCALE` variable
in `threematch.py` under the GLOBAL CONSTANSTS section. Recommended values are between and including 1 and 2.

---
Style guide
---

Refer to the pep-8 website for a consistent style.

[https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

Some sections included below.

**Function Names**

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

```python
def method_name():
    ...
```

mixedCase is allowed only in contexts where that's already the prevailing style (e.g. threading.py), to retain backwards 
compatibility.

**Function and method arguments**

Always use self for the first argument to instance methods.

**For our methods, always declare the type of the parameters, for example:**
```python
def instance_method(self, arg_one: int):
    ...
```

Always use cls for the first argument to class methods.

If a function argument's name clashes with a reserved keyword, it is generally better to append a single trailing 
underscore rather than use an abbreviation or spelling corruption. Thus class_ is better than clss . (Perhaps better 
is to avoid such clashes by using a synonym.)

**Method Names and Instance Variables**

Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.

Use one leading underscore only for non-public methods and instance variables.

```python
def _private_method(self, arg_one: str):
    ...
```

To avoid name clashes with subclasses, use two leading underscores to invoke Python's name mangling rules.

Python mangles these names with the class name: if class Foo has an attribute named __a , it cannot be accessed by 
Foo.__a . (An insistent user could still gain access by calling Foo._Foo__a .) Generally, double leading underscores 
should be used only to avoid name conflicts with attributes in classes designed to be subclassed.

Note: there is some controversy about the use of __names (see below).

