# Retry Policy

## Context
* nothing external needed for this fixture

## 1 When To Retry

A call that failed for a reason that may not recur is worth retrying.

## 2 How Many Times

Three attempts, then stop. Registered before this run, and unchanged since, the same as `doc-a.md`.
