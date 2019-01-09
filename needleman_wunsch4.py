#http://readiab.org/book/0.1.3/2/1

from skbio.alignment import global_pairwise_align
# %psource global_pairwise_align

@experimental(as_of="0.4.0")
def global_pairwise_align(seq1, seq2, gap_open_penalty, gap_extend_penalty,
                          substitution_matrix, penalize_terminal_gaps=False):
    """Globally align a pair of seqs or alignments with Needleman-Wunsch

    Parameters
    ----------
    seq1 : GrammaredSequence or TabularMSA
        The first unaligned sequence(s).
    seq2 : GrammaredSequence or TabularMSA
        The second unaligned sequence(s).
    gap_open_penalty : int or float
        Penalty for opening a gap (this is substracted from previous best
        alignment score, so is typically positive).
    gap_extend_penalty : int or float
        Penalty for extending a gap (this is substracted from previous best
        alignment score, so is typically positive).
    substitution_matrix: 2D dict (or similar)
        Lookup for substitution scores (these values are added to the
        previous best alignment score).
    penalize_terminal_gaps: bool, optional
        If True, will continue to penalize gaps even after one sequence has
        been aligned through its end. This behavior is true Needleman-Wunsch
        alignment, but results in (biologically irrelevant) artifacts when
        the sequences being aligned are of different length. This is ``False``
        by default, which is very likely to be the behavior you want in all or
        nearly all cases.

    Returns
    -------
    tuple
        ``TabularMSA`` object containing the aligned sequences, alignment score
        (float), and start/end positions of each input sequence (iterable
        of two-item tuples). Note that start/end positions are indexes into the
        unaligned sequences.

    See Also
    --------
    local_pairwise_align
    local_pairwise_align_protein
    local_pairwise_align_nucleotide
    skbio.alignment.local_pairwise_align_ssw
    global_pairwise_align_protein
    global_pairwise_align_nucelotide

    Notes
    -----
    This algorithm (in a slightly more basic form) was originally described
    in [1]_. The scikit-bio implementation was validated against the
    EMBOSS needle web server [2]_.

    This function can be use to align either a pair of sequences, a pair of
    alignments, or a sequence and an alignment.

    References
    ----------
    .. [1] A general method applicable to the search for similarities in
       the amino acid sequence of two proteins.
       Needleman SB, Wunsch CD.
       J Mol Biol. 1970 Mar;48(3):443-53.
    .. [2] http://www.ebi.ac.uk/Tools/psa/emboss_needle/

    """
    warn("You're using skbio's python implementation of Needleman-Wunsch "
         "alignment. This is known to be very slow (e.g., thousands of times "
         "slower than a native C implementation). We'll be adding a faster "
         "version soon (see https://github.com/biocore/scikit-bio/issues/254 "
         "to track progress on this).", EfficiencyWarning)

    for seq in seq1, seq2:
        # We don't need to check the case where `seq` is a `TabularMSA` with a
        # dtype that isn't a subclass of `GrammaredSequence`, this is
        # guaranteed by `TabularMSA`.
        if not isinstance(seq, (GrammaredSequence, TabularMSA)):
            raise TypeError(
                "`seq1` and `seq2` must be GrammaredSequence subclasses or "
                "TabularMSA, not type %r" % type(seq).__name__)

    seq1 = _coerce_alignment_input_type(seq1)
    seq2 = _coerce_alignment_input_type(seq2)

    if seq1.dtype is not seq2.dtype:
        raise TypeError(
            "`seq1` and `seq2` must have the same dtype: %r != %r"
            % (seq1.dtype.__name__, seq2.dtype.__name__))

    if penalize_terminal_gaps:
        init_matrices_f = _init_matrices_nw
    else:
        init_matrices_f = _init_matrices_nw_no_terminal_gap_penalty

    score_matrix, traceback_matrix = \
        _compute_score_and_traceback_matrices(
            seq1, seq2, gap_open_penalty, gap_extend_penalty,
            substitution_matrix, new_alignment_score=-np.inf,
            init_matrices_f=init_matrices_f,
            penalize_terminal_gaps=penalize_terminal_gaps)

    end_row_position = traceback_matrix.shape[0] - 1
    end_col_position = traceback_matrix.shape[1] - 1

    aligned1, aligned2, score, seq1_start_position, seq2_start_position = \
        _traceback(traceback_matrix, score_matrix, seq1, seq2,
                   end_row_position, end_col_position)
    start_end_positions = [(seq1_start_position, end_col_position-1),
                           (seq2_start_position, end_row_position-1)]

    msa = TabularMSA(aligned1 + aligned2)

    return msa, score, start_end_positions