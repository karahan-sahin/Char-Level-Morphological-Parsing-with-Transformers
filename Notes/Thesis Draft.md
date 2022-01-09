# Character-level Morphological Analysis in Turkish with Transformers

## Abstract

In this paper,

## 1. Introduction

In the 



## 2. Related Works

In 

### 2.1 Early Works

### 2.2 Neural Morphological Analysis

### 2.3 Contextual Information



## 3. Data

The data used in this study is syntactic parsing dependency parsing annotations from *A Gold Standard Dependency Treebank for Turkish* (Kayadelen et.al. 2020). The data is in original format of Universal Dependencies treebank annotation format, CoNLL-U format. The CoNLL-U  format of a token with multiple morphology, the token *açıklanmayan*, is represented as in example below. There are multiple Universal Dependencies treebanks introduced for Turkish as UD-Boun, IMST-UD, ...

There are multiple reasons why choose this treebank the instead of other dependency annotation treebanks. The main reason why we choose, is the order of morphological feature annotations. In Universal Dependencies framework, the features are ordered in alphabetical order where 

```
1	Açık	açık	NOUN	NN	PersonNumber=A3sg|Possessive=Pnon|Case=Bare|Proper=False	2	ig	_	SpaceAfter=No
2	la	_	VERB	VB	Derivation=Make|Proper=False	3	ig	_	SpaceAfter=No
3	nma	_	VERB	VB	Derivation=Pass|Polarity=Neg|Proper=False	4	ig	_	SpaceAfter=No
4	yan	_	ADJ	VJ	Derivation=PresPart|Possessive=Pnon|Proper=False	5	rcmod	_	_
```



The token count and sentence for the treebank is given below. We converted the dependency annotations of each token into morphological parse output as concatenating the lemmatized token, part-of-speech tag, and  morphological features `lemma+Part-of-Speech+Feature1+..+FeatureN` which also aligns with the standardized format introduced by Oflazer (?).  


| Data          | Count |
| ------------- | ----- |
| Wiki Token    | 39932 |
| Web Token     | 26508 |
| Wiki Sentence | 2310  |
| Web Sentence  | 2541  |



#### Data Processing

- Random distribution controlled by feature rep.
- **Phonological Normalization**

#### Phonological Normalization

- Mostly done however cannot decide on the lemma alternation
  - kitap -> kitab-ı??
- lemma[-1] `d->t ,ğ->k, `
- Rfx passfix

## Feature Reduction and Overall Morphological Representations

> Main reason why I do this is to capture **overt morphology** which more features can create **a noise to the model**







- I have turned semantic features into different POS tags 

  - ADP+ComplementType=? -> ADP^ComplementType
    - This token is due to the previous tokens Case, there should be a separate token
  - PRON+PronType=? -> PRON^PronType
  - ConjunctionType
    - `re.sub("CONJ\+ConjunctionType=","",decode)`

- Multiple Polarity around Derivation=Able as

  - ```
    atabiliyor:	at+VERB+*Polarity=Pos*+Derivation=Able+Polarity=Pos+TenseAspectMood=Prog1+Copula=PresCop+PersonNumber=V3sg
    to
    at+VERB+Derivation=Able+Polarity=Pos+TenseAspectMood=Prog1+Copula=PresCop+PersonNumber=V3sg
    ```

  - Capabiility vs possibility --> subsampling

    - Scope general --> disambiguation
    - Modality disambiguatior (Case Study)

  - To further demonstrate overt morphology

- Should extra feature further eliminated

  - Case=Bare before the derivation the derivation

- > 

- Proper=True+ ..
  - Proper=True within the morphology
  - Ali - siz
  - `re.sub("Proper=True+", "", decode)`
  
- Case=Bare within the morphology
  - While `Case=Loc` can be within the lemma
  - `Case=(?<!Bare)+?\+(?<!Proper=True)`
    - Talk these cases
    - kitap(Case=Nom) - tır
    - 
  - Bare case has no overt usE
  
- `Possessive=Pnon` also null 

  - **Generally null features are redundant**
  - This is a one way of

