# CoNLL conversion of the B4 Heliand corpus

Note that this about 3.000 tokens only, i.e., about 5% of the full corpus, as training data, this is neglectable, but it can be used for testing.

## Content

- `zips/paula_1-0.zip` original source data as provided by [Laudatio][https://www.laudatio-repository.org/browse/corpus/7ySuCXMB7CArCQ9Ccica/corpora)
- `b4-conll/` CoNLL/TSV edition of the original PAULA data
- `conll/` consolidated CoNLL annotation with PTB-style parses
- `conllu/` CoNLL-U edition, based on B4 parses with disambiguation from HeliPaD-UD and DDD-UD

## CoNLL/TSV edition (results in `b4-conll/`)

We provide an opportunistic* converter from Heliand PAULA to CoNLL. Run with 

	$> ./scripts/paula2conll.sh
	
This will create `tmp/paula/b4.heliand/*/*.merged.conll`. The _manually curated_ form of these files resides under `b4_conll/`.
	
Based on the PAULA data model, we generate the following column structure:

0      ID (numerical token identifier)
1      TOKEN (original token identifier)
2      WORD (string value, draw from comment [!] in *.tok.xml)
3      segmentation (with annotation-specific column label)
       annotation-specific segmentation in IOBES format, corresponding to one PAULA *Seg.xml file, e.g., "aboutness" (for *aboutnessSeg.xml)
       note that the labels provided are identifiers (i.e. unique within the column), but not meaningful
4..n   annotation (with annotation-specific column label)
       one or multiple columns with annotations of the segments defined in 3, each corresponding to one PAULA *Seg_*.xml file.
       the annotation is attached to the first element of the corresponding segment.
       column label is a concatenation of segmentation label (see 3) and feature name, e.g., "aboutness:aboutness" (for *aboutnessSeg_aboutness.xml)
n+1    analoguous to 3
n+2..m analoguous to 4
       etc.

The order of columns 3 and following is determined by the lexicographical order of the underlying files.
This structure can be substantially simplified, esp. for annotations for individual tokens, but this needs to be verified by hand.
In particular, the sequence, content, position and existence of columns is defined by the PAULA files provided, and these are not necessarily the same 
across different subcorpora.

* Note that this is specific to this data, no guarantees for functionality on other data sets.
In particular, we rely on resource-specific conventions for file naming, layout, attribute and element order, XML comments (!) and the structure of xpointers.
Further, we only support data structures encountered here, no support for structs or feature groups.
It is expected, however, that this may be applicable to other Exmaralda-based PAULA data provided by HU Berlin or U Potsdam.

## Consolidated CoNLL/TSV edition (results in `conll/`)

Generated from `b4-conll/`, compact aggregation of PAULA data structures into one column per *Seg.xml, conversion to PTB-style syntax annotation. Resulting column structure:

	ID WORD PARSE aboutness alliteration bibl context definiteness bg marker givenness position no comm marker trans

Here, `PARSE` combines the annotations of 8 original B4-CoNLL columns ("cat", "cat:cat", "clause", "clause:status", "gf", "gf:gf", "pos", "pos:pos").
Created using

	$> cat $b4file.conll | python3 scripts/consolidate-b4.py > $outfile.conll
	
## CoNLL-U edition (results in `conllu/`)

Alignment of consolidated CoNLL files with HeliPaD and DDD Heliand in CoNLL-U. Reproduce with

	$> cd scripts/
	$> merge.sh

- Reads PTB-style B4 parses
- B4 has no sentence splitting, hence split sentences at a clause boundary if it coincides *both* with a H and D sentence split.
- Alignment with HeliPaD (H) and DDD (D) (HeliPaD has better annotation quality, DDD is textually closer to this edition)
- `LEMMA` <  H, supplemented by D
- `UPOS` < H, supplemented by D and mapping of B4 POS (note that B4 POS is coarse-grained)
- `XPOS` < concatenation of H POS, D POS and B4 POS
- `FEATS` empty
- `HEAD` extrapolated from B4 parse, with disambiguation from H and D
- `EDGE` where defined by B4, derived from `cat`, `gf` or `pos` labels (no `clause` labels used here); where underspecified in B4, derived from H, if consistent with B4 parse, or D, if consistent with B4 parse
- `DEPS` empty
- `MISC` protocol for the derivation of B4 annotations from B,H and D, resp., its agreement with any of these

Head extrapolation:

- for every word, calculate the number of dependents in D and H annotation
- for every phrase node (B4 `pos`, `cat`, `gf` or `clause`) span, calculate the number of D and H dependents as the maximum number of its descendant words
- for every phrase node, identify the child that contains the syntactic head as `x:HEAD`:
	- mark every dependant as `x:HEAD`
	- if a nif:Word has a H HEAD that has the same parent and is its `x:HEAD`, adopt H HEAD and EDGE and remove it as `x:HEAD`
	- if a nif:Word has a D HEAD that has the same parent and is its `x:HEAD`, adopt D HEAD and EDGE and remove it as `x:HEAD`
	- if a phrase has multiple `x:HEAD` elements, keep the first
- for every nif:Word that does not have a HEAD and that is not an `x:HEAD`: attach it to the head word (`x:HEAD*`) of its parent node (`B`)
	- if HEAD = D HEAD, adopt D EDGE as label, otherwise,
	- if HEAD = H HEAD, adopt H EDGE as label,
	- otherwise mark as `dep` (`B*`)
- for every branching phrase node n; for every non-`x:HEAD` child c
	- attach the head word of c (`x:HEAD*`) to the head word of n (`B`)
	- extrapolate a UD label from the annotation of n (`BL`)
- for every root node that carries a D HEAD annotation, adopt its HEAD and EDGE
- for every root node that carries a H HEAD annotation, adopt its HEAD and EDGE
- rule-based treatment of punctuation (`p`) and root (`r`)

The codes `HL` and `DL` apply if the resulting EDGE matches H, resp., D (regardless of method of derivation). Likewise the codes `H` and `D` are used for HEAD annotations (regardless of method of derivation).

Unlabelled dependencies:

- 67% (1810/2705) of unlabelled dependencies are directly derived from B4 parses 
- 13% (343/2705) of unlabelled depenencies are rule-based for punctuation and roots
- 20% (the remainder) are derived from H or D
- 57% (1543/2705) of unlabelled dependencies conform to projected H parses; without gaps in the alignment this is 65% (1543/2384)
- 70% (1880/2705) of unlabelled dependencies conform to projected D parses; without gaps in the alignment this is 78% (1880/2409)

Note that the text of B4 Heliand is closer to DDD Heliand than to HeliPaD. This is partially reflected only by the alignment scores:
- 88% (2384/2705) of tokens could be aligned* with HeliPaD
- 89% (2409/2705) could be aligned with DDD

* Note that we ran Levenshtein alignment (after Myer's diff, align to the Levenshtein-closest elements to a span delimited by two aligned words). 
So, any pair of words between two alignment pairs will be merged regardless of their similarity.

Labelled dependencies:

- 58% (1570/2705) of labelled dependencies are directly derived from B4 annotations
- 13% (343/2705) of labelled depenencies are rule-based for punctuation and roots
- 29% (the remainder) are derived from H or D
- 69% (1874/2705) of dependency labels conform to projected H parses (regardless of attachment); without gaps in the alignment, this is 79% (1874/2384)
- 63% (1704/2705) of dependency labels conform to projected D parses (regardless of attachment); without gaps in the alignment, this is 70% (1704/2409)

Overall, we have an agreement of up to 80% for labels (H-B) and dependencies (D-B) among the alignable parts of the three corpora.

Note that these deviations do not necessarily reflect errors (in any of the schemes), but go largely back to conceptual differences (mostly, the degree of underspecification) in the different corpora:

- B4 did not define clausal juncture and did not support the annotation of recursive elements; `cat`, `pos` and `gf` labels and their limited degree of nesting does not perfectly map to UD dependencies.
- DDD did *only* define clausal juncture (in an underspecified way), so its annotations of subclausal units and attachment are derived from a HeliPaD parser and backed up by HeliPaD projection.
- HeliPaD was originally annotated in a variant of the PTB schema, with a custom mapping to UD. The mapping is heuristic, in that information implicitly encoded in the ordering was used to bootstrap head informations, 
and that the annotation used a considerable amount of empty elements which could not be directly operationalized.

Note that the DDD clause annotations had not been integrated in the version of the DDD Heliand used here.

For different levels of annotation, different corpora provide better data:
- `WORD`: Prefer DDD, because it preserves/restores accents and provides normalized orthography. Also note that the DDD text is more complete (it is based on a philological edition), whereas HeliPaD is based on a single manuscript.
- `LEMMA`: Prefer HeliPaD, because DDD lemmatizes against Old High German rather than Old Saxon. 
- `UPOS`: DDD and HeliPaD are comparable, B4 lacks certain distinctions (SCONJ, CCONJ)
- `XPOS`: Prefer HeliPaD, because HeliPaD-style XPOS has been included in both DDD and B4 editions
- `HEAD`: Prefer HeliPaD (because this comes from an internally consistent annotation) over B4 (because this comes from a partial annotation) over DDD (because only clause linking was manually annotated, everything else was projected from HeliPaD or automatically annotated)
- `EDGE`: For clausal dependencies, prefer DDD, because these have been explicitly annotated in an easily mappable form. Otherwise, prefer HeliPaD, because these come from a consistent annotation.

## Attribution

Source data under

CC BY 3.0
Svetlana Petrova, Karin Donhauser, Sonja Linde; Heliand; Humboldt-Universität zu Berlin
https://www.sfb632.uni-potsdam.de/aprojekte/b4.html.

Attribution for CoNLL editions to be provided.

## History

- 1935 print edition (PAULA edition comes without metadata, but the source is *very likely* Eduard Sievers: Heliand. Titelauflage vermehrt um das Prager Fragment und die Vatikanischen Fragmente. Halle 1935(1878))
- 2015 PAULA edition [B4]
- 2020-07-21 CoNLL (`b4-conll`) edition [CC]
- 2021-06-07 consolidated CoNLL edition [CC]
- 2021-06-08 CoNLL-U edition [CC]


## Contributors

- B4 - Svetlana Petrova, Karin Donhauser, Sonja Linde, https://www.sfb632.uni-potsdam.de/aprojekte/b4.html
- CC - chiarcos@cs.uni-frankfurt.de