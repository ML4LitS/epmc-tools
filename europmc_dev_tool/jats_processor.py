import re
from bs4 import BeautifulSoup
from rapidfuzz import process as fuzz_process, fuzz
import spacy
from .section_maps import (
    ordered_labels, compiled_titleMapsBody, compiled_titleExactMapsBody, compiled_titleMapsBack
)

class XMLProcessor:
    def __init__(self, sentenciser=True):
        self.sentenciser = sentenciser
        if sentenciser:
            self.nlp = spacy.load("en_core_sci_sm", disable=["parser", "ner", "tagger", "lemmatizer"])
            self.nlp.add_pipe("sentencizer")
        else:
            self.nlp = None

    def sentence_split(self, text):
        if self.sentenciser and self.nlp:
            doc = self.nlp(text)
            return [sent.text.strip() for sent in doc.sents]
        else:
            return [text.strip()] if text.strip() else []

    def createSecTag(self, soup, secType):
        secTag = soup.new_tag('SecTag')
        secTag['type'] = secType
        return secTag

    def call_sentence_tags(self, ch):
        sentences = []
        for gch in ch.children:
            if isinstance(gch, str):
                continue
            if gch.name in ['title', 'label', 'td', 'th']:
                text = gch.get_text(separator=' ', strip=True)
                if text:
                    sents = self.sentence_split(text)
                    sentences.extend(sents)
            elif gch.name == 'p':
                sentences.extend(self.process_p_tag(gch))
            else:
                text = gch.get_text(separator=' ', strip=True)
                if text:
                    sentences.extend(self.sentence_split(text))
        return sentences

    def process_p_tag(self, gch):
        text = gch.get_text(separator=' ', strip=True)
        return self.sentence_split(text) if text else []

    def titleMatch(self, title, secFlag):
        matchKeys = []
        title_lower = title.lower().strip()
        if secFlag == 'body':
            titleMaps = compiled_titleMapsBody
            exactMaps = compiled_titleExactMapsBody
        else:
            titleMaps = compiled_titleMapsBack
            exactMaps = {}

        for key, patterns in exactMaps.items():
            if title_lower in patterns:
                matchKeys.append(key)
                break
        if not matchKeys:
            for key, patterns in titleMaps.items():
                if any(pattern.search(title_lower) for pattern in patterns):
                    matchKeys.append(key)
        return ','.join(matchKeys) if matchKeys else None

    def section_tag(self, soup):
        if soup.body:
            for sec in soup.body.find_all('sec', recursive=False):
                title = sec.find('title')
                if title:
                    title_text = title.get_text(separator=' ', strip=True)
                    mappedTitle = self.titleMatch(title_text, 'body')
                    if mappedTitle:
                        secBody = self.createSecTag(soup, mappedTitle)
                        sec.wrap(secBody)
        if soup.back:
            for sec in soup.back.find_all(['sec', 'ref-list'], recursive=False):
                if sec.name == 'ref-list':
                    secRef = self.createSecTag(soup, 'REF')
                    sec.wrap(secRef)
                else:
                    title = sec.find('title')
                    if title:
                        title_text = title.get_text(separator=' ', strip=True)
                        mappedTitle = self.titleMatch(title_text, 'back')
                        if mappedTitle:
                            secBack = self.createSecTag(soup, mappedTitle)
                            sec.wrap(secBack)

    def process_full_text(self, xml_content):
        xml_content = re.sub(r'<body(\s[^>]*)?>', '<orig_body\\1>', xml_content)
        xml_content = xml_content.replace('</body>', '</orig_body>')
        try:
            xml_soup = BeautifulSoup(xml_content, 'lxml')
            if xml_soup.html: xml_soup.html.unwrap()
            if xml_soup.body: xml_soup.body.unwrap()
            if xml_soup.find('orig_body'):
                xml_soup.find('orig_body').name = 'body'

            article_tag = xml_soup.find('article')
            if article_tag:
                open_status = article_tag.get('open-status', '')
                article_type = article_tag.get('article-type', '')
            else:
                open_status = ''
                article_type = ''
            article_ids = {}
            for id_tag in xml_soup.find_all('article-id'):
                id_type = id_tag.get('pub-id-type', 'unknown')
                article_ids[id_type] = id_tag.text.strip()
            if not article_ids:
                return None

            self.section_tag(xml_soup)
            sections = {}
            for sec_tag in xml_soup.find_all('SecTag'):
                sec_type = sec_tag.get('type', 'unknown').strip().upper()
                if sec_type not in sections:
                    sections[sec_type] = []
                for nested_sec in sec_tag.find_all('SecTag', recursive=True):
                    nested_sec.extract()
                sentences = self.call_sentence_tags(sec_tag)
                sections[sec_type].extend(sentences)

            sections = {k: v for k, v in sections.items() if v}
            return {
                'article_ids': article_ids,
                'open_status': open_status,
                'article_type': article_type,
                'keywords': [],
                'sections': sections
            }
        except Exception as e:
            print(f"Error processing article: {e}")
            return None

    def process_json(self, data, ordered_labels):
        if not data or 'sections' not in data:
            return {}
        if not ordered_labels:
            return {}

        sections = data['sections']
        if "TITLE-GROUP" in sections:
            sections["TITLE"] = sections.pop("TITLE-GROUP")
        section_keys = set(sections.keys())
        ordered_labels_set = set(ordered_labels)
        unfound_keys = section_keys - ordered_labels_set
        normalized_unfound_keys = {key.replace(" ", "").upper(): key for key in unfound_keys}

        mapped_labels = {}
        for normalized_key, original_key in normalized_unfound_keys.items():
            if not normalized_key:
                mapped_labels[original_key] = "OTHER"
                continue
            match, score = fuzz_process.extractOne(normalized_key, ordered_labels, scorer=fuzz.partial_ratio)
            if not match or score < 80:
                mapped_labels[original_key] = "OTHER"
            else:
                mapped_labels[original_key] = match

        result_json = {}
        for section_key in sections:
            label = mapped_labels.get(section_key, section_key)
            texts = [{"text": text} for text in sections[section_key]]
            if label in result_json:
                result_json[label].extend(texts)
            else:
                result_json[label] = texts

        ordered_json = {}
        for label in ordered_labels:
            if label in result_json:
                ordered_json[label] = result_json.pop(label)
        ordered_json.update(result_json)

        sent_id = 1
        for section in ordered_json.values():
            for entry in section:
                entry["sent_id"] = sent_id
                sent_id += 1

        combined_data = {
            'article_ids': data['article_ids'],
            'open_status': data['open_status'],
            'article_type': data['article_type'],
            'keywords': data['keywords'],
            'sections': ordered_json
        }
        return combined_data
