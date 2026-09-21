# Cache Tuning

## Context
* [Cache Eviction Policy](../policies/eviction-policy.md) - the eviction behaviour tuning works against

## 1 What To Measure

Hit rate, eviction rate, and the age of the oldest surviving entry. The three together say whether a cache is
too small, too large, or the wrong shape.

## 2 Sizing

A cache is big enough when its eviction rate under normal traffic is near zero and its hit rate is stable.

TODO: name the eviction rate that counts as "near zero" once we have a month of production figures.

## 3 When Tuning Will Not Help

A cache whose keys are almost never asked for twice cannot be tuned into usefulness. Remove it instead.

# Rationale

**Why eviction rate rather than eviction count.** An eviction policy says what goes, never how often; a count
rises with traffic whether or not the cache is behaving worse, so a count cannot be compared between two
weeks. A rate can, and a rate is what shows thrashing.

**Why the oldest surviving entry and not the average age.** An average hides the case this measure exists to
catch, which is a cache evicting so fast that nothing lives long enough to be hit twice.

# Appendix A: Worked Sizing Example

A cache serving 400 reads a second at a 90% hit rate, under an eviction policy of least-recently-used and a
retention of one hour, needs room for one hour of distinct keys. Size it below that and it is thrashing.
