######################### PACKAGES #########################
import spacy
from spacy.tokens import Token
from spacy import Language

from collections import deque

from nltk.corpus import reuters

import regex as re

import requests
from bs4 import BeautifulSoup

import pandas as pd

from jaal import Jaal

######################### NLP OBJECT #########################
nlp = spacy.load('en_core_web_lg')

######################### NLP PIPES #########################

Token.set_extension('ref_n', default='', force = True)
Token.set_extension('ref_t', default='', force = True)

@Language.component("init_coref")
def init_coref(doc):
    for e in doc.ents:
        if e.label_ in ['ORG', 'GOV', 'PERSON','MONEY']:
            e[0]._.ref_n, e[0]._.ref_t = e.text, e.label_
    return doc

def reset_pipeline(nlp, pipes):
    # remove all custom pipes
    custom_pipes = [pipe for (pipe, _) in nlp.pipeline
                    if pipe not in ['tagger', 'parser', 'ner',
                                    'tok2vec', 'attribute_ruler', 'lemmatizer']]
    for pipe in custom_pipes:
        _ = nlp.remove_pipe(pipe)
    # re-add specified pipes
    for pipe in pipes:
        if 'neuralcoref' == pipe or 'neuralcoref' in str(pipe.__class__):
            nlp.add_pipe(pipe, name='neural_coref')
        else:
            nlp.add_pipe(pipe)

reset_pipeline(nlp, ['init_coref'])

######################### HELP FUNCTIONS #########################

def synonyms(term):
    """
    source: https://stackoverflow.com/questions/52910297/pydictionary-word-has-no-synonyms-in-the-api
    """
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text.strip() for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})] 

def clean(article:str):
    pattern = re.compile("\n")
    article = re.sub(pattern,"",article)
    pattern = re.compile(" +")
    article = re.sub(pattern," ",article)
    pattern = re.compile("(\s\&lt;.{1,4}>)")
    article = re.sub(pattern,"",article)
    # pattern = re.compile(".'s")
    # article = re.sub(pattern,"'s",article) #???
    article = article.strip()
    #re.findall("(\w[^\.]*\.)",article)
    return article

######################### RELATION EXTRACTION FUNCTIONS #########################

# Actually we search for the shortest path between the
# subject running through our predicate (verb) to the object.
# subject and object are organizations in our examples.

# Here are the three helper functions omitted in the book:
# - bfs: breadth first searching the closest subject/object 
# - is_passive: checks if noun or verb is in passive form
# - find_subj: searches left part of tree for subject
# - find_obj: searches right part of tree for object

def bfs(root, ent_type: str, deps:list, first_dep_only:bool=False):
    """
    
    : root: token containing the word at the left of the verb, hopefully the subject?
    : ent_type: specifies entity type (for now always called for "ORG")
    : deps: ??? ['nsubjpass', 'nsubj:pass'] ???
    : first_dep_only: 
    """
    """Return first child of root (included) that matches
    ent_type and dependency list by breadth first search.
    Search stops after first dependency match if first_dep_only
    (used for subject search - do not "jump" over subjects)"""
    # deque to ease the access to the list
    to_visit = deque([root]) # queue for bfs

    while len(to_visit) > 0:
        # the left element of the queue is given to child and deleted from the queue
        child = to_visit.popleft()
        ## print("child", child, child.dep_)
        # check if the dependency of the token was one of those provided
        if child.dep_ in deps:
            # check if the label/entity type is the same as the one provided
            if child._.ref_t == ent_type:
                return child
            #else:
            #    for 
            # explore what to do if we keep looking after the first dependency match?
            # quid for a subject with an "and"???
            elif first_dep_only: # first match (subjects)
                return None
        # check if it is a compound (adjective),
        # if the noun it describes dependency is one of those provided
        # and if it has the right entity type but only works on the first token of the entity (customized pipe)
        # why doesn't it return the whole entity then? A compound is no subject by its own...?
        # add " or child.head.head.dep_ in deps " to the second condition only if ent_type=="MONEY"
        # or use the root of the entity?
        elif child.dep_ == 'compound' and \
             (child.head.dep_ in deps or child.head.head.dep_ in deps) and \
             child._.ref_t == ent_type: # check if contained in compound
            return child
        to_visit.extend(list(child.children))
    return None

def is_passive(token):
    if token.dep_.endswith('pass'): # noun
        return True
    for left in token.lefts: # verb
        if left.dep_ == 'auxpass':
            return True
    return False

def find_subj(pred, ent_type: str, passive: bool):
    """
    Find closest subject in predicates left subtree or
    predicates parent's left subtree (recursive).
    Has a filter on organizations.
    : pred: token containing a verb
    : ent_type: specifies entity type (for now always called for "ORG")
    : passive: specifies if the verb is in the passive form
    : return: pred's subject
    """
    ## To modify to make it work for different kind of entities

    # begins with the further related word on the left of the predicate
    for left in pred.lefts:
        if passive: # if pred is passive, search for passive subject
            subj = bfs(left, ent_type, ['nsubjpass', 'nsubj:pass'], True)
        else:
            subj = bfs(left, ent_type, ['nsubj'], True)
        if subj is not None: # found it!
            return subj
    
    # if the subject is not on the left tree of the predicate,
    # the predicate's head could be another verb with the same subject
    # example: Apple is looking at buying a startup
    if pred.head != pred and not is_passive(pred): # why not just "passive" instead of is_passive(pred)?
        return find_subj(pred.head, ent_type, passive) # climb up left subtree
    else:
        return None

