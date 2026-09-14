# Widget Store Guide

How the widget store is used.

## Context
* [Widget Model](widget-model.md) - what a widget is

## Overview

See §1 for the interface. The [model's own §2.3](widget-model.md) belongs to another document;
[retry §1.1](widget-store-guide.md) and [retry again §1.1](./widget-store-guide.md) belong to this one.
The [published copy §2.1](https://docs.example.com/widget-store-guide) is not resolved at all.

## 1 Using The Store

### Context
* [Retry Policy](retry-policy.md) - when a caller should retry

The store accepts one widget per call. Version 1.4.2 is current.
Terms are defined in @magpieweaver-docs/docs/glossary.md/§4.

### Errors

What the store does when it will not accept a widget. The worked example in §Appendix.1 shows one.

### 1.1 Retry

Retrying is the caller's responsibility.

``` 1.1.a Retry Invocation
widget-store put --retries 3
```

# Appendix

## 1 Worked Example

A complete put-and-retry exchange.

## 2 Field Reference

Every field the store accepts.

# rationale

## 1 Why One Widget Per Call

Batching was considered and rejected.
