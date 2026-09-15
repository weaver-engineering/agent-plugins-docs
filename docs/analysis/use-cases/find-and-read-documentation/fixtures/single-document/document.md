# Retry Policy

## Context
* nothing outside this document is needed to read it

## 1 When To Retry

A call that failed for a reason that may not recur is worth retrying. A call that failed because it was wrong
is not.

## 2 How Many Times

Three attempts, then stop and report.

### 2.1 Backoff

Wait longer between each attempt than the last, so a struggling service is not made worse by the retrying.

## 3 What To Report

The last failure, and how many attempts were made before it.
