import contextlib
from io import StringIO
from xml.etree import ElementTree

import pytest

from tagout import Document


@contextlib.contextmanager
def transclude(doc):
    # transclude components
    with doc.tag('html', lang='en'):
        with doc.tag('head'):
            with doc.tag('title'):
                doc.text('Sample Site')
        with doc.tag('body'):
            yield


def component(doc, data):
    # pass in data to components
    with doc.tag('li'):
        doc.text(f'"{data}"')


def write_doc(stream, self_closing):
    doc = Document(stream, self_closing)

    with transclude(doc):
        with doc.tag('h1', id='header', _class='"escaped"'):
            doc.text('Sample Header')
        with doc.tag('img'):
            pass
        with doc.tag('ul'):
            for i in range(10):
                component(doc, i)


EXPECTED = {
    'tag': 'html',
    'attrib': {'lang': 'en'},
    'text': '',
    'children': [
        {
            'tag': 'head',
            'attrib': {},
            'text': '',
            'children': [
                {
                    'tag': 'title',
                    'attrib': {},
                    'text': 'Sample Site',
                    'children': [],
                },
            ]
        },
        {
            'tag': 'body',
            'attrib': {},
            'text': '',
            'children': [
                {
                    'tag': 'h1',
                    'attrib': {'class': '"escaped"', 'id': 'header'},
                    'text': 'Sample Header',
                    'children': [],
                },
                {
                    'tag': 'img',
                    'attrib': {},
                    'text': '',
                    'children': [],
                },
                {
                    'tag': 'ul',
                    'attrib': {},
                    'text': '',
                    'children': [
                        {
                            'tag': 'li',
                            'attrib': {},
                            'text': f'"{i}"',
                            'children': []
                        }
                        for i in range(10)
                    ],
                },
            ],
        },
    ],
}


def tree_to_dict(tree):
    text = tree.text

    if text:
        text = text.strip()
    else:
        text = ''

    return {
        'tag': tree.tag,
        'attrib': tree.attrib,
        'text': text,
        'children': [tree_to_dict(child) for child in tree],
    }


@pytest.mark.parametrize('self_closing', (
    True,
    False,
))
def test_doc(self_closing):
    stream = StringIO()
    write_doc(stream, self_closing)

    root = ElementTree.fromstring(stream.getvalue())

    assert tree_to_dict(root) == EXPECTED
