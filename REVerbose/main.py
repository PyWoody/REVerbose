import re

from collections import abc


# TODO: Make sure all items that can accept inputs do
#       i.e., End should accept something so you can do ...$

# TODO: Find a way to normalize names so all iterable classes are obvious
#       Maybe 'ALL' and 'ANY' will work

# NOTE: Since Regex is hashable, it can be used as a key in a dict
#       results = defaultdict(list)
#       regexes = [Regex(...), ..., N]
#       with open(some_file) as f:
#           for line in file:
#               for regex in regexes:
#                   if match := regex.search(line):
#                       results[regex].append(match.group())
#       print(results[regexes[0])
#
#
#       Would also be good for counters
#       results = Counter()  # maybe double-check
#       regexes = [Regex(...), ..., N]
#       with open(some_file) as f:
#           for line in file:
#               for regex in regexes:
#                   if regex.search(line):
#                       results[regex] += 1
#       print(results.max()) # or whatever


class BaseAdder:

    def __init__(self, *args, **kwargs):
        if any([args, kwargs]):
            cls = self.__class__.__name__
            raise NotImplementedError(
                f'{cls}() Does not accept positional or keyword arguments'
            )

    def __call__(self, *args, **kwargs):
        cls = self.__class__.__name__
        raise NotImplementedError(f'{cls} cannot be called')

    def __repr__(self):
        if isinstance(self, abc.Iterable):
            args = []
            for arg in self:
                if isinstance(arg, str):
                    args.append(f'r"{arg}"')
                else:
                    args.append(str(repr(arg)))
            args = f"[{', '.join(args)}]"
        elif items := self.__dict__.items():
            args = ', '.join([f'{k}="{v}"' for k, v in items])
        else:
            args = ''
        return rf'{self.__class__.__name__}({args})'

    def __add__(self, other):
        if not isinstance(other, Regex):
            if not issubclass(type(other), BaseAdder):
                raise TypeError(f'Cannot concatenate Regex and {type(other)}')
        if isinstance(self, Regex):
            return Regex(*self.parts, other)
        return Regex(self, other)

    def __iadd__(self, other):
        if not isinstance(other, Regex):
            if not issubclass(type(other), BaseAdder):
                raise TypeError(f'Cannot concatenate Regex and {type(other)}')
        if isinstance(self, Regex):
            self.parts.append(other)
            return self
        return Regex(self, other)


