# YARA-X Rule Quality

Require:

- current YARA-X syntax and exact tested version;
- a narrow detection objective;
- provenance for every decisive feature;
- at least one positive and meaningful benign negative fixture;
- format/size guards where relevant;
- expected undefined-module behavior;
- regression results and known limits.

Treat packed, encrypted, truncated, universal, nested, and script/document variants as separate coverage questions. A rule matching one sample does not establish family coverage.

Use the current [YARA-X documentation](https://virustotal.github.io/yara-x/docs/) and migration guidance. Original YARA compatibility is high but not absolute.
