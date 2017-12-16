# CogLang - Genetic Algorithm

Use a genetic algorithm to generate words for a "Cognate Language" (a.k.a. "CogLang" for short). The "CogLang" is a language with special properties (details [here](https://github.com/hchiam/cognateLanguage)). The genetic algorithm puts the words in output.txt. Results seem to resemble those generated manually or deterministically (deterministic_output.txt comes from https://github.com/hchiam/cognateLanguage).

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