class Regex(BaseAdder):

    def __init__(self, *parts, flags=0):
        self.parts = list(parts)
        self.flags = flags
        self.__compiled = None

    def __repr__(self):
        words = ', '.join([repr(p) for p in self.parts])
        return rf'{self.__class__.__name__}({words})'

    def __str__(self):
        return r''.join([str(p) for p in self.parts])

    def __getitem__(self, index):
        return str(self)[index]

    def __contains__(self, item):
        return item in str(self)

    def __iter__(self):
        yield from str(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return isinstance(other, Regex) and str(self) == str(other)

    def __hash__(self):
        return hash(repr(self))

    @property
    def compiled(self):
        if self.__compiled is None:
            self.__compiled = re.compile(str(self), self.flags)
        return self.__compiled

    # NOTE: Tmp placeholders for demonstration
    def search(self, line):
        return self.compiled.search(line)

    def match(self, line):
        return self.compiled.match(line)


class AnyAlphanumericWord(BaseAdder):
    """Matches any alphanumeric character;
   this is equivalent to the class [a-zA-Z0-9_]
    
   Documentation Source: https://docs.python.org/3/howto/regex.html
                         by A.M. Kuchling <amk@amk.ca>
    """

    def __str__(self):
        return r'\w'


class AnyNonAlphanumericWord(BaseAdder):
    """Matches any non-alphanumeric character;
   this is equivalent to the class [^a-zA-Z0-9_]
    
   Documentation Source: https://docs.python.org/3/howto/regex.html
                         by A.M. Kuchling <amk@amk.ca>
    """

    def __str__(self):
        return r'\W'


class AnyDigit(BaseAdder):
    """Matches any decimal digit; this is equivalent to the class [0-9]

   Documentation Source: https://docs.python.org/3/howto/regex.html
                         by A.M. Kuchling <amk@amk.ca>
    """

    def __str__(self):
        return r'\d'


class AnyNonDigit(BaseAdder):
    """Matches any non-digit character; this is equivalent to the class [^0-9]
        
   Documentation Source: https://docs.python.org/3/howto/regex.html
                         by A.M. Kuchling <amk@amk.ca>
    """

    def __str__(self):
        return r'\D'


class AnyWhitespaceCharacter(BaseAdder):
    """Matches any whitespace character;
   this is equivalent to the class [ \t\n\r\f\v]
    
   Documentation Source: https://docs.python.org/3/howto/regex.html
                         by A.M. Kuchling <amk@amk.ca>
    """

    def __str__(self):
        return r'\s'


class AnyNonWhitespaceCharacter(BaseAdder):
    """Matches any non-whitespace character;
   this is equivalent to the class [^ \t\n\r\f\v]
    
   Documentation Source: https://docs.python.org/3/howto/regex.html
                         by A.M. Kuchling <amk@amk.ca>
    """

    def __str__(self):
        return r'\S'


class AnyWordGroup(BaseAdder):
    """
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, groups):
        self.groups = list(groups)

    @classmethod
    def __call__(cls, groups):
        return cls(groups)

    def __iter__(self):
        yield from self.groups

    def __str__(self):
        return r'|'.join([str(g) for g in self.groups])


class Asterik(BaseAdder):
    """Causes the resulting RE to match 0 or more repetitions of the
    preceding RE, as many repetitions as are possible.
    ab* will match ‘a’, ‘ab’, or ‘a’ followed by any number of ‘b’s.
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, chars=''):
        self.chars = str(chars)

    @classmethod
    def __call__(cls, chars=''):
        return cls(chars)

    def __str__(self):
        return rf'{self.chars}*'


class BackReference(BaseAdder):
    """A backreference to a named group; it matches whatever text was
    matched by the earlier group named name

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, ref):
        self.ref = str(ref)

    @classmethod
    def __call__(cls, ref):
        return cls(ref)

    def __str__(self):
        return rf'(?P={self.ref})'


class Caret(BaseAdder):
    """(Caret.) Matches the start of the string, and in MULTILINE mode also
    matches immediately after each newline.
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, chars=''):
        self.chars = str(chars)

    @classmethod
    def __call__(cls, chars=''):
        return cls(chars)

    def __str__(self):
        return rf'^{self.chars}'


class Comment(BaseAdder):
    """A comment; the contents of the parentheses are simply ignored

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, comment):
        self.comment = str(comment)

    @classmethod
    def __call__(cls, comment):
        return cls(comment)

    def __str__(self):
        return rf'(?#{self.comment})'


class Dot(BaseAdder):
    """(Dot.) In the default mode, this matches any character except a newline.
    If the DOTALL flag has been specified, this matches any character
    including a newline.
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __str__(self):
        return r'.'


class End(BaseAdder):
    """Matches the end of the string or just before the newline at the end
    of the string, and in MULTILINE mode also matches before a newline.
    foo matches both ‘foo’ and ‘foobar’, while the regular expression foo$
    matches only ‘foo’. More interestingly, searching for foo.$ in
    'foo1\nfoo2\n' matches ‘foo2’ normally, but ‘foo1’ in MULTILINE mode;
    searching for a single $ in 'foo\n' will find two (empty) matches:
    one just before the newline, and one at the end of the string.
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, word=''):
        self.word = str(word)

    @classmethod
    def __call__(cls, word=''):
        return cls(word)

    def __str__(self):
        return r'{self.word}$'


class Escape(BaseAdder):
    """Either escapes special characters (permitting you to match characters
    like '*', '?', and so forth), or signals a special sequence;
    special sequences are discussed below.

    Please note all classes use raw strings by default

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, char=''):
        self.char = str(char).lstrip(r'\\')

    @classmethod
    def __call__(cls, char=''):
        return cls(char)

    def __str__(self):
        return rf'\{self.char}'


