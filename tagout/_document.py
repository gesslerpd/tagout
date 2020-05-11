"""Document writer."""

import contextlib

from ._utils import escape_text


class Document:
    """Document writer.
    
    :param stream: writable stream
    :type stream: file-like object
    
    :param self_closing: enable self closing tag output
    :type self_closing: bool

    """

    def __init__(self, stream, self_closing=False):
        self.stream = stream
        self._depth = 0
        self.indent = '  '
        self._tag = False
        self.self_closing = self_closing

    @contextlib.contextmanager
    def tag(self, tag_name, **attributes):
        """Write tag.

        :param tag_name: tag name
        :type tag_name: str

        :param attributes:
            any extra keyword arguments become escaped tag attribute values
            (the leading underscore is removed)
        :type attributes: dict

        """
        for attr in list(attributes):
            if attr.startswith('_'):
                attributes[attr[1:]] = attributes[attr]
                del attributes[attr]
        if attributes:
            attrs = ' ' + ' '.join(
                f'{attr}' if value is None else f'{attr}="{escape_text(value)}"'
                for attr, value in attributes.items()
            )
        else:
            attrs = ''
        indent = '\n' + (self.indent * self._depth)
        self.stream.write(f'{indent}<{tag_name}{attrs}>')
        self._depth += 1
        begin_tag_position = self.stream.tell()
        yield
        end_tag_position = self.stream.tell()
        self._depth -= 1
        if self.self_closing and end_tag_position == begin_tag_position:
            self.stream.seek(begin_tag_position - 1)
            self.stream.write(' />')
        else:
            prefix = indent if self._tag else ''
            self.stream.write(f'{prefix}</{tag_name}>')
        self._tag = True
        if not self._depth:
            self.stream.write('\n')

    def text(self, text):
        """Write text.

        This text is written to the document after being escaped.

        :param text: text to write
        :type text: str

        """
        self.write(escape_text(text))

    def write(self, data):
        """Write data.

        This data is written to the document without any transformations.

        :param data: data to write
        :type data: str

        """
        lines = data.splitlines()
        if len(lines) > 1:
            indent = '\n' + (self.indent * self._depth)
            suffix = '\n' + (self.indent * (self._depth - 1))
            self.stream.write(indent + indent.join(lines) + suffix)
        else:
            self.stream.write(data)
        self._tag = False
