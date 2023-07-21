# Snips NLU

[Snips NLU](https://snips-nlu.readthedocs.io) is a Python library designed for extracting structured information from sentences written in natural language.

## What is Snips NLU about?

At the heart of every chatbot and voice assistant is a shared technology: Natural Language Understanding (NLU). Any time a user interacts with AI via natural language, their expressions must be translated into a format that a machine can understand.

The NLU engine first identifies the user's intent, then extracts the query's parameters, also known as 'slots'. Developers can then use this structured data to determine the appropriate action or response.

Let’s take an example to illustrate this, and consider the following sentence:


    "What will be the weather in paris at 9pm?"

Properly trained, the Snips NLU engine will be able to extract structured data such as:


    {
       "intent": {
          "intentName": "searchWeatherForecast",
          "probability": 0.95
       },
       "slots": [
          {
             "value": "paris",
             "entity": "locality",
             "slotName": "forecast_locality"
          },
          {
             "value": {
                "kind": "InstantTime",
                "value": "2018-02-08 20:00:00 +00:00"
             },
             "entity": "snips/datetime",
             "slotName": "forecast_start_datetime"
          }
       ]
    }

In this case, the identified intent is ``searchWeatherForecast`` and two slots were extracted, a locality and a datetime. As you can see, Snips NLU does an extra step on top of extracting entities: it resolves them. The extracted datetime value has indeed been converted into a handy ISO format.

Check out our `blog post`_ to get more details about why we built Snips NLU and how it works under the hood. We also published a `paper on arxiv`_, presenting the machine learning architecture of the Snips Voice Platform.

Citing Snips NLU
----------------

Please cite the following paper when using Snips NLU:
```bibtex
   @article{coucke2018snips,
     title   = {Snips Voice Platform: an embedded Spoken Language Understanding system for private-by-design voice interfaces},
     author  = {Coucke, Alice and Saade, Alaa and Ball, Adrien and Bluche, Th{\'e}odore and Caulier, Alexandre and Leroy, David and Doumouro, Cl{\'e}ment and Gisselbrecht, Thibault and Caltagirone, Francesco and Lavril, Thibaut and others},
     journal = {arXiv preprint arXiv:1805.10190},
     pages   = {12--16},
     year    = {2018}
   }
```

