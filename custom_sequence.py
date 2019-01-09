from skbio.sequence import GrammaredSequence
from skbio.util import classproperty
import string


class CustomSequence(GrammaredSequence):
    @classproperty
    def degenerate_map(cls):
        return {}

    @classproperty
    def definite_chars(cls):
        return set(string.ascii_lowercase+string.ascii_uppercase+"0"+"-_/()")


    @classproperty
    def default_gap_char(cls):
        return '.'

    @classproperty
    def gap_chars(cls):
        return set('.')