## spoor

![Tests](https://github.com/bmwant/spoor/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/spoor)](https://pypi.org/project/spoor/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spoor)


[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![EditorConfig](https://img.shields.io/badge/-EditorConfig-grey?logo=editorconfig)](https://editorconfig.org/)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)


Track invocation of your functions and methods; display collected statistics for the invocations; export data gathered to external services.

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

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `attach` | `bool` | `False` | Expose `called`/`call_count` attributes directly on a function/method object. |
|`distinct_instances` | `bool` | `False` | Separate metrics collection for each instance of a class. Has no effect if tracking only functions. |
|`skip_dunder` | `bool` | `True` | Do not track double underscore method calls (like `__str__`) for class instances. Has no effect if tracking only functions. |
| `disabled` | `bool` | `False` | Initialize as inactive and ignore metrics collection until enabled explicitly. Can be controlled via `enable()`/`disable()` methods later. |


### Exporters

* [statsd]()
* [DataDog]()

### See also

* 🍒 [podmena](https://github.com/bmwant/podmena) for nice commits emoji
* 🌈 [rich](https://github.com/Textualize/rich) for beautiful terminal output
* 🇺🇦 [United 24](https://u24.gov.ua/) to support Ukraine in the war