def find_obj(pred, ent_type, excl_prepos):
    """
    Find closest object in predicates right subtree.
    Skip prepositional objects if the preposition is in exclude list.
    Has a filter on organizations.
    : pred: token containing a verb
    : ent_type: specifies entity type (for now always called for "ORG")
    : excl_prepos: excluded prepositions
    : return: object of the predicate
    """
    
    ## To modify to make it work for different kind of entities
        
    # looks into every related token on the right of the predicate
    # until it finds an object filling the conditions
    for right in pred.rights:
        ## print("right: ",right)
        obj = bfs(right, ent_type, ['dobj', 'pobj', 'iobj', 'obj', 'obl'])
        # if an object is found,
        # it looks that its preposition is not excluded
        if obj is not None:
            if obj.dep_ == 'pobj' and obj.head.lemma_.lower() in excl_prepos: # check preposition
                continue
            return obj
    return None

def extract_rel_dep(doc,
                    pred_name:str="", pred_synonyms:list=[],
                    subj_ents:list=['ORG', 'GOV', 'PERSON'],
                    obj_ents:list=['ORG', 'GOV', 'PERSON','MONEY'],
                    excl_prepos=[]):
    """
    Method extracting relationship(s) (may be plural!)
    It only returns triplets!
    : doc: text to analyze
    : pred_name: predicate
    : pred_synonyms: predicate's synonyms
    : excl_prepos: prepositions which can not precede the object chosen
    : return: triplet(s) with the subject and its entity type,
              the predicate and the object and its entity type
    """
    for token in doc:
        ## print(token, token.pos_, token.lemma_)
        # looks for a verb equivalent to the predicate referred to
        if token.pos_ == 'VERB':# and token.lemma_ in pred_synonyms:
            ## print("found token: ",token)
            # saves that verb as a predicate (readability)
            # looks if it is passive
            # and then searches for the subject of the verb
            pred = token
            passive = is_passive(pred)
            ## print("passive: ",passive)
            for subj_ent in subj_ents:
                subj = find_subj(pred, subj_ent, passive)
                ## print("subject: ",subj)
                # if the subject is found, it looks for the object
                if subj is not None:
                    for obj_ent in obj_ents:
                        obj = find_obj(pred, obj_ent, excl_prepos)
                        ## print("object: ",obj)
                        if obj is not None:
                            # if there is a subject and an object,
                            # it sets the triplet in the following order:
                            # active subject, verb in active form, passive subject
                            if passive: # switch roles
                                obj, subj = subj, obj
                            yield ((subj._.ref_n, subj._.ref_t), pred.lemma_, #, pred_name
                                   (obj._.ref_n, obj._.ref_t))

######################### RELATION EXTRACTION #########################
# fileids = reuters.fileids("crude")
# crude = {}
# for fileid in fileids:
#     file = clean(reuters.raw(fileid))
#     crude[fileid] = nlp(file)

# verb = "sell"
# relations = {}
# subjects = []
# subjects_label = []
# verbs = []
# objects = []
# objects_label = []
# for fileid in crude.keys():
#     relations[fileid] = [relation for relation in extract_rel_dep(crude[fileid],pred_name=verb,pred_synonyms=[verb]+synonyms(verb), excl_prepos=[])]
# for fileid in relations.keys():
#     print(fileid,"\n",(relation for relation in relations[fileid]))
#     for relation in relations[fileid]:
#         subject_tuple, verb, object_tuple = relation
#         subjects.append(subject_tuple[0])
#         subjects_label.append(subject_tuple[1])
#         verbs.append(verb)
#         objects.append(object_tuple[0])
#         objects_label.append(object_tuple[1])

fileids = reuters.fileids("crude")[0:20]
crude = {}
main_verb = "sell"
relations = {}
relationships = pd.DataFrame({"subjects":[],"subjects_label":[],"verbs":[],"objects":[],"objects_label":[]})
for fileid in fileids:
    file = clean(reuters.raw(fileid))
    crude[fileid] = nlp(file)
    relations[fileid] = [relation for relation in extract_rel_dep(crude[fileid],pred_name=main_verb,pred_synonyms=[main_verb]+synonyms(main_verb), excl_prepos=[])]
    # print(fileid)
    for relation in relations[fileid]:
        # print(relation)
        subject_tuple, verb, object_tuple = relation
        rel_data = {"subjects":subject_tuple[0],"subjects_label":subject_tuple[1],"verbs":verb,"objects":object_tuple[0],"objects_label":object_tuple[1]}
        relationships = relationships.append(rel_data,ignore_index=True)

edge_df = relationships[["subjects","verbs","objects"]].rename(columns={"subjects":"from","verbs":"label","objects":"to"})

#Import and clean
# edge_df = pd.DataFrame({"from":subjects,"to":objects,"label":verbs})
# edge_df.drop(edge_df.filter(regex="Unname"),axis=1, inplace=True) # not needed without csv
edge_df.drop_duplicates(inplace = True)
edge_df.reset_index(drop=True, inplace=True)

#remove duplicates based on the from and to columns 
edge_df = edge_df.drop_duplicates(
  subset = ['from', 'to'],
  keep = 'first').reset_index(drop = True)
edge_df['Type'] = 'Directed'

node_df = pd.concat([edge_df["from"],edge_df["to"]], axis=0).value_counts().reset_index().rename(columns={'index': 'id', 0: 'weight'})

# init Jaal and run server
Jaal(edge_df, node_df).plot(vis_opts={'height': '600px', # change height
                                      'interaction':{'hover': True}, # turn on-off the hover 
                                      'physics':{'stabilization':{'iterations': 100}}}, directed=True) # define the convergence iteration of network