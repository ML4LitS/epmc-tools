import spacy
import re
import requests
import json
import os
from spacy.matcher import Matcher
from .spacy_patterns import patterns as spacy_patterns, blacklist

CACHE_FILE = '/home/stirunag/work/github/epmc-tools/uri_cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def extract_with_spacy(nlp, text, section="unknown", sentence_id=None, offline=False):
    """
    Extracts accession numbers and resources from text using spaCy's Matcher.

    This function uses a predefined list of patterns to find potential
    accession numbers and resources in a given text. It also performs context validation
    to reduce false positives.

    :param nlp: The loaded spaCy language model.
    :param text: The input text (sentence) to search within.
    :type text: str
    :param section: The document section where the text originates,
                    defaults to "unknown".
    :type section: str, optional
    :param sentence_id: The ID of the sentence, defaults to None.
    :type sentence_id: str, optional
    :param offline: If True, skips online validation.
    :type offline: bool, optional
    :return: A list of dictionaries, where each dictionary represents
             an extracted accession number or resource and its metadata.
    :rtype: list
    """
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    cache = load_cache()

    # Create a map from rule ID to pattern details for easy lookup
    pattern_map = {p["label"]: p for p in spacy_patterns}

    for p in spacy_patterns:
        matcher.add(p["label"], [[{"TEXT": {"REGEX": p["pattern"]}}]], greedy='LONGEST')

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
        
        context_found = True # Assume true if no context check is needed
        if context_regex:
            if not re.search(context_regex, text):
                context_found = False

        # Check against blacklist patterns
        is_blacklisted = False
        for pattern in blacklist:
            if re.fullmatch(pattern, span.text):
                is_blacklisted = True
                break

        if context_found and not is_blacklisted:
            
            extraction_type = "resource" if pattern_details["label"].startswith('R') else "accession"
            
            uri = pattern_details.get('normalization_url', '')
            validation_method = pattern_details.get('validation_method')
            is_valid = True

            if not offline and validation_method in ['online', 'onlineWithContext']:
                if uri:
                    if not pattern_details["label"].startswith('R'):
                        uri = f"{uri}/{span.text}"

                    if uri in cache and cache[uri]:
                        pass  # Use cached result
                    elif uri in cache and not cache[uri]:
                        is_valid = False
                    else:
                        try:
                            response = requests.get(uri, timeout=5, stream=True)
                            if response.status_code >= 400:
                                cache[uri] = False
                                is_valid = False
                            else:
                                cache[uri] = True
                        except requests.exceptions.RequestException:
                            cache[uri] = False
                            is_valid = False
            
            if is_valid:
                if uri and not pattern_details["label"].startswith('R') and (offline or validation_method not in ['online', 'onlineWithContext']):
                    uri = f"{uri}/{span.text}"

                found_spans.add((span.start_char, span.end_char))
                extracted_data.append({
                    'type': extraction_type,
                    'name': pattern_details["label"],
                    'exact': span.text,
                    'span': [span.start_char, span.end_char],
                    'uri': uri,
                    'sentence_id': sentence_id
                })
            
    save_cache(cache)
    return extracted_data