# CogLang - Genetic Algorithm

(Skip [here](https://github.com/hchiam/cogLang-geneticAlgo#try-it-out) for how to try it out.)

Use a genetic algorithm to generate words for a "Cognate Language" (a.k.a. "CogLang" for short). The "CogLang" is a language with special properties (details [here](https://github.com/hchiam/cognateLanguage)). The genetic algorithm puts the words in output.txt. Results seem to resemble those generated manually or deterministically (deterministic_output.txt comes from https://github.com/hchiam/cognateLanguage).

## Goals at a Glance:

Generate words:

* with as much "cognacy" as possible with the source words from all 5 source languages (like recognizability -- an emphasis on initial syllables in words should help),

* while allowing for "allophones" (acceptable alternative spellings for flexibility),

* while having the generated words relatively easy to pronounce,

and

* while having words as short as possible.

See the code in [geneticAlgo_just1_v2.py](https://github.com/hchiam/cogLang-geneticAlgo/blob/master/geneticAlgo_just1_v2.py) for details on how the above goals are quantified and combined for overall "fitness" scores.

## Background / Other Related Repos:

https://github.com/hchiam/cognateLanguage

https://github.com/hchiam/cognateLanguage2

https://github.com/hchiam/coglang-translator

## Try it out:

Use the command line interface.

To run an example on just one word:

```
python geneticAlgo_just1_v2.py
```

To run on all the data in data.txt: (This outputs to output.txt and best-scorers.txt)

```
python geneticAlgo.py
```

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

## Lessons Learned:

* Find more efficient data structures and algorithms = faster and less risk of over-heating. Example: hashtable.

* Better-defined fitness evaluators and better generators = better results / more sensible results.

## Stats:

### Scores Using evaluator_old.py:

13185.0 = geneticAlgo_just1_v2.py (first try)

11067.9 = geneticAlgo_just1.py (first try)

9822.4 = deterministic

So:

v2 = 1.2 times better than v1 (not to mention faster)

v1 = 1.1 times better than deterministic

v2 = 1.3 times better than deterministic
