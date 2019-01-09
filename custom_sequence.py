from skbio.sequence import GrammaredSequence
from skbio.util import classproperty
import string


subst_matrix = {}
for x1 in string.ascii_lowercase+string.ascii_uppercase:
    subst_matrix[x1]={}
    for x2 in string.ascii_lowercase+string.ascii_uppercase:
        if x1 == x2:
            subst_matrix[x1][x2] = 1
        else:
            subst_matrix[x1][x2] = -1
    for x2 in "0":
        subst_matrix[x1][x2] = -100
    for x2 in "-_/()":
        subst_matrix[x1][x2] = -100
for x1 in "0":
    subst_matrix[x1]={}
    for x2 in string.ascii_lowercase+string.ascii_uppercase:
        subst_matrix[x1][x2] = -100
    for x2 in "0":
        subst_matrix[x1][x2] = 1
    for x2 in "-_/()":
        subst_matrix[x1][x2] = -100
for x1 in "-_/()":
    subst_matrix[x1]={}
    for x2 in string.ascii_lowercase+string.ascii_uppercase:
        subst_matrix[x1][x2] = -100
    for x2 in "0":
        subst_matrix[x1][x2] = -100
    for x2 in "-_/()":
        if x1 == x2:
            subst_matrix[x1][x2] = 1
        else:
            subst_matrix[x1][x2] = -100



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