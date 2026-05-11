# Parsing

We provide an Old Saxon baseline parser trained on (a CoNLL-U edition of) HeliPaD to facilitate annotation integration. Its (sole) purpose is to fill in gaps in the annotation that result from errors in annotation projection from HeliPad or gaps in the HeliPad source data.

For the majority of Old Saxon corpus data, we have manual annotations, but 
- only one source annotation provides complete parses (HeliPaD)
- other annotated corpora provide partial annotations only (B4, DDD)
- only one annotation covers the full text (DDD)
- they go back to different editions and manuscript witnesses (of the same source), so that there may be omissions or deviations in the text

We ground our Heliand annotation in (a conversion of) HeliPaD, but align it with the other Heliand annotations to derive a richer (and more robust) annotation. 
We provide a consolidated annotation for all main versions of the Heliand text (M, C, BT).

C: Direct conversion from HeliPad.
BT: Annotation projection from HeliPad plus subsequent refinement with DDD and B4 annotations. Where HeliPad projection is not available (C is a subset of BT), we resort to the *HeliPad-style parser*, instead.
M: Annotation projection from BT. No manual annotations available, but M is a subset of BT.