class Group(BaseAdder):
    """Matches whatever regular expression is inside the parentheses,
    and indicates the start and end of a group; the contents of a group
    can be retrieved after a match has been performed, and can be matched
    later in the string with the \number special sequence, described below.
    To match the literals '(' or ')', use \( or \), or enclose them inside
    a character class: [(], [)]
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, group):
        self.group = str(group)

    @classmethod
    def __call__(cls, group):
        return cls(group)

    def __str__(self):
        return rf'({self.group})'


class List(BaseAdder):
    """

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, chars):
        self.chars = list(chars)

    @classmethod
    def __call__(cls, chars):
        return cls(chars)

    def __iter__(self):
        yield from self.chars

    def __str__(self):
        return rf'[{r"".join([str(i) for i in self.chars])}]'


class LookAheadAssertion(BaseAdder):
    """Matches if ... matches next, but doesn’t consume any of the string.
    This is called a lookahead assertion.

    For example, Isaac (?=Asimov) will match 'Isaac ' only if it’s
    followed by 'Asimov'

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, assertion):
        self.assertion = str(assertion)

    @classmethod
    def __call__(cls, assertion):
        return cls(assertion)

    def __str__(self):
        return rf'(?={self.assertion})'


class NamedGroup(BaseAdder):
    """Similar to regular parentheses, but the substring matched by the
    group is accessible via the symbolic group name name. Group names must
    be valid Python identifiers, and each group name must be defined only
    once within a regular expression. A symbolic group is also a numbered
    group, just as if the group were not named.

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, name, group):
        self.name = str(name)
        self.group = str(group)

    @classmethod
    def __call__(cls, name, group):
        return cls(name, group)

    def __str__(self):
        return rf'(?P<{self.name}>{self.group})'


class NegativeLookAhead(BaseAdder):
    """Matches if ... doesn’t match next. This is a negative lookahead
    assertion. For example, Isaac (?!Asimov) will match 'Isaac ' only
    if it’s not followed by 'Asimov'

    Documentation Source: https://docs.python.org/3/library/re.html
    """
    def __init__(self, assertion):
        self.assertion = str(assertion)

    @classmethod
    def __call__(cls, assertion):
        return cls(assertion)

    def __str__(self):
        return rf'(?!{self.assertion})'


class NonMatchingGroup(BaseAdder):
    """A non-capturing version of regular parentheses. Matches whatever
    regular expression is inside the parentheses, but the substring
    matched by the group cannot be retrieved after performing a match
    or referenced later in the pattern

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, group):
        self.group = str(group)

    @classmethod
    def __call__(cls, group):
        return cls(group)

    def __str__(self):
        return rf'(?:{self.group})'


class Period(BaseAdder):
    """An escpaed, r'\.', period"""

    def __str__(self):
        return r'\.'


class Plus(BaseAdder):
    """Causes the resulting RE to match 1 or more repetitions of the
    preceding RE. ab+ will match ‘a’ followed by any non-zero number
    of ‘b’s; it will not match just ‘a’.
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, chars=''):
        self.chars = str(chars)

    @classmethod
    def __call__(cls, chars=''):
        return cls(chars)

    def __str__(self):
        return rf'{self.chars}+'


class PositiveLookBehindAssertion(BaseAdder):
    """Matches if the current position in the string is preceded by
    a match for ... that ends at the current position. This is called a
    positive lookbehind assertion. (?<=abc)def will find a match in 'abcdef',
    since the lookbehind will back up 3 characters and check if the contained
    pattern matches. The contained pattern must only match strings of some 
    ixed length, meaning that abc or a|b are allowed, but a* and a{3,4} are
    not. Note that patterns which start with positive lookbehind assertions
    will not match at the beginning of the string being searched; you will
    most likely want to use the search() function rather than the match()
    function

    Documentation Source: https://docs.python.org/3/library/re.html
    """
    def __init__(self, assertion, query):
        self.assertion = str(assertion)
        self.query = str(query)

    @classmethod
    def __call__(cls, assertion, query):
        return cls(assertion, query)

    def __str__(self):
        return rf'(?<={self.assertion}){self.query}'


