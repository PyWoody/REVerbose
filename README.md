# REVerbose
## Regex for the Lazy

REVerbose was created to make creating complicated Regular Expressions easier to generate without having to memorize specialized syntaxes. With REVerbose, all you need to do is build up a series of pre-defined words and the Regular Expression is genenerated automatically. The `Regex.compiled` property will return your compiled Regular Expression that can be used for the standard `.search`, `.match`, `.fullmatch`, `.sub`, `.subn`, `.split`, `.findall`, and `.finditer` functions.


### Basic example

```python3
import re
import REVerbose as rev

>>> regex = rev.LINE_START + rev.ANY_DIGIT
>>> print(regex)
^\d
>>> repr(regex)
'Regex(Caret(chars=r""), AnyDigit())'
>>> regex.search('99 Red Balloons')
<re.Match object; span=(0, 1), match='9'>
```

Compiling a regular expression in steps:

```python3
>>> regex = rev.LINE_START
>>> regex += rev.ANYTHING
>>> regex += rev.ANY_WORD_GROUPS(['something', 'wicked'])
>>> regex += rev.ANY
>>> regex += rev.ALL_OR_NONE
>>> regex += rev.LINE_END
>>> print(regex)
^.*something|wicked.*$
>>> regex.search('something wicked this way comes').group()
'something'
>>> regex.search('SOMETHING WICKED THIS WAY COMES', re.IGNORECASE).group()
'SOMETHING'
```


### Extended Features

Since the compiled Regular Expression objects are hashable, they can be used in tuples and as dictionary keys.

```python3
>>> results = collections.defaultdict(list)
>>> contains_cat_or_dog = rev.WHITESPACE
>>> contains_cat_or_dog += rev.ZERO_OR_ONE
>>> contains_cat_or_dog += rev.ANY_WORD_GROUPS(['cat', 'dog'])
>>> contains_cat_or_dog += rev.ZERO_OR_ONE(rev.WHITESPACE)
>>> regexes = [
    contains_cat_or_dog,
    rev.LINE_START + rev.WORD_GROUP('Macbeth')
]
>>> with open(r'data/macbeth_1533-0.txt', 'r', encoding='utf8') as f:
...  for line in f:
...   for regex in regexes:
...    if match := regex.search(line):
...     results[regex].append(match)
>>> for key, values in results.items():
...  print(f'{str(key)} ({repr(key)})')
...  for result in values:
...   print(f'\t{result}')
...
\s?cat|dog\s? (Regex(AnyWhitespaceCharacter(), ZeroOrOne(chars=r""), AnyWordGroup([r"cat", r"dog"]), ZeroOrOne(chars=r"\s")))
        <re.Match object; span=(36, 39), match='cat'>
        <re.Match object; span=(59, 62), match='cat'>
        <re.Match object; span=(2, 6), match=' cat'>
        <re.Match object; span=(15, 18), match='cat'>
        <re.Match object; span=(37, 41), match=' cat'>
        <re.Match object; span=(13, 17), match=' cat'>
        <re.Match object; span=(7, 10), match='cat'>
        <re.Match object; span=(47, 50), match='cat'>
        <re.Match object; span=(36, 39), match='cat'>
        <re.Match object; span=(6, 9), match='cat'>
        <re.Match object; span=(61, 64), match='cat'>
        <re.Match object; span=(35, 38), match='cat'>
        <re.Match object; span=(10, 14), match=' cat'>
        <re.Match object; span=(19, 22), match='dog'>
        <re.Match object; span=(38, 41), match='cat'>
        <re.Match object; span=(44, 47), match='cat'>
        <re.Match object; span=(16, 19), match='cat'>
        <re.Match object; span=(4, 8), match=' cat'>
        <re.Match object; span=(18, 22), match=' cat'>
        <re.Match object; span=(27, 30), match='dog'>
        <re.Match object; span=(9, 12), match='cat'>
        <re.Match object; span=(10, 13), match='cat'>
        <re.Match object; span=(25, 28), match='cat'>
        <re.Match object; span=(20, 23), match='dog'>
        <re.Match object; span=(19, 22), match='cat'>
        <re.Match object; span=(25, 28), match='cat'>
        <re.Match object; span=(28, 31), match='cat'>
        <re.Match object; span=(53, 56), match='cat'>
        <re.Match object; span=(57, 60), match='cat'>
        <re.Match object; span=(12, 15), match='cat'>
        <re.Match object; span=(21, 24), match='cat'>
        <re.Match object; span=(56, 59), match='cat'>
        <re.Match object; span=(13, 16), match='cat'>
        <re.Match object; span=(61, 64), match='cat'>
        <re.Match object; span=(38, 41), match='cat'>
        <re.Match object; span=(58, 61), match='cat'>
^(Macbeth) (Regex(Caret(chars=r""), Group(group=r"Macbeth")))
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
```

You could easily take advantage of this for use in Counters:

```python3
>>> counter = collections.Counter()
>>> words = rev.ZERO_OR_ONE(rev.WHITESPACE)
>>> words += rev.ALL_OR_NONE(rev.ANY_WORD)
>>> words += rev.ZERO_OR_ONE(rev.WHITESPACE)
>>> regexes = [words, rev.compile(rev.WHITESPACE)]
>>> with open(r'data/macbeth_1533-0.txt', 'r', encoding='utf8') as f: 
...  for line in f:
...   for regex in regexes:
...    for match in regex.finditer(line):
...     if match: counter[regex] += 1
... 
>>> counter
Counter({Regex(ZeroOrOne(chars=r"\s"), Asterik(chars=r"\w"), ZeroOrOne(chars=r"\s")): 37198, Regex(AnyWhitespaceCharacter()): 22654})```


## TODO:
- Set words in stone w/ descriptions
- Add remaining functions from `re`
- Add additional sytnaxes supported by Python
- Reevaluate how match v. non-matching groups are captured
- Negations
