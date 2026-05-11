# Heliand-BT, CoNLL-U edition

- based on the synoptic edition by Behaghel/Taeger 1984, DDD edition
- annotations:
	- tokenization according to DDD Heliand
	- morphosyntactic annotations according to DDD Heliand
	- lemmatization according to DDD Heliand
	- syntax according to B4 Heliand (where available) and DDD Heliand (otherwise)
	- both B4 and DDD UD syntax are derived by complementing DDD and B4 syntax with projected *and* automated HeliPaD UD parses
- automated merging:
	
	$> scripts/build.sh
	
- the MISC column contains provenance information:

	`B4` B4 overrides DDD annotations (and deviated from it), these are 13% of B4 annotations (345/2705)
	`B4=DDD` B4 agrees with DDD annotatons (and overrides it), these are 20% of B4 annotations (535/2705)
	`cycle>DDD` mixed B4 and DDD annotations constitute a cycle, resort to DDD annotations to break it, these are 1% (24/2705) of B4 annotations
	`DDD`,`_` no B4 annotation or alignment mismatch in *initial* alignment with B4, the latter pertains to 66% (1790/2705) of B4 annotations
	`DDD(r)` alignment error between DDD and the result of CoNLL-Merge, annotation follows DDD, for the B4-aligned subcorpus, this applies to 0.4% (11/2705) of B4 lines
	
	The low alignment rate may be due to the gaps in the B4 Heliand that does not provide the full text of each fit.

- procedure:
	- CoNLL-Merge (scripts/align.py): append B4 Heliand to DDD Heliand annotations
	- CoNLL-RDF (derive parse tree from B4+DDD)
	- validation (CoNLL-Merge of the result with DDD Heliand to overcome certain aggregation errors
	
For validation, the automated merge is aligned with the DDD Heliand. Where these deviated from the result of the automated merging, DDD overwrites the merged DDD+B4 Heliand. The output may still contain inconsistencies as syntax is (mostly) based on the HeliPaD corpus (unless superseded by the partial annotations provided by DDD or B4), whereas morphosyntax is (mostly) based on DDD.

Effectively, the resulting parse is 99% (54735/55080) identical with DDD (because of the limited size of B4 Heliand, because of using DDD as fallback where alignment fails and because DDD parses are mostly confirmed by B4). This does not mean that they are error-free, because the B4 UD annotation is partially derived from DDD.