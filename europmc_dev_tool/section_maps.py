import re

ordered_labels = [
    'TITLE', 'ABSTRACT', 'INTRO', 'METHODS', 'RESULTS', 'DISCUSS', 'CONCL', 'CASE',
    'ACK_FUND', 'AUTH_CONT', 'COMP_INT', 'ABBR', 'SUPPL', 'REF', 'ACK_FUND', 'ABBR',
    'COMP_INT', 'SUPPL', 'APPENDIX', 'AUTH_CONT'
]

titleMapsBody = {
    'INTRO': [
        'introduction', 'background', 'related literature', 'literature review', 'objective',
        'aim ', 'purpose of this study', 'study (purpose|aim|aims)', r'\d+\. (purpose|aims|aim)',
        '(aims|aim|purpose) of the study', '(the|drug|systematic|book) review', 'review of literature',
        'related work', 'recent advance', 'overview', 'historical overview',
        'scope', 'context', 'rationale', 'hypothesis', 'motivation'
    ],
    'METHODS': [
        'methods and materials', 'method', 'material', 'experimental procedure',
        'implementation', 'methodology', 'treatment', 'statistical analysis', "experimental",
        "protocol", "protocols", 'study protocol', 'construction and content',
        'analysis', 'utility', 'design', "theory", 'data analysis', 'data collection'
    ],
    'RESULTS': [
        'result', 'finding', 'diagnosis', 'outcomes', 'findings', 'observations',
        'key results', 'main results', 'data', 'analysis results'
    ],
    'DISCUSS': [
        'discussion', 'management of', 'limitations', 'perspective', 'commentary',
        'interpretation', 'insights', 'reflection', 'critical analysis'
    ],
    'CONCL': [
        'conclusion', 'key message', 'future', 'summary', 'recommendation',
        'implications for clinical practice', 'concluding remark'
    ],
    'CASE': [
        'case study report', 'case report', 'case presentation', 'case description',
        r'case \d+', r'\d+\. case', 'case summary', 'case history', 'case overview',
        'case study', 'case examination'
    ],
    'ACK_FUND': [
        'funding', 'acknowledgement', 'acknowledgment', 'financial disclosure',
        'funding sources', 'funding support', 'financial support'
    ],
    'AUTH_CONT': [
        "author contribution", "authors' contribution", "author's contribution",
        "contribution of authors"
    ],
    'COMP_INT': [
        'competing interest', 'conflict of interest', 'conflicts of interest',
        'disclosure', 'declaration', 'competing interests'
    ],
    'ABBR': [
        'abbreviation', 'abbreviations list', 'acronyms', 'nomenclature',
        'glossary'
    ],
    'SUPPL': [
        'supplemental data', 'supplementary file', 'supporting information',
        'supplemental material', 'additional material', 'appendix'
    ]
}

titleExactMapsBody = {
    'INTRO': [
        "aim", "aims", "purpose", "purposes", "purpose/aim", "purpose of study", "review", "overview", "background"
    ],
    'METHODS': [
        "experimental", "the study", "protocol", "protocols", "procedure", "methodology", "data analysis"
    ],
    'DISCUSS': [
        "management", "comment", "comments", "discussion", "limitations", "perspectives"
    ],
    'CASE': [
        "case", "cases", "case study", "case report", "case overview"
    ]
}

titleMapsBack = {
    'REF': [
        'reference', 'literature cited', 'references', 'bibliography', 'citations',
        'works cited', 'cited literature'
    ],
    'ACK_FUND': [
        'funding', 'acknowledgement', 'acknowledgment', 'open access', 'financial support',
        'grant', 'author note', 'financial disclosure', 'support statement'
    ],
    'ABBR': [
        'abbreviation', 'glossary', 'abbreviations list', 'acronyms', 'terminology'
    ],
    'COMP_INT': [
        'competing interest', 'conflict of interest', 'conflicts of interest',
        'disclosure', 'declaration'
    ],
    'CASE': [
        'case study report', 'case report', 'case presentation', 'case description'
    ],
    'SUPPL': [
        'supplemental data', 'supplementary file', 'supporting information',
        'supplemental material', 'appendix'
    ]
}

compiled_titleMapsBody = {
    key: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for key, patterns in titleMapsBody.items()
}
compiled_titleExactMapsBody = {
    key: [pattern.lower() for pattern in patterns]
    for key, patterns in titleExactMapsBody.items()
}
compiled_titleMapsBack = {
    key: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for key, patterns in titleMapsBack.items()
}