class QuestionMark(BaseAdder):
    """An escpaed, r'\?', question mark"""

    def __str__(self):
        return r'\?'


class StringStartsWith(BaseAdder):
    """Matches only at the start of the string.

    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, word):
        self.word = str(word)

    @classmethod
    def __call__(cls, word):
        return cls(word)

    def __str__(self):
        return rf'\A{self.word}'


class ZeroOrOne(BaseAdder):
    """Causes the resulting RE to match 0 or 1 repetitions of the preceding RE.
    ab? will match either ‘a’ or ‘ab’.
        
    Documentation Source: https://docs.python.org/3/library/re.html
    """

    def __init__(self, chars=''):
        self.chars = str(chars)

    @classmethod
    def __call__(cls, chars=''):
        return cls(chars)

    def __str__(self):
        return rf'{self.chars}?'



def compile(regex, flags=0):
    return re.compile(str(regex), flags=flags)


ALL_OR_NONE = Asterik()
ANY = Dot()
ANY_DIGIT = AnyDigit()
ANY_NON_DIGIT = AnyNonDigit()
ANY_NON_WORD = AnyNonAlphanumericWord()
ANY_WORD = AnyAlphanumericWord()
ANY_WORD_GROUP = AnyWordGroup
BACK_REFERENCE = BackReference
COMMENT = Comment
ESCAPE = Escape()
GROUP = Group
LINE_END = End()
LINE_START = Caret()
LIST = List
LOOK_AHEAD = LookAheadAssertion
NAMED_GROUP = NamedGroup
NEGATIVE_LOOK_AHEAD = NegativeLookAhead
NON_WHITESPACE = AnyNonWhitespaceCharacter()
NON_MATCHING_GROUP = NonMatchingGroup
ONE_OR_MORE = Plus
PERIOD = Period()
POSITIVE_LOOK_BEHIND = PositiveLookBehindAssertion
STRING_STARTS_WITH = StringStartsWith
QUESTION_MARK = QuestionMark()
WHITESPACE = AnyWhitespaceCharacter()
ZERO_OR_ONE = ZeroOrOne


__all__ = (
    compile,
    ALL_OR_NONE,
    ANY,
    ANY_DIGIT,
    ANY_NON_DIGIT,
    ANY_NON_WORD,
    ANY_WORD,
    ANY_WORD_GROUP,
    BACK_REFERENCE,
    COMMENT,
    ESCAPE,
    GROUP,
    LINE_END,
    LINE_START,
    LIST,
    LOOK_AHEAD,
    NAMED_GROUP,
    NEGATIVE_LOOK_AHEAD,
    NON_WHITESPACE,
    NON_MATCHING_GROUP,
    ONE_OR_MORE,
    PERIOD,
    POSITIVE_LOOK_BEHIND,
    STRING_STARTS_WITH,
    QUESTION_MARK,
    WHITESPACE,
    ZERO_OR_ONE,
)


if __name__ == '__main__':
    ANY = Dot()
    ANY_WORD = AnyWordGroup()
    LINE_START = Caret()
    LINE_END = End()
    ALL_OR_NONE = Asterik()
    ONE_OR_MORE = Plus()
    ZERO_OR_ONE = QuestionMark()
    GROUP = Group()
    output = LINE_START
    output += ANY
    output += ANY_WORD(['fart', 'tacos'])
    output += GROUP(['test', ANY, 'fart', ONE_OR_MORE])
    output += GROUP([r'C:\test\file\name'])
    output += LINE_END
    print(output)
    print(type(output))
    print(str(output))
    print(repr(output))
    print(output())

    print(hash(eval(repr(output))), hash(output))
    print(hash(eval(repr(output))) == hash(output))
    print(eval(repr(output)) == output)
    print(str(eval(repr(output))) == str(output))
    print(eval(repr(output))())
