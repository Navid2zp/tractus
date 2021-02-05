# tractus

Trace HTTP requests and gather performance metrics.

### Install

```
pip install tractus
```

### Usage

```python

from tractus import Tracer

result = Tracer('https://google.com').trace()

print(f'Host IP: {result.ip}')
print(f'Status code: {result.status_code}')
print(f'DNS time: {result.dns:.2f} ms')
print(f'Handshake time: {result.handshake:.2f} ms')
print(f'First byte time: {result.first_byte:.2f} ms')
print(f'Full body time: {result.full_data:.2f} ms')
print(f'Body length: {result.data_length} bytes')
print(f'Headers length: {result.headers_length} bytes')

```

#### Helpers:
```python
# Get result as json
result.as_json()
# Get result as dict
result.as_dict()
```

License
----
MIT

#### Name
https://en.wiktionary.org/wiki/tractus