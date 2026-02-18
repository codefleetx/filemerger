# FileMerger

**FileMerger** is a developer-focused CLI tool that consolidates project files into a
single plain-text output.

It is designed to help developers:
- Share complete code context with AI tools (ChatGPT, Gemini, Grok, Claude, etc.)
- Review large codebases
- Create audit or snapshot files
- Prepare structured input for analysis

---

## Installation

```bash
pip install filemerger-cli
```

---

## Basic Usage

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

## Output Modes

FileMerger supports multiple output modes depending on **who (or what)** will consume the output.

### 1. Default Mode (Human-Readable)

```bash
filemerger src/
```

**Use this when:**

* You want to read the output yourself
* You are reviewing or auditing code
* You want clear visual separation

**Characteristics:**

* File lists and headers
* Visual separators
* Structured, readable layout

---

### 2. LLM Mode (`--llm`)

```bash
filemerger src/ --llm
```

**Use this when:**

* The output will be pasted into an AI system
* You want deterministic file references
* You want to reduce semantic noise

**Characteristics:**

* Files are numbered (`[1]`, `[2]`, …)
* No decorative separators
* Simple, predictable structure

Example:

```
[1] path/to/file.py
<content>

[2] another/file.js
<content>
```

---

### 3. LLM Compact Mode (`--llm-compact`)

```bash
filemerger src/ --llm-compact
```

**Use this when:**

* Token limits are tight
* The project is very large
* Maximum efficiency matters

**Characteristics:**

* Same structure as `--llm`
* Fewer blank lines
* Minimal formatting overhead

---

### 4.  Statistics

Use `--stats` to print merge statistics:

```bash
filemerger src/ --stats
```

Reported values:

* Number of files
* Total lines
* Total bytes
* Skipped files (binary / non-UTF8)

---

### 5. AI Marker Mode (`--ai-markers`)

```bash
filemerger src/ --ai-markers
````

**Use this when:**

* You need strong, explicit file boundaries for AI systems
* You want deterministic multi-file reasoning
* You are feeding large structured context into LLMs
* You need machine-parsable output

**Characteristics:**

* Explicit file boundary markers
* Clear begin/end delimiters
* Unambiguous separation between files
* Designed for reliable AI ingestion

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


## Configuration (Optional)

FileMerger supports an optional `.filemerger.toml` file in the project root.

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

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
