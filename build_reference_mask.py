import re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


# return array containing reference format corresponding to each ref (ref with digits replaced by 0 and _..._IS removed)
def to_reference_format(refs):
    reference_formats = ['' for _ in range(len(refs))]

    for (i, r) in enumerate(refs):
        reference_formats[i] = re.sub('_Withdrawal_IS$', '',
                                      re.sub('_Verdict_IS$', '',
                                             re.sub('_Settlement_IS$', '',
                                                    re.sub('_Complaint_IS$', '',
                                                           re.sub('_Hearing_IS$', '',
                                                                  re.sub('[0-9]', '0',r))))))
    return reference_formats


def build_masks(refs):
    reference_formats = list(set(to_reference_format(refs))) #getting all distinct reference formats
    masks = np.empty(len(reference_formats), dtype=object)
    for (i, rf) in enumerate(reference_formats):
        mask = ''
        for c in rf:
            if c==0:
                mask += '[0-9]'
            elif c == '(' or c == ')':
                mask = mask + '[' + c + ']'
            else:
                mask += c
        masks[i] = mask
    return masks


def build_global_mask(refs):
    masks = build_masks(refs)
    global_mask = '^(?i)(' + '|'.join(masks) + ')|(_Hearing_IS|_Complaint_IS|_Settlement_IS|_Verdict_IS|_Withdrawal_IS)\\?$'
    return global_mask



def build_court_masks(court_id):
    engine = create_engine('mysql+pymysql://bruno:bruno@localhost:3327')
    conn = engine.connect()
    query = "SELECT d.reference as decision_ref, dk.reference as docket_ref, dk.court_fk as court " \
            "FROM darts.decision d " \
            "JOIN darts.docket dk on d.docket_fk = dk.id " \
            "JOIN darts.court c on dk.court_fk = c.id " \
            "WHERE d.status <> 'D' " \
            "AND c.id = "+str(court_id)+";"
    result = pd.read_sql(query, conn)

    decision_refs = result["decision_ref"]
    docket_refs = result["docket_ref"]

    decision_ref_mask = build_global_mask(decision_refs)
    docket_ref_mask = build_global_mask(docket_refs)
    return (decision_ref_mask, docket_ref_mask)





# PRV : 285
(decision_ref_mask, docket_ref_mask) = build_court_masks(285)


print(len(decision_ref_mask))
print(decision_ref_mask)
print(len(docket_ref_mask))
print(docket_ref_mask)

