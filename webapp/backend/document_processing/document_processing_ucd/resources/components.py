import enum
from typing import List

from haystack.nodes import PreProcessor, FARMReader, TfidfRetriever
from dagster import resource, Enum


nltk.download('punkt')


class SplitBy(Enum):
    word = "word"
    sentence = "sentence"
    passage = "passage"

@resource(
    config_schema={
        "preprocessor_init_args": {
            "clean_header_footer": bool,
            "clean_whitespace": bool,
            "clean_empty_lines": bool,
            "remove_substrings": bool,
            "split_by": Field(Enum.from_python_enum(SplitBy)),
            "split_length": int,
            "split_overlap": int,
            "split_respect_sentence_boundary": bool
        }
    }
)
def preprocessor(init_context):
    # TODO: select different preprocessors
    preprocessor = PreProcessor(**init_context.resource_config['preprocessor_init_args'])

    return preprocessor


@resource(
    config_schema={
        model_name=str,
        use_gpu=bool
    },
)
def reader(init_context):

    model_name = init_context.resource_config['model_name']
    use_gpu = init_context.resource_config['use_gpu']
    # TODO: make reader selectable
    reader = FARMReader(model_name_or_path=model_name, use_gpu=use_gpu)

    return reader

@resource(
    required_resource_keys={"document_store"}
)
def retriever(init_context):
    document_store = init_context.resources.document_store

    # TODO: make retriever selectable
    retriever = TfidfRetriever(document_store=document_store)

    return retriever
