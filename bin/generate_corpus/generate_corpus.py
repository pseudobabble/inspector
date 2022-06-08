#!/usr/bin/env python
import aspose.words as aw
import requests
import os, sys


def build_doc(text: str, filename: str) -> None:
    doc = aw.Document()

    builder = aw.DocumentBuilder(doc)
    builder.write(text)

    doc.save(f"{filename}.docx")

def main(*args):
    for i in range(*args):
        url = f"https://www.rfc-editor.org/rfc/rfc{i}.txt"
        try:
            response = requests.get(url)
            if not 200 <= response.status_code < 300:
                raise ValueError(f"RFC {i}: got non 2XX response code {response.status_code}")

            build_doc(response.text, f"rfc_{i}")
            message = """
SUCCESSFULLY GENERATED RFC
==========================

""" + os.getcwd() + f"rfc_{i}.docx" + """

==========================
"""
        except Exception as e:
            message = """
ENCOUNTERED ERROR - DETAILS BELOW
=================================

""" + f"{e}" + """

=================================

""" + f"{url}" + """

=================================
"""
        print(message)


if __name__ == "__main__":
    main(*[int(arg) for arg in sys.argv[1:]])
