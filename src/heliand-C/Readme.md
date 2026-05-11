# CoNLL and CoNLL-U editions of HeliPaD corpus

Heliand, ms. C

- Initially, the HeliPaD annotations were converted from Penn Historical Treebank annotation to CoNLL-U (`src/helipad/heliand.conllu`).
- This was used to bootstrap an annotation of the Heliand-BT. Their UD annotations were enriched with partial syntax annotations from DDD and B4 (`../../heliand-BT/heliand-bt.conllu`)
- These are projected back to the HeliPaD in order to benefit from corrections/enrichments (`src/heliand-BT/heliand-bt.conllu`).
- Both source annotations are merged, with HeliPaD taking priority in any case of conflict. Heliand-BT is consulted for refinements and extended XPOS annotation. Lemmatization stays intact. If BT alignment fails, no DDD-style POS annotation is given, in particular not `|_`.

## Initial HeliPaD conversion

Go to directory `src/helipad`.

	$> cd src/helipad

### PSD 2 CoNLL

	$> bash -e ./build-conll.sh

retrieves data (heliand.psd) and converts to CoNLL representations with following tabs:

WORD POS LEMMA PARSE

outpout stored in heliand.conll

### CoNLL 2 CoNLL-U

	$> bash -e ./heliand2ud.sh heliand.conll > heliand.conllu

## Annotation projection from Heliand-BT

	$> cd src/heliand-BT
	$> bash -e ./build.sh

## Merging

In the local directory

	$> bash -e ./build.sh
	
## Release

TODO: 

- Align with Heliand-BT and project refined dependency labels and morphosyntactic annotations from there
- Remove empty tokens