- A3sg vs V3pl

- `üyelArIYdI	üye+VERB+PersonNumber=A3pl+Possessive=P3sg+Case=Bare+Copula=PastCop+PersonNumber=V3pl`
  
  - POS!!!! --> lemma pos or token pos
  - PersonNumber --> Nominal pred
    - üye**leri**ydi **V3pl is null**
    - *güzeller-di-ler
    - kitaplar-dır vs kitaplarım-dı vs *kitaplarım-dır 
    - also an error
    - Also nullness hypothesis

#### Data Augmentation

- Upsampling with respect to Noun Verb Distribution

  - Improved accuracy

- Tried distribution of each morphology with the pseudo-code

- ````pseudocode
  for feature -> sorted(morphology_feature):	
  ````



## Model

- Original transformer in the paper
- Computational complexity
- Parameters
- Show architecture

| Parameter                   | Value                          |
| --------------------------- | ------------------------------ |
| Vocab Size                  | **322 (Dataset char + feats)** |
| Sequence Length             | 20                             |
| Embedding Dimensions        | 256                            |
| Latent Dimensions           | 2048                           |
| Number of (Attention) Heads | 8                              |
| Batch Size                  | 64                             |
| Epoch                       | 5                              |



### Results

- Partial Match: Calculates in terms of subset of common features

$$
Precision = \frac{S_{gold} \cap S_{model}}{S_{gold}}\\
Recall = \frac{S_{gold} \cap S_{model}}{S_{model}}
$$

- Exact Match: Literal string Match of sequences
  - 
  - 0.1 ~ 0.2
- BLEU Score: Feature-wise edit distance between y_pred and y_true
- Further Analysis
  - edit_distance(lemma_pred vs lemma_true)
  - precision, recall of POS tagging



|                                | Partial-Precision | Par-Rec   | BLEU  | POS  | Lemma |
| ------------------------------ | ----------------- | --------- | ----- | ---- | ----- |
| Baseline (Random - Token)      | 0.763             | 0.774     | 0.77  |      |       |
| Feature Distribution           | 0.35              | 0.35      |       |      |       |
| Random Dist with Normalization | **0.825**         | **0.805** | 0.827 |      | 0.955 |
| Feat Dist with Normalization   | 0.645             | 0.645     | 0.62  | 0.32 |       |
| **Upsampling**                 | 0.757             | 0.743     | 0.808 | 0.82 |       |

## Future Works

- Context Embeddings
- Try it with other treebanks
- FST for Normalization
- Compare with Other Models
- Faster Transformer
- Better Evaluation

## References

MA

Oflazer, K. (1994). Two-level description of Turkish morphology. *Literary and linguistic computing*, *9*(2), 137-148.

Sak, H., Güngör, T., & Saraçlar, M. (2011). Resources for Turkish morphological processing. *Language resources and evaluation*, *45*(2), 249-261.

Güngördü, Z., & Oflazer, K. (1995). Parsing Turkish using the lexical functional grammar formalism. *Machine Translation*, *10*(4), 293-319.

Sak, H., Güngör, T., & Saraçlar, M. (2008, August). Turkish language resources: Morphological parser, morphological disambiguator and web corpus. In *International Conference on Natural Language Processing* (pp. 417-427). Springer, Berlin, Heidelberg.



Neural

Akyürek, E., Dayanık, E., & Yuret, D. (2019). Morphological analysis using a sequence decoder. *Transactions of the Association for Computational Linguistics*, *7*, 567-579.



Model

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. In *Advances in neural information processing systems* (pp. 5998-6008).





Data References

Kayadelen, T., Öztürel, A., & Bohnet, B. (2020, May). A Gold Standard Dependency Treebank for Turkish. In *Proceedings of the 12th Language Resources and Evaluation Conference* (pp. 5156-5163).

Nivre, J., De Marneffe, M. C., Ginter, F., Goldberg, Y., Hajic, J., Manning, C. D., ... & Zeman, D. (2016, May). Universal dependencies v1: A multilingual treebank collection. In *Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC'16)* (pp. 1659-1666).
