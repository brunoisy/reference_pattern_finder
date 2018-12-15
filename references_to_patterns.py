import pandas as pd
import numpy as np
from collections import Counter
import re

filename = "shanghai_ip_decisions.csv"
# filename = "shanghai_ip_dockets.csv"


data = pd.read_csv(filename, sep=',').values
ids = data[:,0]
refs = data[:,1]

# simplified ref of each reference := digits replaced with 0
simple_refs = ['' for _ in range(len(ids))]

for (i,r) in enumerate(refs):
    simple_refs[i] = re.sub('_Settlement_IS$','',re.sub('_Complaint_IS$','',re.sub('_Hearing_IS$','',re.sub('[0-9]', '0', r))))

simple_refs = np.array(simple_refs)
patterns = Counter(simple_refs).most_common()
print(patterns)

n_max = patterns[0][1]

A = [['' for _ in range(len(patterns)+1)] for _ in range(n_max+2)]
A[0][0] = 'reference pattern'
A[1][0] = 'number of occurrences'
A[2][0] = 'ids'


for (i,(p,n)) in enumerate(patterns):
    A[0][i+1] = p
    A[1][i+1] = n
    decision_ids = ids[simple_refs == p]
    for (j,id) in enumerate(decision_ids):
        A[j+2][i+1] = id

A = np.asarray(A)
np.savetxt("patterns_and_decisions.csv", A, delimiter=',', fmt='%s')



# creating masks
masks = ['' for _ in range(len(patterns))]
for (i, (p,n)) in enumerate(patterns):
    mask = ''
    for c in p:
        if c.isnumeric():
            mask += '[0-9]'
        elif c == '(' or c == ')':
            mask = mask + '[' + c + ']'
        else:
            mask += c
    masks[i] = mask

global_mask = '^(?i)('+ '|'.join(masks) + ')|(_Hearing_IS|_Complaint_IS|_Settlement_IS)\\?$'# check if works on website (java)

print(global_mask)

# simple test
print(re.match(global_mask, refs[0]) != None)# should be true
print(re.match(masks[0], refs[0])!=None)# should be false
print(re.match(masks[0], refs[902])!=None)# should be true
