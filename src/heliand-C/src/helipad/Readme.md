# CoNLL and CoNLL-U editions of HeliPaD corpus

Heliand, ms. C

converted from Penn Historical Treebank annotation

## PSD 2 CoNLL

run

> $> ./build-conll.sh

retrieves data (heliand.psd) and converts to CoNLL representations with following tabs:

WORD POS LEMMA PARSE

outpout stored in heliand.conll

## CoNLL 2 CoNLL-U

run > $> ./heliand2ud.sh heliand.conll > heliand.conllu

creates CoNLL-U representation in heliand.conllu.
Note that the heliand2ud.sh script can be configured to produce different output (see section "OUTPUT or DEBUG" in the script).

Note that we do not yet remove empty tokens. A pilot for this has been prepared in remove-empty-tokens.sparql, but it does not yet update the token numbering.

## Pruning

Used to produce training data for building a parser. Note that we skip a (small) number of sentences with multiple roots.

	$> cat heliand.conllu | python3 prune-toks.py > heliand.pruned.conllu