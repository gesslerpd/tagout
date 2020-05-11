# tagout

A small, pythonic, HTML/XML writer.

## Installation

```
$ pip install tagout
```

## Usage

This example shows how to use component functions to easily compose a document.

```python
import contextlib
import sys
import io

from tagout import Document, class_names


@contextlib.contextmanager
def layout(doc):
    """Site layout component that allows transclusion of content."""
    doc.write('<!DOCTYPE html>')
    with doc.tag('html', lang='en'):
        with doc.tag('head'):
            with doc.tag('meta', charset='utf-8'):
                pass
            with doc.tag('meta', name='viewport', content='width=device-width, initial-scale=1, shrink-to-fit=no'):
                pass
            with doc.tag(
                'link',
                rel='stylesheet',
                href='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
                integrity='sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
                crossorigin='anonymous'
            ):
                pass
            with doc.tag('title'):
                doc.text('tagout')
        with doc.tag('body'):
            with doc.tag('div', _class='container'):
                # transclude content
                yield


def module_component(doc, module):
    """Site module name list item component."""
    is_private = module.startswith('_')
    # the `class_names` utility function can be used to conditionally add class names
    with doc.tag('li', _class=class_names({'text-danger': is_private})):
        doc.text(module)


def write_doc(stream):
    doc = Document(stream, self_closing=True)
    with layout(doc):
        # the layout component is a context manager and allows for transclusion

        # the leading underscore will be removed from keyword attributes
        # this is useful for the `class` attribute since it happens to be a python keyword  
        with doc.tag('h1', _class='text-primary'):
            doc.text('<tagout>')

        with doc.tag('p'):
            doc.text('A small, pythonic, HTML/XML writer.')

        with doc.tag('h2'):
            doc.text('Modules')
    
        with doc.tag('ul'):
            # loops can be used to generate multiple components
            for module in sys.modules:
                # the module component takes in data
                module_component(doc, module)


if __name__ == '__main__':
    # the document can be written to a file-like object
    with open('index.html', 'w') as output_file:
        write_doc(output_file)

    # the document can be written to an io.StringIO instance to get a string
    output_string = io.StringIO()
    write_doc(output_string)
    print(output_string.getvalue())

```
