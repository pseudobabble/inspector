from dagster import graph

from ops.documents import get_file_keys, get_file_from_document_store, put_file_to_document_store, convert_with_tika

@graph
def convert_file_to_text(file_key: str):
    file_content = get_file_from_document_store(file_key)
    file_text = convert_with_tika(file_content)
    response = put_file_to_document_store(file_key)


@graph
def convert_files_to_text():
    keys = get_file_keys()
    responses = keys.map(convert_file_to_text)
    return responses.collect()
