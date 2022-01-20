import spacy
import neuralcoref
from spacy import displacy
nlp = spacy.load('en_core_web_lg') 
neuralcoref.add_to_pipe(nlp)


def coref(text):
    text = str(text)
    c_text = nlp(clean(text))
    res_text = nlp(c_text._.coref_resolved)
    resolved_text = displacy.render(res_text, style="ent")
    return resolved_text