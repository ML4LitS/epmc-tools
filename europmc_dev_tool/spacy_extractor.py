import spacy
import re
from spacy.matcher import Matcher
from .spacy_patterns import patterns as spacy_patterns

def extract_with_spacy(nlp, text, section="unknown"):
    """
    Extracts accession numbers from text using spaCy's Matcher.

    This function uses a predefined list of patterns to find potential
    accession numbers in a given text. It also performs context validation
    to reduce false positives.

    :param nlp: The loaded spaCy language model.
    :param text: The input text (sentence) to search within.
    :type text: str
    :param section: The document section where the text originates,
                    defaults to "unknown".
    :type section: str, optional
    :return: A list of dictionaries, where each dictionary represents
             an extracted accession number and its metadata.
    :rtype: list
    """
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    # Create a map from rule ID to pattern details for easy lookup
    pattern_map = {p["id"]: p for p in spacy_patterns}

    for p in spacy_patterns:
        matcher.add(p["id"], [p["pattern"]], greedy='LONGEST')

    matches = matcher(doc)
    extracted_data = []
    found_spans = set()

    for match_id, start, end in matches:
        span = doc[start:end]
        
        if (span.start_char, span.end_char) in found_spans:
            continue
        
        rule_id = nlp.vocab.strings[match_id]
        pattern_details = pattern_map.get(rule_id)

        if not pattern_details:
            continue

        # Context validation
        context_regex = pattern_details.get("context_regex")
        context_window = pattern_details.get("context_window", 0)
        
        context_found = True # Assume true if no context check is needed
        if context_regex:
            context_start = max(0, span.start_char - context_window)
            context_end = min(len(text), span.end_char + context_window)
            context_text = text[context_start:context_end]
            if not context_regex.search(context_text):
                context_found = False

        if context_found:
            found_spans.add((span.start_char, span.end_char))
            extracted_data.append({
                'acc.nname': pattern_details["label"],
                'exact': span.text,
                'span in sentence': (span.start_char, span.end_char),
                'sentence': text,
                'section': section
            })
            
    return extracted_data