# # spacy_patterns.py

import re

patterns = [
    # CATH domain identifiers
    {"label": "cath", "id": "cath_1", "pattern": [{"TEXT": {"REGEX": r"^(?=.{7}$)[1-9][0-9A-Za-z]{3}(?:[A-Za-z]|0)[0-9]{2}$"}}], "context_regex": re.compile(r"(?i)(\bcath\b|cath-Gene3D|cath Gene3D|c\.a\.t\.h|\bdomain\b|\bfamilies\b|\bcathnode\b|\bpdb\b|\bsuperfamily\b)"), "context_window": 20000},
    {"label": "cath", "id": "cath_2", "pattern": [{"TEXT": {"REGEX": r"^[1-4]\.[0-9]+\.[0-9]+\.[0-9]+$"}}], "context_regex": re.compile(r"(?i)(\bcath\b|cath-Gene3D|cath Gene3D|c\.a\.t\.h|\bdomain\b|\bfamilies\b|\bcathnode\b|\bpdb\b|\bsuperfamily\b)"), "context_window": 20000},

    # Cellosaurus cell line IDs
    {"label": "cellosaurus", "id": "cellosaurus_1", "pattern": [{"TEXT": {"REGEX": r"^CVCL_[A-Za-z0-9]{4}$"}}], "context_regex": re.compile(r"(?i)(cells|cellosaurus|cellosaurus database|Cell lines|Cell Bank|accession number|RRID: )"), "context_window": 20000},

    # ChEBI
    {"label": "chebi", "id": "chebi_1", "pattern": [{"TEXT": "CHEBI:"}, {"LIKE_NUM": True}], "context_regex": re.compile(r"(?i)(chebi|compound)"), "context_window": 20000},

    # ChEMBL
    {"label": "chembl", "id": "chembl_1", "pattern": [{"TEXT": {"REGEX": r"(?i)^chembl[0-9]+$"}}], "context_regex": re.compile(r"(?i)(chembl|compound)"), "context_window": 20000},

    # ComplexPortal
    {"label": "complexportal", "id": "complexportal_1", "pattern": [{"TEXT": {"REGEX": r"(?i)^CPX-[0-9]+$"}}], "context_regex": re.compile(r"(?i)(protein|complex)"), "context_window": 20000},

    # EBI Metagenomics
    {"label": "metagenomics", "id": "metagenomics_1", "pattern": [{"TEXT": {"REGEX": r"^SRS[0-9]{6}$"}}], "context_regex": re.compile(r"(?i)(samples|ebi metagenomics|metagenomics|database)"), "context_window": 20000},

    # Experimental Factor Ontology (EFO)
    {"label": "efo", "id": "efo_1", "pattern": [{"TEXT": {"REGEX": r"^EFO_[0-9]+$"}}], "context_regex": None, "context_window": 0},
    {"label": "efo", "id": "efo_2", "pattern": [{"TEXT": {"REGEX": r"^EFO:[0-9]+$"}}], "context_regex": None, "context_window": 0},

    # GSE (GEO Series)
    {"label": "gse", "id": "gse_1", "pattern": [{"TEXT": {"REGEX": r"^GSE[0-9]+$"}}], "context_regex": None, "context_window": 0},

    # GEO (Gene Expression Omnibus)
    {"label": "geo", "id": "geo_1", "pattern": [{"TEXT": {"REGEX": r"^G(?:PL|SM|SE|DS)[0-9]+$"}}], "context_regex": re.compile(r"(?i)(gene expression omnibus|genome|geo|accession|functional genomics|data repository|data submissions)"), "context_window": 20000},

    # EGA (European Genome-phenome Archive)
    {"label": "ega.study", "id": "ega_study_1", "pattern": [{"TEXT": {"REGEX": r"^EGAS[0-9]{11}$"}}], "context_regex": re.compile(r"(?i)(ega|accession|archive|studies|study|European Genome-phenome Archive|European Genome phenome Archive)"), "context_window": 20000},
    {"label": "ega.dataset", "id": "ega_dataset_1", "pattern": [{"TEXT": {"REGEX": r"^EGAD[0-9]{11}$"}}], "context_regex": re.compile(r"(?i)(ega|accession|data set|datasets|dataset|validation set|validation sets|archive|European Genome-phenome Archive|European Genome phenome Archive)"), "context_window": 20000},
    {"label": "ega.dac", "id": "ega_dac_1", "pattern": [{"TEXT": {"REGEX": r"^EGAC[0-9]{11}$"}}], "context_regex": re.compile(r"(?i)(ega|accession|archive|dac|European Genome-phenome Archive|European Genome phenome Archive)"), "context_window": 20000},

    # EMDB (Electron Microscopy Data Bank)
    {"label": "emdb", "id": "emdb_1", "pattern": [{"TEXT": {"REGEX": r"^EMD-[0-9]{4,5}$"}}], "context_regex": re.compile(r"(?i)(emdb|accession|code)"), "context_window": 20000},

    # EMPIAR (Electron Microscopy Public Image Archive)
    {"label": "empiar", "id": "empiar_1", "pattern": [{"TEXT": {"REGEX": r"^EMPIAR-[0-9]{5}$"}}], "context_regex": None, "context_window": 20000},

    # GenBank/ENA/DDBJ (INSDC nucleotide accessions)
    {"label": "gen", "id": "gen_1", "pattern": [{"TEXT": {"REGEX": r"^[A-Z][0-9]{5}$"}}], "context_regex": re.compile(r"(?i)(genbank|\bgen\b|\bena\b|ddbj|embl|european nucleotide archive|accession|nucleotide|archive|assembled|annotated|sequence|sequences)"), "context_window": 20000},
    {"label": "gen", "id": "gen_2", "pattern": [{"TEXT": {"REGEX": r"^[A-Z]{2}[0-9]{6}$"}}], "context_regex": re.compile(r"(?i)(genbank|\bgen\b|\bena\b|ddbj|embl|european nucleotide archive|accession|nucleotide|archive|assembled|annotated|sequence|sequences)"), "context_window": 20000},

    # Ensembl stable IDs (genes, transcripts, proteins)
    {"label": "ensembl", "id": "ensembl_1", "pattern": [{"TEXT": {"REGEX": r"^ENS[A-Za-z]*[GTP][0-9]{11,}(?:\.[0-9]+)?$"}}], "context_regex": re.compile(r"(?i)(ensembl|accession|transcript|sequence)"), "context_window": 20000},

    # Gene Ontology (GO)
    {"label": "go", "id": "go_1", "pattern": [{"TEXT": {"REGEX": r"^GO:[0-9]{7}$"}}], "context_regex": re.compile(r"(?i)(go|gene ontology)"), "context_window": 20000},

    # HGNC (HUGO Gene Nomenclature Committee)
    {"label": "hgnc", "id": "hgnc_1", "pattern": [{"TEXT": {"REGEX": r"^HGNC:[0-9]+$"}}], "context_regex": re.compile(r"(?i)(HUGO Gene Nomenclature Committee|hugo|gene|nomenclature|committee|database)"), "context_window": 20000},

    # Human Protein Atlas antibodies
    {"label": "hpa", "id": "hpa_1", "pattern": [{"TEXT": {"REGEX": r"(?i)^HPA[0-9]{6}$"}}], "context_regex": None, "context_window": 0},
    {"label": "hpa", "id": "hpa_2", "pattern": [{"TEXT": {"REGEX": r"(?i)^CAB[0-9]{6}$"}}], "context_regex": None, "context_window": 0},

    # 1000 Genomes / IGSR samples
    {"label": "igsr", "id": "igsr_1", "pattern": [{"TEXT": {"REGEX": r"^HG0[0-4][0-9]{3}$"}}], "context_regex": re.compile(r"(?i)(\bcell\b|sample|iPSC|iPSCs|fibroblast|fibroblasts|QTL|eQTL|pluripotent|induced|\bdonor\b|\bstem\b|EBiSC|1000 Genomes|Coriell|\bLCL\b|lymphoblastoid)"), "context_window": 1000},
    {"label": "igsr", "id": "igsr_2", "pattern": [{"TEXT": {"REGEX": r"^(?:NA|GM)[0-2][0-9]{4}$"}}], "context_regex": re.compile(r"(?i)(\bcell\b|sample|iPSC|iPSCs|fibroblast|fibroblasts|QTL|eQTL|pluripotent|induced|\bdonor\b|\bstem\b|EBiSC|1000 Genomes|Coriell|\bLCL\b|lymphoblastoid)"), "context_window": 1000},

    # IntAct
    {"label": "intact", "id": "intact_1", "pattern": [{"TEXT": {"REGEX": r"^EBI-[0-9]+$"}}], "context_regex": re.compile(r"(?i)(intact|interaction|interactions|protein)"), "context_window": 20000},

    # InterPro
    {"label": "interpro", "id": "interpro_1", "pattern": [{"TEXT": {"REGEX": r"(?i)^IPR[0-9]{6}$"}}], "context_regex": re.compile(r"(?i)(interpro|domain|family|motif|accession)"), "context_window": 20000},

    # MetaboLights
    {"label": "metabolights", "id": "metabolights_1", "pattern": [{"TEXT": {"REGEX": r"^MTBLS[0-9]+$"}}], "context_regex": re.compile(r"(?i)(metabolights|accession|repository)"), "context_window": 20000},

    # PDB (Protein Data Bank)
    {"label": "pdb", "id": "pdb_1", "pattern": [{"TEXT": {"REGEX": r"^(?=.{4}$)(?=.*[A-Za-z])[1-9][A-Za-z0-9]{3}$"}}], "context_regex": re.compile(r"(?i)(\bpdb\b|protein data bank|structure|domain)"), "context_window": 200},

    # Pfam
    {"label": "pfam", "id": "pfam_1", "pattern": [{"TEXT": {"REGEX": r"(?i)^PF[0-9]{5}$"}}], "context_regex": re.compile(r"(?i)(pfam|domain|family|accession|motif)"), "context_window": 20000},

    # ProteomeXchange / PRIDE
    {"label": "pxd", "id": "pxd_1", "pattern": [{"TEXT": {"REGEX": r"^(?:R)?PXD[0-9]{6}$"}}], "context_regex": re.compile(r"(?i)(pxd|proteomexchange|pride|dataset|accession|repository)"), "context_window": 20000},

    # Reactome Pathways
    {"label": "reactome", "id": "reactome_1", "pattern": [{"TEXT": {"REGEX": r"^R-HSA-[0-9]+$"}}], "context_regex": re.compile(r"(?i)(biological|regulatory|pathway|pathways|database)"), "context_window": 20000},

    # Rfam
    {"label": "rfam", "id": "rfam_1", "pattern": [{"TEXT": {"REGEX": r"^RF[0-9]{5}$"}}], "context_regex": None, "context_window": 0},

    # Rhea Reactions
    {"label": "rhea", "id": "rhea_1", "pattern": [{"TEXT": {"REGEX": r"(?i)^RHEA:[1-9][0-9]+$"}}], "context_regex": re.compile(r"(?i)(reactions|database|rhea database|accession)"), "context_window": 20000},

    # RNAcentral
    {"label": "rnacentral", "id": "rnacentral_1", "pattern": [{"TEXT": {"REGEX": r"^URS[0-9A-F]{10}_[0-9]+$"}}], "context_regex": None, "context_window": 0},

    # UniProtKB
    {"label": "uniprot", "id": "uniprot_1", "pattern": [{"TEXT": {"REGEX": r"^(?:[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})(?:-\d+)?$"}}], "context_regex": re.compile(r"(?i)(\bswiss-prot\b|\bsprot\b|\buniprot\b|\bswiss prot\b|\baccession(s)?\b|\bLocus\b|\bGenBank\b|\bgenome\b|\bsequence(s)?\b|\bprotein\b|\btrembl\b|\buniparc\b|\buniprotkb\b|\bAcc\.?No\b)"), "context_window": 20000},

    # RefSeq
    {"label": "refseq", "id": "refseq_1", "pattern": [{"TEXT": {"REGEX": r"^(?:AC|AP|NC|NG|NM|NP|NR|NT|NW|NZ|XM|XP|XR|YP|ZP|NS)_[A-Z]{0,4}[0-9]{6,9}(?:\.[0-9]+)?$"}}], "context_regex": re.compile(r"(?i)(refseq|genbank|accession|sequence)"), "context_window": 20000},

    # RefSNP
    {"label": "refsnp", "id": "refsnp_1", "pattern": [{"TEXT": {"REGEX": r"^[rs]s[0-9]{2,9}$"}}], "context_regex": re.compile(r"(?i)(allele|polymorphism|variant|snp)"), "context_window": 20000},

    # DOI
    {"label": "doi", "id": "doi_1", "pattern": [{"TEXT": {"REGEX": r"^10\.[0-9]{4,}/[^ ()\"<>]+$"}}], "context_regex": re.compile(r"(?i)(doi|repository)"), "context_window": 20000},

    # BioProject
    {"label": "bioproject", "id": "bioproject_1", "pattern": [{"TEXT": {"REGEX": r"^PRJ(?:NA|EA|EB|DB)[0-9]+$"}}], "context_regex": re.compile(r"(?i)(bioproject|accession|archive)"), "context_window": 20000},

    # GCA
    {"label": "gca", "id": "gca_1", "pattern": [{"TEXT": {"REGEX": r"^GCA_[0-9]{9}(?:\.[0-9]+)?$"}}], "context_regex": None, "context_window": 0},

    # TreeFam
    {"label": "treefam", "id": "treefam_1", "pattern": [{"TEXT": {"REGEX": r"^TF[0-9]{6}$"}}], "context_regex": re.compile(r"(?i)(treefam|tree|family|accession|dendrogram)"), "context_window": 20000},

    # EudraCT
    {"label": "eudract", "id": "eudract_1", "pattern": [{"TEXT": {"REGEX": r"^[0-9]{4}-[0-9]{6}-[0-9]{2}$"}}], "context_regex": re.compile(r"(?i)(eudract|trial|agency|register|clinical)"), "context_window": 20000},

    # dbGaP
    {"label": "dbgap", "id": "dbgap_1", "pattern": [{"TEXT": {"REGEX": r"^phs[0-9]{6}$"}}], "context_regex": re.compile(r"(?i)(dbgap|accession|database of genotypes and phenotypes)"), "context_window": 20000},

    # ArrayExpress
    {"label": "arrayexpress", "id": "arrayexpress_1", "pattern": [{"TEXT": {"REGEX": r"^E-[A-Z]{4}-[0-9]+$"}}], "context_regex": re.compile(r"(?i)(arrayexpress|atlas|gxa|accession|experiment)"), "context_window": 20000},

    # BioModels
    {"label": "biomodels", "id": "biomodels_1", "pattern": [{"TEXT": {"REGEX": r"^(?:BIOMD|MODEL)[0-9]{10}$"}}], "context_regex": re.compile(r"(?i)(biomodels|accession|model|identifier)"), "context_window": 20000},

    # BioSample
    {"label": "biosample", "id": "biosample_1", "pattern": [{"TEXT": {"REGEX": r"^SAM[NED][A-Z]?[0-9]+$"}}], "context_regex": re.compile(r"(?i)(biosample|accession)"), "context_window": 20000},

    # Addgene Plasmid IDs
    {"label": "addgene", "id": "addgene_hash", "pattern": [{"LOWER": "addgene"}, {"TEXT": "#"}, {"LIKE_NUM": True}], "context_regex": None, "context_window": 0},
]
