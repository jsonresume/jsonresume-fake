# Almost Real Resume

https://fake.jsonresume.org

Fully generated fake resumes using machine learning models trained off ~6000 JSON resumes.

This repo generates the website, and also includes code for people who would like to see how to train text based models and generate sample outputs.

This is just for a bit of fun, all ideas are welcome (create an issue) and we hope you learn something along the way.

We did not include the real data the models are currently trained off for privacy purposes. Though, thousands of people host their `resume.json` on [Github Gist](https://jsonresume.org/getting-started/) which you can see results for [here](https://gist.github.com/search?l=JSON&o=desc&q=resume.json&s=updated)

Note: The models/output obviously suck. We didn't clean the data enough. And we didn't train them for long enough. (Who can afford that)

## Getting Started

You will need Node and Python3 for this project (sorry)

```
git clone https://github.com/jsonresume/jsonresume-fake
# Install dependencies
npm i
pip3 install -r requirements.txt
```

This entire project largely works off a beautiful Python lib called [textgenrnn](https://github.com/minimaxir/textgenrnn). (Built on top of Keras/Tensorflow). It was created by [Max Woolf](https://github.com/minimaxir/) (thanks and great job man).

## Start the web server

To launch the fake resume viewer;

```
node server.js
```

It should start on [http://localhost:3000](http://localhost:3000)

Refresh the page each time, it will load a new pre-generated resume from the `./resumes` folder.

## Generate Sample Output

Every field in the fake resume is generated, there are 10 models in total.

To generate a sample company name;

```
python3 sample.py
# You should get something like "Javelin Group"
```

We hope that worked, if not, leave an issue.

If you want to try the other models;

```
./models/cities/
./models/company_highlights/
./models/company_names/
./models/company_position/
./models/company_summaries/
./models/interests/
./models/labels/
./models/names/
./models/references/
./models/summaries/
```

You have to edit the `./sample.py` to refect which model you want to run.

Each folder contains;

```
./textgenrnn_config.json
./textgenrnn_vocab.json
./textgenrnn_weights.hdf5
```

Which is the entirety of a trained "model".

## Train your own model

From this repo, you can only train a new `./models/names/` model, the learning set for other models was not included for privacy reasons.

The `textgenrnn` lib expects that you have a single text file that has a new line for every text it should train off e.g.

```
// e.g. names.txt
Thomas Davis
Maximus Kolesnyk
Jimmy Barnes
Beyonce Knowles
```

If you look inside the `./models/names` directory, you can see we have included a file called `names.txt` already based off some random dataset off the internet.

To start generating random names, simply run;

```
cd models/names
python3 train.py
```

You should see some output!

It will suck for some time, much like the samples used in the fake resumes, the longer you train it for the better your results may be. (ML obviously eventually gets a lot more difficult than this)

The script is set to run 10000 epochs (iterations).

There are some caveats with the `train.py` script.

Fortunately, it will save the model if you exit it before finishing the epochs/iterations.

Unfortunately, you can't stop and start the training process in this tutorial.

Everytime you train the model, it will override the original.

Once you've trained for some time, try run again;

```
python3 sample.py
```

If it is still pointing at `./models/names` then it should generate a sample from what your computer had been training.

## Generate fake resumes

Be warned, the script for generating a fake resume is not optimal but it does the job.

It involves loading the 10 models that are pre-trained into a Python script and inserting the sample output into valid places in a JSON Resume. (browse the `./resumes/` folder to see what it outputs)

To generate a fake resume;

```
python3 generate.py
```

There will be some quasi-useful logs and it will also output the results to `./resumes/`.

Type `git status`, if you want to see which new ones you are generating.

## Conclusion

We will make this repo better over time, but as stated at the start, it is just a bit of fun.

Please ask any questions though, basic machine learning stuff is kind of easy, and cool to play with.

There have been some great suggestions as to why a fake resume might be a good thing;

```
- Apply to jobs and see if a recruiter perhaps takes the bait
- HR DDOS (spam a company with fake resumes, where it is hard to tell what is real or fake) (Don't do this)
```

## Contributors

[Thomas Davis](https://registry.jsonresume.org/thomasdavis)
[Max Kolesnyk](https://registry.jsonresume.org/maxkolesnyk)
