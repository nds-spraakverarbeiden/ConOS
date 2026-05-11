# Heliand-BT-based annotation of Helipad corpus

- Take full HeliPaD (WORD, LEMMA, XPOS, UPOS, FEATS) as basis.
- Drop empty words.
- Calculate IDs.
- Align with Heliand-BT, enforce HeliPaD sentence splits, and copy Heliand-BT annotations (see `heliand-bt.conll`)
- Convert to conjoint CoNLL-U representation (see `heliand-bt.conllu`)

Note that the result is a partial annotation, because dependencies etc. will be empty in case of alignment errors of segmentation differences. So, wherever a HeliPaD-based annotation contradicts a Heliand-BT annotation, it should take priority.

