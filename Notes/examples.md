- Case=Bare vs Case=Nom


- Negative problem
- Also confusion with multiple Propers

```
token: yaptırılamıyordu
[start]yap[VERB][Proper=False][Derivation=Cau][Proper=False][Derivation=Pass][Polarity=Pos][Proper=False][Derivation=Nonf][PersonNumber=A3sg][Possessive=P3sg][Case=Loc][Proper=False]
```

```
<Test>
Input token: yazamayacağım
Model output: [start]yazama+VERB+Polarity=Neg+Proper=False+Derivation=FutNom+PersonNumber=A3sg+Possessive=P1sg+Case=Bare+Copula=PresCop+PersonNumber=V1sg+Proper=False[end]
True output: [start]yaz+VERB+Proper=False+Derivation=Able+Polarity=Neg+Proper=False+Derivation=FutNom+PersonNumber=A3sg+Possessive=P1sg+Case=Bare+Proper=False[end]
<\Test>
```


- Context
```
<Test>
Input token: sıralar 
Model token: [start]sıra+NOUN+A3pl+Pnon+Nom+[end] 
True token: [start]sıra+VERB+A3pl+Pnon+Bare+PresCop+V3sg+[end] 
<\Test>
```

```
<Test>Input token: ayda
Model output: ay[NOUN][PersonNumber=A3sg][Possessive=Pnon][Case=Loc][Proper=False]
True output: ay[NOUN][Temporal=True][PersonNumber=A3sg][Possessive=Pnon][Case=Loc][Proper=False]
<\Test>
```

```
<Test>Input token: zevklerinden
Model output: zevk[NOUN][PersonNumber=A3sg][Possessive=P3pl][Case=Abl][Proper=False]
True output: zevk[NOUN][PersonNumber=A3pl][Possessive=P3sg][Case=Abl][Proper=False]
<\Test>
```

```
<Test>
Input token: Bu
Model output: [start]bu+DET+DeterminerType=Dem+Proper=False[end]
True output: [start]bu+PRON+PersonNumber=A3sg+Possessive=Pnon+Case=Nom+Proper=False[end]
<\Test>
```


```
<Test>
Input token: hazırlanan
Model output: [start]hazır+NOUN+PersonNumber=A3sg+Possessive=Pnon+Case=Bare+Proper=False+Derivation=Make+Proper=False+Derivation=Pass+Polarity=Pos+Proper=False+Derivation=PresPart+Possessive=Pnon+Proper=False[end]
True output: [start]hazır+NOUN+PersonNumber=A3sg+Possessive=Pnon+Case=Bare+Proper=False+Derivation=Make+Proper=False+Derivation=Pass+Polarity=Pos+Proper=False+Derivation=PresPart+Possessive=Pnon+Proper=False[end]
<\Test>
```




- Needs a FST layer of underlying representation
- Or 
```
<Test>
Input token: komutan
Model output: komut[VERB][Polarity=Pos][Proper=False][Derivation=Nonf][PersonNumber=A3sg][Possessive=Pnon][Case=Bare][Proper=False]
True output: komutan[NOUN][PersonNumber=A3sg][Possessive=Pnon][Case=Bare][Proper=False]
<\Test>
```