# CogLang - Genetic Algorithm

Use a genetic algorithm to generate words for a "Cognate Language" (a.k.a. "CogLang" for short). The "CogLang" is a language with special properties (details [here](https://github.com/hchiam/cognateLanguage)). The genetic algorithm puts the words in output.txt. Results seem to resemble those generated manually or deterministically (deterministic_output.txt comes from https://github.com/hchiam/cognateLanguage).

## Goals at a Glance:

Generate words:
* with as much "cognacy" as possible with the source words from all 5 source languages (like recognizability -- an emphasis on initial syllables in words should help),
* while allowing for "allophones" (acceptable alternative spellings for flexibility),
* while having the generated words relatively easy to pronounce,
and
* while having words as short as possible.

See the code in `geneticAlgo_just1_v2` for details on how the above goals are quantified and combined for overall "fitness" scores.

## Background / Other Related Repos:

https://github.com/hchiam/cognateLanguage

https://github.com/hchiam/cognateLanguage2

https://github.com/hchiam/coglang-translator

## Genetic Algorithm:

To run an example:

```
python geneticAlgo_just1.py
```

To run on all the data in data.txt:

```
python geneticAlgo.py
```

--> This outputs to output.txt and best-scorers.txt

You can compare scores by running this:

```
python evaluator_old.py output.txt
```

or this:

```
python evaluator_old.py deterministic_output.txt
```

or even to compare with a previous run with an older genetic algorithm:

```
python evaluator_old.py previous_output.txt
```
