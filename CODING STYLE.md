# Coding Style Guidelines

In general, this document outlines the coding style guidelines (which follow
[PEP 0008](https://www.python.org/dev/peps/pep-0008/), the official style
document)  that should be followed when __writing new code__. If you need
clarification or  more details please look there first.

If you are modifying existing code please do this:

* Do not include substantial changes in the same commit as coding style changes.
* Only modify existing code to fit these guidelines if you are already modifying
 that code for other reasons (substantial changes/additions), or you have
 nothing better to do (unlikely).

## The Zen of Python, by Tim Peters

* Beautiful is better than ugly.
* Explicit is better than implicit.
* Simple is better than complex.
* Complex is better than complicated.
* Flat is better than nested.
* Sparse is better than dense.
* Readability counts.
* Special cases aren't special enough to break the rules.
* Although practicality beats purity.
* Errors should never pass silently.
* Unless explicitly silenced.
* In the face of ambiguity, refuse the temptation to guess.
* There should be one -- and preferably only one -- obvious way to do it.
* Although that way may not be obvious at first unless you're Dutch.
* Now is better than never.
* Although never is often better than _right_ now.
* If the implementation is hard to explain, it's a bad idea.
* If the implementation is easy to explain, it may be a good idea.
* Namespaces are one honking great idea -- let's do more of those!

## Code Layout

### Indentation

* 4 spaces per indentation level (Never use hard tabs).
* This should be setup correctly by default in Atom.

### Maximum Line Length

* Limit lines to a maximum of 80 characters. Atom gives a guideline for this.
  * Exception: URLs should not be broken over multiple lines.

### Blank Lines

* Surround top-level function and class definitions with two blank lines.
* Surround method definitions inside a class with single blank lines.
* Use blank lines in functions, sparingly, to indicate logical sections.

### Imports

* Imports should each be on their own line.
* Imports should be at the top of the source file, immediately following any
 comments and before any other code.

## String Quotes

* Use double quotes to enclose strings, unless the string contains double quotes
 in it. In that case switch them.

## Whitespace in expressions

* Do not put spaces immediately inside parenthesis. `( x )` = bad, `(x)` = good.
* Put a single space after a comma, but not before it.
* Put a space on both sides of an `==` or other equality operator (`!=`,
   `>=`, `<=` etc).
* Do not put spaces around an `=` sign or other assignment operators.

## comments

* Update any relevant comments when you modify code.
* User proper English in your comments. That includes using full sentences.
* Syntax: `#` (followed by a space) for each line comment line.
* Don't Use in-line comments to explain the obvious.
  * Bad:
  ```python
  x += 1 #increment x by 1
  ```
  * Good:
  ```python
  x += 1   #compensate for border overlap
  ```

### Documentation Strings

Insert documentation strings to functions and methods when application. These
will show up when using auto-complete features. They are placed at the very
beginning of the function/method. Syntax:
```python
""" Returns a foobang

Optional plotz says to frobnicate the bizbaz first.
"""
```
Make sure the closing `"""` is on it's own line if the documentation string is
 multiple lines. It can go on the same line as the text if it is a single line
 documentation string.

## Naming Conventions

* Never use the characters 'l' (lowercase letter el), 'O' (uppercase letter oh),
 or 'I' (uppercase letter eye) as single character variable names.
* `package_name`, `module_name`, `function_name`, `method_name`, `instance_variable`,
* `ClassNames`
* `ExceptionNameError`, or `ExceptionNameException` depending on whether the
 exception is an error or just an exception.
* `CONSTANT_NAME`
