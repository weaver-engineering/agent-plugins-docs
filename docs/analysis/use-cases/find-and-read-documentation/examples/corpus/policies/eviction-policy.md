# Cache Eviction Policy

## Context
* [Retention Policy](retention-policy.md) - what may be kept, and for how long
* [Eviction Procedures](../procedures/eviction-procedures.md) - how this policy is carried out

## 1 Scope

This policy governs every cache the platform operates. A cache holds a copy of something that is authoritative
elsewhere, so evicting from a cache loses nothing that cannot be fetched again.

## 2 When An Entry Is Evicted

An entry is evicted when the cache is full and a new entry needs its space, or when the entry has outlived the
retention its data class allows.

### 2.1 Pressure Eviction

Under pressure the least recently used entry is evicted first. The policy takes no view on how recency is
measured, only that the measure is the same for every entry in one cache.

### 2.2 Age Eviction

An entry older than its retention is evicted whether or not the cache is under pressure, because stale data is
worse than absent data.

## 3 What Is Never Evicted

An entry still being written is never evicted. An entry pinned by an operator is never evicted while the pin
stands.
