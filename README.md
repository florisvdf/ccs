# CCS - Chinese Comprehension Scoring

Users can score their own reading comprehension based on their vocabulary against a 
media source for both words or for characters. Additionally, users can obtain a 
vocabulary list of words/characters based on a media source and a desired comprehension 
score. 

If you don't have a file of your current vocabulary stored anywhere, but you know your 
reading ability in terms of HSK levels (new or old), you can instead choose to score the 
media source for various levels of HSK. This will output a text file that stores a 
comprehension score for each HSK level, both new and old.

In addition, you may be interested in knowing which words to prioritize in order to 
read your book at a certain level of reading comprehension. `ccs` can generate a word
or character vocabulary to learn in order to reach that score.

# Installation


# The comprehension score

The comprehension score is simply the frequency of your vocabulary in a media source as 
a percentage.

# Usage

## comprehension_report
comprehension_report.py
Vocabulary options. --hsk flag or provide path
-- words
-- characters

Returns:
- A comprehension score for each vocabulary passed
- A plot displaying the number of words/characters to learn to reach remaining 
comprehension scores for each vocabulary passed

## generate_vocab
-- words
-- characters

If you don't have a vocabulary file, you can simply download one of the hsk vocabularies
and provide the path to that file.
