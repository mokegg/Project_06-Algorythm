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
