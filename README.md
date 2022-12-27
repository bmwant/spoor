## spoor

![Tests](https://github.com/bmwant/spoor/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/spoor)](https://pypi.org/project/spoor/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spoor)


[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![EditorConfig](https://img.shields.io/badge/-EditorConfig-grey?logo=editorconfig)](https://editorconfig.org/)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)


```bash
$ pip install spoor
```

### Usage

```python
from spoor import Spoor

s = Spoor()

@s.track
def function(a: int, b: int):
  return a + b

func(5, 10)
func(23, 42)

assert s.called(func)
assert s.call_count(func) == 2
```

### Configuration

| Option | Type | Default |
|--------|------|---------|
| attach | `bool` | `False` |
|`distinct_instances` | `bool` | `False` |
| `disabled` | `bool` | `False` |


### Exporters

* [statsd]()
* [DataDog]()

### TODO:

* [x] Add datadog exporter
* [x] Add group methods by class option
* [ ] Add tracking by import path
* [x] Add `most_common` method for statistics
* [ ] Add mkdocs / readthedocs with examples
