import sys
import os
import pytest

from filter_plugins.generate_all_domains import FilterModule

@pytest.fixture
def generate_filter():
    """
    Fixture to return the generate_all_domains filter function.
    """
    fm = FilterModule()
    return fm.generate_all_domains

def test_simple_string_values(generate_filter):
    domains = {'app': 'example.com'}
    result = generate_filter(domains)
    # Expect original and www-prefixed, deduped and sorted
    expected = ['example.com', 'www.example.com']
    assert result == expected

def test_list_and_dict_values(generate_filter):
    domains = {
        'app1': ['one.com', 'two.com'],
        'app2': {'x': 'x.com', 'y': 'y.com'}
    }
    result = generate_filter(domains)
    expected = sorted([
        'one.com', 'two.com', 'x.com', 'y.com',
        'www.one.com', 'www.two.com', 'www.x.com', 'www.y.com'
    ])
    assert result == expected

def test_include_www_false(generate_filter):
    domains = {'app': 'no-www.com'}
    result = generate_filter(domains, include_www=False)
    # Only the original domain
    assert result == ['no-www.com']

def test_deduplicate_and_sort(generate_filter):
    domains = {
        'a': 'dup.com',
        'b': 'dup.com',
        'c': ['b.com', 'a.com'],
    }
    result = generate_filter(domains)
    # Should contain unique domains sorted alphabetically
    expected = ['a.com', 'b.com', 'dup.com', 'www.a.com', 'www.b.com', 'www.dup.com']
    assert result == expected

if __name__ == '__main__':
    pytest.main()
