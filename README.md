# FileMerger

**FileMerger** is a developer-focused CLI tool that consolidates project files into a
single plain-text output.

It is designed to help developers:

- Share complete code context with AI tools (ChatGPT, Gemini, Grok, Claude, etc.)
- Review large codebases
- Create audit or snapshot files
- Prepare structured input for analysis
- Generate structured multi-file context for LLM systems

---

# Installation

FileMerger is available on PyPI as:

```

filemerger-cli

````

Install with:

```bash
pip install filemerger-cli
````

---

# Basic Usage

Merge a directory:

```bash
filemerger src/
```

Specify output file:

```bash
filemerger src/ --output context.txt
```

Dry run (no file written):

```bash
filemerger . --dry-run
```

---

# Output Modes

FileMerger supports multiple output modes depending on **who (or what)** will consume the output.

---

## 1. Default Mode (Human Readable)

```bash
filemerger src/
```

Use when:

* You want to review code manually
* You are auditing a repository
* You want structured readable output

Characteristics:

* File headers
* Visual separators
* Structured readable layout

---

## 2. LLM Mode

```bash
filemerger src/ --llm
```

Use when:

* Output is intended for an AI model
* Deterministic file ordering is required
* Reduced formatting noise is preferred

Characteristics:

* Files numbered sequentially
* Minimal formatting
* Predictable structure

Example:

```
[1] path/to/file.py
<content>

[2] another/file.js
<content>
```

---

## 3. LLM Compact Mode

```bash
filemerger src/ --llm-compact
```

Use when:

* Token limits are tight
* Projects are large
* Maximum efficiency is required

Characteristics:

* Same structure as `--llm`
* Fewer blank lines
* Reduced output size

---

## 4. AI Marker Mode

```bash
filemerger src/ --ai-markers
```

Designed for deterministic multi-file AI ingestion.

Characteristics:

* Explicit file boundary markers
* Strong machine-readable structure
* Reliable AI context separation

Example:

```
<<<FILE 1: path/to/file.py>>>
<content>
<<<END FILE>>>

<<<FILE 2: another/file.js>>>
<content>
<<<END FILE>>>
```

---

# Statistics

Display merge statistics:

```bash
filemerger src/ --stats
```

Reports:

* Total files
* Total lines
* Total bytes
* Skipped files (binary / non-UTF8)

---

# Runtime Configuration Overrides (v0.3.2)

FileMerger supports **temporary runtime overrides** for configuration using CLI arguments.

This allows flexible usage without modifying `.filemerger.toml` or library defaults.

Configuration precedence:

```
CLI arguments
→ .filemerger.toml
→ config.py defaults
```

---

## Allow Excluded Directories

Allow directories normally excluded by default configuration.

Example:

```bash
filemerger . --allow-dir migrations
```

Multiple directories:

```bash
filemerger . --allow-dir migrations,tests
```

---

## Allow Excluded Files

Allow files normally excluded.

Example:

```bash
filemerger . --allow-file .DS_Store
```

---

## Extend Allowed File Extensions

Add additional file extensions.

Example:

```bash
filemerger . --allow-ext .yaml,.yml
```

---

## Override Maximum File Size

Default maximum file size is **2MB**.

Override temporarily:

```bash
filemerger . --max-size 5
```

---

## Override Separator Length

Customize output separator length.

Example:

```bash
filemerger . --separator 40
```

---

## Combined Example

```bash
filemerger . \
  --allow-dir migrations,tests \
  --allow-ext .yaml \
  --allow-file .DS_Store \
  --max-size 5 \
  --separator 40
```

---

# Configuration (Optional)

FileMerger supports an optional configuration file:

```
.filemerger.toml
```

Example:

```toml
[filters]
max_file_size_mb = 1
exclude_dirs = ["tests"]

[output]
separator_length = 60
```

If the file is not present, default behavior is used.

---

# Design Goals

FileMerger is designed with the following principles:

* Deterministic output
* Minimal configuration
* AI-friendly formatting
* Predictable file ordering
* Zero project mutation

---

# License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.
