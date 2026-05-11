
# Heliand, DDD v1.1, UD edition

- CoNLL-U edition
- source data from https://www.deutschdiachrondigital.de/, CC-BY-NC 3.0
- The original data contained lemmatization, parts of speech, morphosyntactic features and information on clause linking (but no systematic parses) in ELAN format.
- CoNLL conversion using the ELAN2CoNLL converter from https://github.com/acoli-repo/conll-merge/tree/master/cmd/elan2conll
- XPOS: Based on a mapping of DDD annotations to HeliPaD parts of speech, developed with CoNLL-Merge by CC.
- UPOS: Based on a mapping of DDD annotations to an earlier UD interpretation of HeliPaD parts of speech, developed by CC.
- HEAD/DEP: automatically created using a parser trained on an UD interpretation of HeliPaD created by CC.

Data
==

- `ddd-heliand-v1.1.conll` CoNLL conversion ("EAF-CoNLL") of the original ELAN data
- `ddd-plus-helipad.conll` EAF-CoNLL file with HeliPaD UD annotations appended [superseded by `ddd-heliand.parsed.full.conll`]
- `ddd-heliand-v1.1-helipad-emulation.conll` heuristic mapping to HeliPaD/UD conventions [this is for verifiability only, do not work with this file]
- `osx_ddd-heliand.pruned.parsed.conllu` automated parse of the HeliPaD-mapped file, created by UDPipe v.1 trained over the *full* HeliPaD/UD edition [note that this file uses HeliPaD normalization]
- **`ddd-heliand.parsed.full.conll`** automated parse with DDD forms and annotations restored and manual HeliPaD/UD annotations aligned [*this file contains the full data*]
- **`ddd-heliand.parsed.conllu`** CoNLL-U excerpt from the full parse, so far using the automated parse alone


DDD Heliand vs. HeliPaD
==

- [ELAN2CoNLL](https://github.com/acoli-repo/conll-merge/tree/master/cmd/elan2conll): Initially, created a first CoNLL version from ELAN data (`ddd-heliand-v1.1.conll`), contains morphosyntactic annotations, but no syntax.
- `merge.sh`: Use [CoNLL-Merge](https://github.com/acoli-repo/conll-merge) to align the result with a CoNLL edition of HeliPaD corpus created beforehand. The alignment was run over a normalization that aimed to maximize the similarities between both corpora. 
- `emulate-helipad.py`: Bootstrap a heuristic mapping from DDD FORM to HeliPaD FORM (lexical replacement and transliteration rules), for LEMMA (dto), for UPOS and XPOS (majority replacement) from the merged file.
- UDPipe v.1: automated UD parse of HeliPaD-mapped version of DDD Heliand
- `recover-forms-from-helipad.sh`: restore DDD FORM, LEMMA and XPOS in the parsed file, align with HeliPaD/UD and export CoNLL-U

Automated Parsing
==

Performed with UDPipe, using normalization to HeliPaD, 50-dim Word2Vec vectors trained over HeliPaD and normalized DDD-Heliand (full corpus), trained over the *entire* HeliPaD UD corpus. (With two editions of the same text, much of the text is basically duplicated, so we set `-min-count` to `3` rather than defaulting to `2`.)

	$> word2vec -train osx_heliand.all.txt -output models/osx_heliand_all.vec -cbow 0 -size 50 -window 10 -negative 5 -hs 0 -sample 1e-1 -threads 12 -binary 0 -iter 15 -min-count 3
	
	$> word2vec -train osx_heliand.all_lemmas.txt -output models/osx_heliand_all_lemmas.vec -cbow 0 -size 50 -window 10 -negative 5 -hs 0 -sample 1e-1 -threads 12 -binary 0 -iter 15 -min-count 3

	$> cat osx_heliand.pruned.conllu | udpipe --parser "embedding_form_file=models/osx_heliand_all.vec;embedding_lemma_file=models/osx_heliand_all_lemmas.vec" --train models/train.conll.osx_heliand_full.vec.udpipe
	
	$> cat osx_ddd-heliand.pruned.conllu | egrep '^$|^[0-9]' | perl -pe "s/\s*(#.*)?\n/\n/g;" | udpipe --input "conllu" --parse models/train.conll.osx_heliand_full.vec.udpipe  --parser "use_gold_tags=True" > osx_ddd-heliand.pruned.parsed.conllu

Performance:
UDPipe model, trained analoguously on a 80% subset and evaluated against a 10% subset of HeliPaD:
Parsing from gold tokenization with gold tags - forms: 5347, UAS: 87.43%, LAS: 81.20%

Attribution
==

- primary data: Eduard Sievers, Burkhard Taeger (1984), Heliand. Tübingen. 
- digitization: Karin Donhauser,Jost Gippert,Rosemarie Lühr; Deutsch Diachron Digital - Referenzkorpus Altdeutsch Version 1.1; Humboldt-Universität zu Berlin, http://www.deutschdiachrondigital.de/
- syntax: Christian Chiarcos, details tba.

history
==
- 1984 print edition [ST]
- 2014-11-13 DDD edition 0.1, ELAN/ANNIS version with all documents and annotation descriptions [DDD]
- 2017-01-01 DDD edition 1.0, corrected ELAN/ANNIS version of the document. [DDD] Also cf. https://titus.uni-frankfurt.de/lea/Hel_01_Heliand.I.komplett.html [which is probably based on that but covers additional manuscripts].
- 2020-07-21 CoNLL conversion of ELAN version of DDD Heliand, alignment with UD edition of HeliPaD using CoNLL-Merge [CC]
- 2021-05-31 CoNLL-U edition 1.0 [CC]

contributors
==
- ST: Eduard Sievers, Burkhard Taeger (1984), Heliand. Tübingen. 
- DDD: Karin Donhauser,Jost Gippert,Rosemarie Lühr; Deutsch Diachron Digital - Referenzkorpus Altdeutsch Version 1.1; Humboldt-Universität zu Berlin, http://www.deutschdiachrondigital.de/
- CC: Christian Chiarcos, chiarcos@cs.uni-frankfurt.de
