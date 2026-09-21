# Eviction Procedures

## Context
* [Cache Eviction Policy](../policies/eviction-policy.md) - the policy these procedures carry out

## 1 Before You Start

Check that the cache you are about to operate on is the one named in the ticket. Eviction is not reversible
from the cache's own side.

## 2 Policies In Force

Each cache runs under one eviction policy, named in its configuration.

### 2.1 Cache Eviction

To evict by hand, name the cache and the key. The entry is removed and the next read fetches it again from the
authoritative store.

### 2.2 Bulk Eviction

Evicting a whole prefix is the same operation repeated. Do it in batches, so a cache serving traffic is not
emptied faster than the store behind it can refill.

## 3 After Eviction

Watch the hit rate for one full traffic cycle. A hit rate that does not recover means the eviction removed
entries that were still being asked for.
