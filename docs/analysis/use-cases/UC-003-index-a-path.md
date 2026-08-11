# UC-003 — Index A Path

//TODO - Elicit and write this use case (WVR-89): the tool that indexes a
given path (a single doc, or a directory) — producing `.index/<slug>.sections.yaml`
(section/code-block structure: title-keyed, optional number, type,
start_line, end_line) and `.index/<slug>.words.yaml` (significant words per
section, same title-keyed scheme) together, since both are driven by the
same trigger (the subject document(s) changed) and were previously an
artificial split between two use cases (formerly UC-003 and UC-004 — see
[UC-004](UC-004-index-document-words.md)).
