# -*- coding: utf-8 -*-

import sys
import getopt
from spacy import load
from typing import NamedTuple
from nltk.corpus import wordnet


nlp = load("en_core_web_sm")

class ISLToken(NamedTuple):
    """Class to hold ISL token with relevant syntactic information"""
    
    text: str
    orig_id: int
    dep: str
    head: int
    tag: str
    ent_type: str
    children: list
    
def filter_spans(spans):
    """Filter a sequence of spans so they don't contain overlaps"""
    
    get_sort_key = lambda span: (span.end - span.start, -span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        # Check for end - 1 here because boundaries are inclusive
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span.start, span.end))
    result = sorted(result, key=lambda span: span.start)
    return result

def token_chunker(doc):
    """Merge entities and noun chunks into one token"""
    
    spans = list(doc.ents) + list(doc.noun_chunks)
    spans = filter_spans(spans)
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)
            
def cc_chunker(doc):
    """
    Merge cc (only 'and' for now) conjuncions for like elements. To be run
    after token_chunker.
    returns -1 if and is chunked, or the token index if sentence is to be split
    """    
    
    for token in doc:
        i = token.i
        if (token.text.lower() == "and") and (token.dep_ == "cc"):
            if i == 0:
                return 0
            
            # if head is attached to the 'and', merge the phrase
            if (token.head.i == i-1):
                # debug:
                # print("merging and chunk:",token.head.left_edge.text, token.head.right_edge.text)
                and_span = doc[token.head.left_edge.i : token.head.right_edge.i + 1]
                with doc.retokenize() as retokenizer:
                   retokenizer.merge(and_span)
                   
                # no need to split
                return -1
            
            # else return 'and' index to split 
            return i
    
    # default to no split
    return -1

# list of articles etc. not present in ISL
droplist = {'be', 'do', 'a', 'the', 'of', 'for', 'from', 'to'}

# synonyms in ISL list for various common English words
worddict = {'there': ['her', 'she', 'that', 'it'], 'no': ['not', 'n\'t'],
            'possible': ['can', 'may']}

def find_syn(token):
    """Finds a synonym that exists in the available wordlist, from WordNet"""
    
    token_synsets = wordnet.synsets(token)
    for synset in token_synsets:
        for l in synset.lemma_names():
            if l in wordlist:
                return l

    for key in worddict.keys():
        if token in worddict[key]:
            return key
    return token


