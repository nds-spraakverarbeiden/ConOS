# Heliand-BT-based annotation of Heliand-M corpus

- Take tokenized Heliand-M as basis ([`../txt/40001B.conll`](../txt/40001B.conll))
- Align with Heliand-BT, enforce Heliand-BT sentence breaks and copy Heliand-BT annotations ([`heliand-bt.raw.conll`](heliand-bt.raw.conll))
- Convert to CoNLL-U ([`heliand-bt.conllu`](heliand-bt.conllu))
	
	Note that the result is a partial annotation, because dependencies etc. will be empty in case of alignment errors of segmentation differences. So, this should be complemented with the results of an automated parse.


To reproduce, run

		$> build.sh

