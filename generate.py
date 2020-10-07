from textgenrnn import textgenrnn
import json
from slugify import slugify
from gingerit.gingerit import GingerIt
import string
from lib.sentence_fixer import sentence_fixer

# This file will start outputting resumes to ./resumes/ once generated
# It adds better grammar using Ginger -> https://www.gingersoftware.com/


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'

# Load models
summariesTextgen = textgenrnn(weights_path='./models/summaries/textgenrnn_weights.hdf5',
                       vocab_path='./models/summaries/textgenrnn_vocab.json',
                       config_path='./models/summaries/textgenrnn_config.json')

labelsTextgen = textgenrnn(weights_path='./models/labels/textgenrnn_weights.hdf5',
                       vocab_path='./models/labels/textgenrnn_vocab.json',
                       config_path='./models/labels/textgenrnn_config.json')


namesTextgen = textgenrnn(weights_path='./models/names/textgenrnn_weights.hdf5',
                       vocab_path='./models/names/textgenrnn_vocab.json',
                       config_path='./models/names/textgenrnn_config.json')


referencesTextgen = textgenrnn(weights_path='./models/references/textgenrnn_weights.hdf5',
                       vocab_path='./models/references/textgenrnn_vocab.json',
                       config_path='./models/references/textgenrnn_config.json')

citiesTextgen = textgenrnn(weights_path='./models/cities/textgenrnn_weights.hdf5',
                       vocab_path='./models/cities/textgenrnn_vocab.json',
                       config_path='./models/cities/textgenrnn_config.json')


interestsTextgen = textgenrnn(weights_path='./models/interests/textgenrnn_weights.hdf5',
                       vocab_path='./models/interests/textgenrnn_vocab.json',
                       config_path='./models/interests/textgenrnn_config.json')

companyNamesTextgen = textgenrnn(weights_path='./models/company_names/textgenrnn_weights.hdf5',
                       vocab_path='./models/company_names/textgenrnn_vocab.json',
                       config_path='./models/company_names/textgenrnn_config.json')

companySummariesTextgen = textgenrnn(weights_path='./models/company_summaries/textgenrnn_weights.hdf5',
                       vocab_path='./models/company_summaries/textgenrnn_vocab.json',
                       config_path='./models/company_summaries/textgenrnn_config.json')

companyHighlightsTextgen = textgenrnn(weights_path='./models/company_highlights/textgenrnn_weights.hdf5',
                       vocab_path='./models/company_highlights/textgenrnn_vocab.json',
                       config_path='./models/company_highlights/textgenrnn_config.json')

companyPositionsTextgen = textgenrnn(weights_path='./models/company_position/textgenrnn_weights.hdf5',
                       vocab_path='./models/company_position/textgenrnn_vocab.json',
                       config_path='./models/company_position/textgenrnn_config.json')


# Load in the template of which we will replace values with our ML generated output
with open('resume.json', 'r+') as f:
    # Parse file into a Hash
    data = json.load(f)
    # Let's generate 100 fake resumes before this script finishes
    for lp in range(100):

        print('\n\n\n')
        print(bcolors.HEADER + "=== GENERATING A FAKE RESUME ===" + bcolors.ENDC)
        print('\n')


        # Save name to resume
        print(bcolors.OKBLUE + "== Generating Fake Name (and email)" + bcolors.ENDC)
        names = namesTextgen.generate(n=1, temperature=1, return_as_list=True)
        name = string.capwords(names[0])
        firstName = name.partition(' ')[0]
        nameSlug = slugify(name)
        # Replace Email with slug
        email = nameSlug + '@gmail.com'
        # Save to resume object
        data['basics']['name'] = name
        data['basics']['email'] = email

        print("Name:", name)
        print("Email:", email)
        print('\n')



        # Save label to resume
        print(bcolors.OKBLUE + "Generating Fake Label/Role" + bcolors.ENDC)
        labels = labelsTextgen.generate(n=1, temperature=0.5, return_as_list=True)
        label = string.capwords(labels[0])
        data['basics']['label'] = label
        print("Label:", label)
        print('\n')

        # Save city to resume
        print(bcolors.OKBLUE + "Generating Fake City" + bcolors.ENDC)
        cities = citiesTextgen.generate(n=1, temperature=0.6, return_as_list=True)
        city = cities[0]
        city = string.capwords(city)
        location = city
        data['basics']['location']['city'] = city
        print("City:", city)
        print('\n')


        # Save summary to resume
        print(bcolors.OKBLUE + "Generating Fake Summary" + bcolors.ENDC)
        summaries = summariesTextgen.generate(n=1, temperature=0.3, return_as_list=True)
        summary = summaries[0]
        summary = sentence_fixer(summary, {"name": firstName}, True)
        data['basics']['summary'] = summary
        print("Summary:", summary)
        print('\n')

        # Save interests to resume
        print(bcolors.OKBLUE + "Generating Fake Interests[]" + bcolors.ENDC)
        interests = interestsTextgen.generate(n=3, temperature=1, return_as_list=True)
        for index in range(len(interests)):
            interest = interests[index]
            interests[index] = string.capwords(interest)
            data['interests'][index]['name'] = interests[index]

        print("Interests:", interests)
        print('\n')

        # Save fake company to resume
        print(bcolors.OKBLUE + "Generating Fake CompanyName" + bcolors.ENDC)
        companyNames = companyNamesTextgen.generate(n=3, temperature=1, return_as_list=True)
        companySummaries = companySummariesTextgen.generate(n=3, temperature=0.4, return_as_list=True)
        companyPositions = companyPositionsTextgen.generate(n=3, temperature=0.4, return_as_list=True)

        for i in range(0, 3):
            companyName = string.capwords(companyNames[i])
            companyPosition = string.capwords(companyPositions[i])
            companySummary = companySummaries[i]
            companySummary = sentence_fixer(companySummary, {"name": firstName, "company": companyNames[i], "location": location}, True)
            companyWebsite = "http://" + slugify(companyName) + ".com"
            data['work'][i]['company'] = companyName
            data['work'][i]['summary'] = companySummary
            data['work'][i]['website'] = companyWebsite
            data['work'][i]['position'] = companyPosition
            print("CompanyName:", companyName)
            print("CompanyWebsite:", companyWebsite)
            print("CompanySummary:", companySummary)
            print("CompanyPosition:", companyPosition)
            print('\n')



            print(bcolors.OKBLUE + "Generating Fake Company Hightlights" + bcolors.ENDC)
            highlights = companyHighlightsTextgen.generate(n=2, temperature=1, return_as_list=True)
            print("Highlights: ", highlights)
            for ia in range(0, 2):
                highlight = highlights[ia]
                highlight = sentence_fixer(highlight, {"name": firstName}, True)
                data['work'][i]['highlights'][ia] = highlight


        # Save fake reference to resume
        print("Generating Fake References")
        print(bcolors.OKBLUE + "Generating Fake Referenes" + bcolors.ENDC)
        references = referencesTextgen.generate(n=2, temperature=0.7, return_as_list=True)

        refererNames = namesTextgen.generate(n=2, temperature=0.6, return_as_list=True)
        for i in range(0, 2):
            referer = refererNames[i]
            reference = references[i]
            reference = sentence_fixer(reference, {"name": firstName, "company": companyNames[i], "location": location}, True)
            data['references'][i]['reference'] = reference
            data['references'][i]['name'] = string.capwords(referer)
            print("Reference done:", referer, reference)

        with open('./resumes/' + nameSlug + '.json', 'w') as fa:
            json.dump(data, fa, indent=4)
            fa.truncate
