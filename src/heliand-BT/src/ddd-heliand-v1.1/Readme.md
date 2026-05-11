# Heliand, DDD v1.1, UD edition

- CoNLL-U edition
- source data from https://www.deutschdiachrondigital.de/, CC-BY-NC 3.0
- The original data contained lemmatization, parts of speech, morphosyntactic features and information on clause linking (but no systematic parses) in ELAN format.
- CoNLL conversion using the ELAN2CoNLL converter from https://github.com/acoli-repo/conll-merge/tree/master/cmd/elan2conll
- XPOS: Based on a mapping of DDD annotations to HeliPaD parts of speech, developed with CoNLL-Merge by CC.
- UPOS: Based on a mapping of DDD annotations to an earlier UD interpretation of HeliPaD parts of speech, developed by CC.
- HEAD/DEP: automatically created using a parser trained on an UD interpretation of HeliPaD created by CC

Data
==

- `ddd-heliand.parsed.conllu` CoNLL-U excerpt from the full parse, with merging protocol in MISC:
	
	- `H` projected from HeliPaD, preferred if HeliPaD alignment covers >80% of the tokens in the sentence
	- `P->H` use automatic parse to _complement_ projected parse, only if HeliPaD alignment covers >80% of the tokens in the sentence; entails `P=H`
	- `P` automatically parsed (no alignment with HeliPaD found or coverage of HeliPaD alignment <= 80% [otherwise, that would be `P->H`>])
	- `P=H` projected and parsed are identical
	
	- `HD` projected dependency label, preferred if head is identical with `H` HEAD
	- `PD` automatically parsed dependency label, used if head is different from `H` HEAD or no `H` head is defined
	- `PD=HD` automatically parsed dependency = projected HeliPad dependency
	- `CEDGE>EDGE` override `HD` or `PD` dependency label with a UD dependency label based on DDD clause annotation (hence `CEDGE`) as given in parentheses
		
	- `dedup_head` heuristic head deduplication	
	- `a->P,PD` alignment between original+annotated+aligned data and the initial CoNLL-U data generated from it failed, these lines are restored from the automated parse
	
- alignment errors (`a->P`): 8% (4406/55080 tokens); on the remainder:
	- projected dependencies (`H`): 72% (36416/50674 tokens), out of these 82% (30042/36416) are identical to automatically parsed (`P`)
	- automatically parsed dependencies (`P`, but not `P=H`):  29% (14484/50674 tokens)
	- DDD-based dependency labels (`CEDGE`): 4% (1976/50674 tokens), out of these, 31% (608/1976) are identical with `P`/`H` labels. Frequent replacements:
		
		- 17% 330 `acl` (H) > `ccomp` (D)
		- 11% 221 `acl` (H) > `acl:relcl` (D) [this is not an error, but a difference in granularity]
		- 10% 204 `advlcl` (H) > `ccomp` (D) [this is a difference in semantic interpretation rather than in syntax]
		- 9% 181 `acl` (H) > `advcl` (D)
		
		Overall, this may reflect a difference in perspective: Whereas HeliPaD clause annotation seems to be defined by the structure of the dependent, DDD clause annotation seems to be defined by (its relation with) the head.
	
	- for the remainder
		- projected labels (`HD`): 74% (35855), out of these, 86% (30809/35855) are identical to automatically parsed (`PD`)
		- automated labels (neither `CEDGE` nor `HD`): 36% (12843)
	
- For intermediate steps and detailed minutes, see `versions/`
- `versions/ddd-heliand.parsed.full.conll` automated parse with DDD forms and annotations restored and manual HeliPaD/UD annotations aligned [*this file contains the full data*]

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
