# tractus

<p align="center">
  <img alt="License" src="https://img.shields.io/github/license/navid2zp/tractus?style=flat-square" />
  <img alt="Github Workflow" src="https://img.shields.io/github/workflow/status/navid2zp/tractus/tractus/main?style=flat-square" />
  <img alt="Python verions" src="https://img.shields.io/pypi/pyversions/tractus?style=flat-square" />
  <img alt="Format" src="https://img.shields.io/pypi/format/tractus?style=flat-square" />
  <img alt="Implementation" src="https://img.shields.io/pypi/implementation/tractus?style=flat-square" />
  <img alt="Version" src="https://img.shields.io/pypi/v/tractus?style=flat-square" />
  <img alt="Quality" src="https://img.shields.io/lgtm/grade/python/github/Navid2zp/tractus?style=flat-square" />
</p>

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
print(f'DNS time: {result.dns} ms')
print(f'Handshake time: {result.handshake} ms')
print(f'First byte time: {result.first_byte} ms')
print(f'Full body time: {result.full_data} ms')
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
