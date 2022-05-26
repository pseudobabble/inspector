#!/usr/bin/env python3
from pprint import pprint

from haystack.nodes.extractor.entity import simplify_ner_for_qa
from haystack.nodes import EntityExtractor

entity_extractor = EntityExtractor(model_name_or_path="dslim/bert-base-NER")

with open('./test-files/Biodiversity Footprint_Report_IEEP.txt', 'r') as f:
    text = f.read()


entities = entity_extractor.extract(text=text)

pprint((entities))
