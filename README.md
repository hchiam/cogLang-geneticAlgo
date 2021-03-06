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

According to the deterministic/manual method's own rough evaluator:

output.txt
13476.4 = rough overall score

deterministic_output.txt
12201.3 = rough overall score

So:

Using the genetic algorithm is **1.105 times** as good as doing it deterministically/manually, or about **11 %** better, even if you use the deterministic method's own rough evaluator.
