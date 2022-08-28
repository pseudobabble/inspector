from dagster import graph, op

from ops.documents import (
    get_file_keys,
    get_target_file_key,
    get_original_file_extension,
    get_file_from_document_store,
    put_file_to_document_store,
    convert_with_tika
)

@graph
def convert_file_to_text(file_key: str):
    target_key = get_target_file_key(file_key)
    original_file_extension = get_original_file_extension(file_key)

    file_content = get_file_from_document_store(file_key)
    file_text = convert_with_tika(file_content, original_file_extension)
    response = put_file_to_document_store(target_key, file_text)

    # TODO: check response code
    return file_text


@graph
def convert_files_to_text():
    responses = get_file_keys().map(convert_file_to_text)
    responses = responses.collect()
