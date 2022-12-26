## spoor

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

* [ ] Add datadog exporter
* [x] Add group methods by class option
* [ ] Add tracking by import path
* [x] Add `most_common` method for statistics
* [ ] Add mkdocs / readthedocs with examples
* [ ] Add http exporter
