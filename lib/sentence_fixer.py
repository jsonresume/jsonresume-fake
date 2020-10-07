from gingerit.gingerit import GingerIt
from transformers import pipeline
import re

## This file just wants to try make the grammar better.
## Very UGLY code be warned

## Initialize Ginger API
parser = GingerIt()

## Intialize BERT Pronoun Entity Recognition
nlp = pipeline("ner")

name = "Thomas"
location = "Melbourne"
company = "Listium"





class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'
    

def sentence_fixer(sequence, pronoun_replacements, use_ginger=True):
    print('\n\n')
    print(bcolors.OKBLUE + " > Sentence Fixer: Trying to improve:" + bcolors.ENDC)
    print("   " + sequence)
    if use_ginger:
        print(bcolors.OKBLUE + "   Querying the Ginger API to fix original sentence" + bcolors.ENDC)
        try:
            sequence = parser.parse(sequence)
            sequence = sequence['result']
        except:
            print(bcolors.WARNING + "   Ginger API couldn't parse this sentence" + bcolors.ENDC)
    nlpReplacements = nlp(sequence)
    for i in nlpReplacements:
        originalWord = i['word']
        if len(originalWord) < 3:
            continue
        print("   BERT NER", i)
        originalWorldRe = ""

        ## If BERT NER returned a fuzzy match make a regex string
        if "##" in originalWord:
            originalWorldRe = originalWord.replace("##", ' \S*') + ' '

        if "name" in pronoun_replacements and i['score'] > 0.7 and i['entity'] == 'I-PER':
            name = pronoun_replacements["name"]
            print("   We should replace with", name)
            if originalWorldRe != "":
                p = re.compile(originalWorldRe)
                matches = p.findall(sequence)
                print("what are the matches")
                print(matches)
                if matches and matches[0] and len(matches[0]) > 3:
                    sequence = sequence.replace(matches[0], ' ' + name + ' ')
                    sequence = sequence.replace(matches[0].lower(), ' ' + name + ' ')
            else:
                sequence = sequence.replace(' ' + originalWord + ' ', ' ' + name + ' ')
                sequence = sequence.replace(' ' + originalWord.lower() + ' ', ' ' + name + ' ')
                sequence = sequence.replace(originalWord + ' ', name + ' ')
                sequence = sequence.replace(originalWord.lower() + ' ', name + ' ')

        if "location" in pronoun_replacements and i['score'] > 0.7 and i['entity'] == 'I-LOC':
            location = pronoun_replacements["location"]
            if originalWorldRe != "":
                print("trying a regex replace for", originalWorldRe)
                p = re.compile(originalWorldRe)
                matches = p.findall(sequence)
                if matches and matches[0] and len(matches[0]) > 3:
                    sequence = sequence.replace(matches[0], ' ' + location + ' ')
                    sequence = sequence.replace(matches[0].lower(), ' ' + location + ' ')
            else:
                sequence = sequence.replace(originalWord, location)
                sequence = sequence.replace(originalWord.lower(), location)
        if "company" in pronoun_replacements  and i['score'] > 0.7 and i['entity'] == 'I-ORG':
            company = pronoun_replacements["company"]
            if originalWorldRe != "":
                print("   trying a regex replace for", originalWorldRe)
                p = re.compile(originalWorldRe)
                matches = p.findall(sequence)
                if matches and matches[0]  and len(matches[0]) > 3:
                    sequence = sequence.replace(matches[0], ' ' + company + ' ')
                    sequence = sequence.replace(matches[0].lower(), ' ' + company + ' ')
            else:
                sequence = sequence.replace(originalWord, company)
                sequence = sequence.replace(originalWord.lower(), company)

    print(bcolors.OKBLUE + "   Sentence Fixer: the 'improvement':" + bcolors.ENDC)
    print("   " + sequence)
    print('\n\n')
    return sequence