def eng_isl_translate(doc):
    """Function to translate English to ISL gloss"""  
    
    # init lists
    dep_list = []
    type_list = []
    tag_list = []   
    ISLTokens = []
    done_list = []
    
    # debug:
    # for token in doc:
    #     print(token.text, token.dep_, token.head.text, token.tag_, token.ent_type_,
    #           [child for child in token.children])

    # chunk noun phrases and entities
    token_chunker(doc)
    
    # used to split cc'd clauses
    doc2 = None
    and_tkn = None
    
    # check for cc and process it
    for token in doc:
        if "CC" == token.tag_ and "and" == token.text.lower():
            and_i = cc_chunker(doc)         
            
            # if sentence needs to be split to clauses
            if and_i > -1:
                
                # get 'root' of second piece
                doc2_root_i = doc[and_i + 1 : ].root.i - and_i - 1
                
                doc2 = doc[and_i + 1 : ].as_doc()
                
                # set 'ROOT'
                doc2[doc2_root_i].dep_ = "ROOT"
                
                # get the cc token
                and_tkn = doc[and_i]
                
                # truncate original doc
                # we need to account for the case where a seentence starts with 'and'
                if and_i == 0:
                    # debug:
                    # print("Initial and")
                    # print(and_tkn.text, and_tkn.dep_, and_tkn.head.text,
                    #       and_tkn.tag_, and_tkn.ent_type_,
                    #       [child for child in and_tkn.children])
                    
                    
                    ISLTokens2 = eng_isl_translate(doc2)
                    ISLTokens.append(and_tkn)
                    ISLTokens.extend(ISLTokens2)
                    return ISLTokens
                    
                # the regular case:
                doc = doc[0 : and_i].as_doc()
                
            # break at first 'and', as the process is recursive
            break
        
    for token in doc:
        dep_list.append(token.dep_)
        tag_list.append(token.tag_)
        type_list.append(token.ent_type_)
        
    
        
    # time related words are first in ISL sentences
    if "DATE" in type_list:
        date_i = type_list.index("DATE")
        done_list.append(date_i)
        tkn = doc[date_i]
        ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i, tkn.tag_,
                                  tkn.ent_type_, [child for child in tkn.children]))
        if doc[date_i].dep_ == "pobj":
            date_ii = doc[date_i].head.i
            tkn = doc[date_ii]
            done_list.append(date_ii)
            ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i,
                                      tkn.tag_, tkn.ent_type_,
                                      [child for child in tkn.children]))
    
    # subjects come next
    if "nsubj" in dep_list:
        nsubj_i = dep_list.index("nsubj")
        tkn = doc[nsubj_i]
        if not tkn.tag_[0] == 'W' and not tkn.i in done_list:
            done_list.append(nsubj_i)
            ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i, tkn.tag_,
                                  tkn.ent_type_, [child for child in tkn.children]))
    
    
    root_i = dep_list.index("ROOT")
    root_children = [child for child in doc[root_i].children]
    
    # checks to see if words are in the following categories and appends them
    if not {"xcomp", "ccomp", "prep", "advcl"}.isdisjoint([child.dep_ for child in doc[root_i].children]):
        for child in doc[root_i].children:
            if child.dep_ in ("xcomp", "ccomp", "prep", "advcl"):
                subtree_span = doc[child.left_edge.i : child.right_edge.i + 1]
                for tkn in subtree_span:
                    
                    if not tkn.i in done_list:
                        ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, 
                                                  tkn.head.i, tkn.tag_, tkn.ent_type_, 
                                                  [child for child in tkn.children]))
                        done_list.append(tkn.i)
               
    # verb obects usually come last
    if "dobj" in [child.dep_ for child in doc[root_i].children]:
        dobj_i_1 = [child.dep_ for child in doc[root_i].children].index("dobj")
        dobj_i = root_children[dobj_i_1].i
        tkn = doc[dobj_i]
        if not dobj_i in done_list:
            done_list.append(dobj_i)
            ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i, tkn.tag_,
                                      tkn.ent_type_, [child for child in tkn.children]))
            
    tkn = doc[root_i]
    done_list.append(root_i)
    ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i, tkn.tag_,
                              tkn.ent_type_, [child for child in tkn.children]))
    isl_root_i = len(ISLTokens) - 1
    
    
    # auxiliaries like must, can etc. come after the object
    if "aux" in [child.dep_ for child in doc[root_i].children]:
        aux_i_1 = [child.dep_ for child in doc[root_i].children].index("aux")
        aux_i = root_children[aux_i_1].i
        tkn = doc[aux_i]
        done_list.append(aux_i)
        ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i, tkn.tag_,
                                  tkn.ent_type_, [child for child in tkn.children]))
        
    # negatives come last in non-questions
    if "neg" in dep_list:
        neg_i = dep_list.index("neg")
        tkn = doc[neg_i]
        done_list.append(neg_i)
        ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i, tkn.tag_,
                                  tkn.ent_type_, [child for child in tkn.children]))
        
    # question markers come dead last
    if tag_list[0][0] == 'W':
        tkn = doc[0]
        done_list.append(0)
        ISLTokens.append(ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i, tkn.tag_,
                                  tkn.ent_type_, [child for child in tkn.children]))
    
    j = isl_root_i
    # insert children of ROOT next to it
    for tkn in root_children:
        if not tkn.i in done_list:
            if not tkn.dep_ in ["aux", "punct", "neg"]:
                done_list.append(tkn.i)
                ISLTokens.insert(j, ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i,
                                             tkn.tag_, tkn.ent_type_,
                                             [child for child in tkn.children]))
                j += 1
    # insert the remainders after
    for tkn in doc:
        if not tkn.i in done_list:
            if not tkn.dep_ in ["aux", "punct", "neg"]:
                done_list.append(tkn.i)
                ISLTokens.insert(j, ISLToken(tkn.lemma_, tkn.i, tkn.dep_, tkn.head.i,
                                             tkn.tag_, tkn.ent_type_,
                                             [child for child in tkn.children]))
                j += 1
        
        
    #print(len(ISLTokens))
    
    # delete tokens not present in ISL
    ISLTokens[:] = [isl_tkn for isl_tkn in ISLTokens if not (isl_tkn.text in droplist)]
            
    # debug:    
    # for token in doc:
    #     print(token.text, token.dep_, token.head.text, token.tag_, token.ent_type_,
    #           [child for child in token.children])
        
    # check if there's a split clause and process recursively
    if doc2:
        ISLTokens2 = eng_isl_translate(doc2)
        ISLTokens.append(and_tkn)
        ISLTokens.extend(ISLTokens2)
        
    
    # check if word present in list. currently deprecated, as the check is
    # expected at the frontend
    
    # for word in sen_list:
    # word_lower = word.__str__().lower()
    # # print('Word to be appended: ' + word_lower)
    # if word_lower in wordlist:
    #     new_sen_list.append(word_lower)
    # else:  # WordNetLemmatizer().lemmatize(word_lower) in wordlist:
    #     new_sen_list.append(WordNetLemmatizer().lemmatize(word_lower))
    # # else:
    # #     found_alt = find_syn(word_lower)
    # #     new_sen_list.append(found_alt)
    
    return ISLTokens

def translate_to_tokens(text):
    """Convert Eng text to o/p as ISLToken list"""
    
    doc = nlp(text)
    
    ISLTknOP = []
    
    for sent in doc.sents:
        ISLSent = eng_isl_translate(sent.as_doc())
        ISLTknOP.extend(ISLSent)
        
    return ISLTknOP

def translate_text(text):
    """Convert ISLToken output to space separated gloss list"""
    
    raw_token_list = translate_to_tokens(text)
    
    raw_isl_text = " ".join([isl_tkn.text.lower() for isl_tkn in raw_token_list])
    
    return raw_isl_text

def main(argv):
    text=''
    
    try:
        opts, args = getopt.getopt(argv,"ht:",["help", "text="])
    except getopt.GetoptError:
        print('spacy_rules.py -t <English text>')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('spacy_rules.py -t <English text>')
            sys.exit()
        elif opt in ("-t", "--text"):
            text = arg
            
    if not text:
        text = "Where is Sanket going?"
        
    print(translate_text(text))


if __name__ == "__main__":
   main(sys.argv[1:])

