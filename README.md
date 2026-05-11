# Consolidated Heliand corpus

Building an Old Saxon UD-style dependency corpus by merging three source corpora and their annotations

- Heliand-B4 (morphosyntax, lemmas, shallow syntax, clausal structure)
- Heliand-DDD (morphosyntax, lemmas, clausal structure)
- HeliPaD (morphosyntax, PTB-style syntax)

## Usage and licensing

The Consolidated Old Saxon corpus is released under a CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0), with reference to 

- Christian Chiarcos and Janine Siewert (2026), Consolidating Syntactically Annotated Corpora with LLOD Technology. An Experiment in the Old Saxon Heliand. In Proceedings of the 10th Workshop on Linked Data in Linguistics (LDL-2026), Palma de Mallorca, Spain, May 2026

In addition, it is required to reference the underlying source corpora, i.e.,

- HeliPaD/CHLG corpus (CC BY 4.0, with attribution to Walkden, George. 2015. HeliPaD: the Heliand Parsed Database. Version 0.9. http://www.chlg.ac.uk/helipad/)
- Referenzkorpus Altdeutsch (CC BY-NC-SA 3.0, with attribution to Karin Donhauser, Jost Gippert, Rosemarie Lühr (2018); Deutsch Diachron Digital - Referenzkorpus Altdeutsch Version 1.1; Humboldt-Universität zu Berlin; Homepage: http://www.deutschdiachrondigital.de/ DOI: https://doi.org/10.34644/laudatio-dev-WiWkDnMB7CArCQ9CyBEw)
- Heliand B4 Corpus (CC BY 3.0, with attribution to Svetlana Petrova, Karin Donhauser, Sonja Linde (2015). Heliand (1.0). Humboldt-Universität zu Berlin. Homepage: https://www.sfb632.uni-potsdam.de/aprojekte/b4.html)

## Content and structure

Characteristics of the data: The dependency annotations provided here are not natively manual annotations, but they are transformed from existing manual annotations. As many these annotations (different editions of) the same text, these annotations are consolidated. We track mismatches and use these as an evaluation criterion of the different consolidation techniques. Wherever manual annotations of a text are available, these are given priority.

- [`release/`](release): Corpus releases
- [`src/`](src): Enriched and transformed versions of the source corpora and their annotations
- [`parsing/`](parsing): Some annotations are incomplete, so that we provide a UD parser (UDpipe v.1) that is consulted as a fallback solution.

Accompanying data:

- [ConOS-UD](https://github.com/UniversalDependencies/UD_Old_Saxon-ConOS) manually annotated sub-corpus at Universal Dependencies

## Corpus structure and construction

The corpus builds on existing manual annotations, but these are neither consistent with CoNLL-U (none of these are dependency annotations) nor complete (HeliPaD coverse parse of the [BT] text only, DDD provides morphosyntactic annotations only, B4 provides phrase structure syntax, but only for a small DDD subset).

The folder `src/` contains the source corpora, their revised annotations, and the respective build scripts. These data overlap with respect to which text witness / edition they represent, so that their annotations are to be merged in a subsequent processing step. The merged data is then provided in `release/`.
