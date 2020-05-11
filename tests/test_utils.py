import pytest

from tagout import class_names


@pytest.mark.parametrize('obj', (
    ('class1', 'class2'),
    ['class1', 'class2'],
    ['class1    ', '     class2      \n'],
    {'class1': True, 'class2': 1, 'class3': None, 'class4': False},
))
def test_class_names(obj):
    assert class_names(obj) == 'class1 class2'
