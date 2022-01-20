<<<<<<< HEAD
# NER model

We made a custom Named Entity recognition model that is able to recognize [products](https://github.com/benoitmargx/Project_06-Algorythm/blob/sebastian/scrapped_oil_products.json) and [oil companies](https://companiesmarketcap.com/oil-gas/largest-oil-and-gas-companies-by-market-cap/).

To create this model, we made a pipeline:
 
The first element of the pipeline is used to scrape the 220 biggest oil [companies](https://companiesmarketcap.com/oil-gas/largest-oil-and-gas-companies-by-market-cap/) in the world, it also scraped 150+ [products]('https://innovativewealth.com/inflation-monitor/what-products-made-from-petroleum-outside-of-gasoline') made with oil/petrolium. This is placed in a Class that's going to save the data in a json-formated file.

The second element of the pipeline in going to generate sentences to feed the model. This step is achieved by getting the raw data from the given dataset. We focused on the categories: crude, castor-oil, gas, fuel, nat-gas, oil. We also made a `class` that generated extra data by scrapping a [wikipedia](https://en.wikipedia.org/wiki/List_of_largest_oil_and_gas_companies_by_revenue) page and saving it as [json](https://github.com/benoitmargx/Project_06-Algorythm/blob/sebastian/wiki_data.json) file. We were able to generate 1 000 000+ sentences to feed the model.
This part of the pipeline took in the raw data cleaned it, searched for the sentences with the companies and products that we targeted.
In this `class` we have a `clean` method that was copied out of this [code](https://github.com/blueprints-for-text-analytics-python/blueprints-text/blob/master/ch12/Knowledge_Graph.ipynb).

Now that we've the training data, in the form of sentences, we created a `class` to train the model.
All of this is managed in the `main` method where the pipeline is created, the final result is a trained spacy [model](https://github.com/benoitmargx/Project_06-Algorythm/tree/sebastian/custom_nlp) that's saved and ready to be used.

## Limitation

we failed to test our model due time shortage. 
We also got a last minute parsing error generating the trainig sentences to feed the model.

## Usage

To use the pretrained model, you need to download the custom ner [directory](https://github.com/benoitmargx/Project_06-Algorythm/tree/sebastian/custom_nlp) to your working directory. In your python file you `import spacy`(see `requirements.txt`), then you load the nlp trained model: `spacy.load('custom_nlp')` and now have fun.
=======
# Analyzing the relationships between entities in text using NLP and knowledge graphs

![knowledge_graph](knowledge_graph1.png)

## Project description

The project is aimed at implementing available NLP libraries to find out relationships between entities in a text document and to visualize the relationships using Knowledge graphs. Nodes represent entities such as persons, places, events, or companies, and edges represent formalized relations between those nodes. For this project, the publicly available Reuters dataset from the NLTK library, specifically the catagory `Crude`was used. 


## Mission objectives

The objectives are consolidate the knowlege in NLP, specifically in :

- Be able to preprocess data obtained from textual sources
- Be able to employ named entity recognition and relationship extraction using SpaCy
- Be able to visualize results
- Be able to present insights and findings to client
- Be able to store data using the graph database Neo4j
- Be able to write clean and documented code.

## The Mission

A manager at a consultancy agency has been overrun by an influx of projects that involve large volumes of financial news. He hands you piles and piles of documents and asks you to read each one and provide a summary of: 

* Who is implicated in this document? and what are their relationships?*


### Must-have features

- A pipeline that takes a document and applies named entity recognition (NER) and relationship extraction of those entities
- A visualization of the entities within the text and their relationships in a network
- A validation strategy for your results

### Nice-to-have features

- Create a graphdata base to store your modeling results using Neo4j.
- Create an app and deploy it using Docker.

## Main Libraries used
- SpaCY
- NeuralCoref (from Hugging Face)

## Discussion

The following features are achieved.

 1. A pipeline that takes a document and applies named entity recognition (NER) and relationship extraction of those entities is implemented
 2. A visualization of the entities within the text and their relationships in a network in `Jaal`
 3. A custom NER model was developed and trained by scraping data from the gived dataset and wikipedia and was able to recognize more companies related to Crude catagory than the pretrained model from spaCy. 


## ## Installation and Usage

There is only one python file









Incompatibility of NeuralCoref with the latest version of SpaCY
While finding named entities in a text and extracting their relationships, applying coreference resolution to find all linguistic expressions (called mentions) in the given text that refer to the same real-world entity is very important. The available tools for this task are limited. The library attempted in this project NeuralCoref from Hugging Face. However, it can only be used by lowering the spaCy version (to spaCy 2.1.0), which compromises other tasks which are better accomplished by the latest vesion (spaCy 3.2 ????) 

## Insights

## A validation strategy for your results 
The validation strategy we followed is to look back at the text and collect the entities and their relationships manually and compare it to what the code delivers. It is notcied that most of the entities  and their relationships are recognized with some exceptions. 

Some of the limitations are:
    
  * In some cases named entities were extracted but their types were wrong. PERSON entities were recognised as ORG entities or viceversa. This could be solved by implementing `Entity Linking` to a knowledge base. Entity linking was not implemented in this project.
  * Some other entities were not recognized at all. It was attempted to improve this by training a custom NER model from a knowlege base.

## Further Development
  * Implementation of Neo4j
  * Deployment

## Personal situation

The project is worked 
>>>>>>> main
