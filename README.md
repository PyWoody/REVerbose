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
>>> contains_cats_or_dogs = rev.ONE_OR_MORE(
    rev.NON_MATCHING_GROUPS([rev.LINE_START, rev.WHITESPACE])
)
>>> contains_cats_or_dogs += rev.NON_MATCHING_GROUPS(['cat', 'dog'])
>>> contains_cats_or_dogs += rev.NON_MATCHING_GROUPS(
    [rev.LINE_END, rev.PERIOD, rev.WHITESPACE, 's']
)
>>> regexes = [
    contains_cats_or_dogs,
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
^(Macbeth) (Regex(Caret(chars=r""), Group(group=r"Macbeth")))
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
        <re.Match object; span=(0, 7), match='Macbeth'>
(?:^|\s)+(?:cat|dog)(?:$|\.|\s|s) (Regex(Plus(chars=r"(?:^|\s)"), NonMatchingGroups([r"cat", r"dog"]), NonMatchingGroups([End(word=r""), Period(), AnyWhitespaceCharacter(), r"s"])))
        <re.Match object; span=(13, 18), match=' cat '>
        <re.Match object; span=(18, 23), match=' dogs'>
        <re.Match object; span=(18, 23), match=' cat '>
        <re.Match object; span=(19, 24), match=' dogs'>```
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
```


## TODO:
- Set words in stone w/ descriptions
- Add remaining functions from `re`
- Add additional sytnaxes supported by Python
- Reevaluate how match v. non-matching groups are captured
- Negations
