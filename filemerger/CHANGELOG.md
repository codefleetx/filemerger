# Changelog

All notable changes to **FileMerger** are documented in this file.

The format loosely follows **Keep a Changelog** principles.

---

# v0.3.2 — Runtime CLI Configuration Overrides

## Added

### Runtime Configuration Overrides

Temporary behavior changes can now be applied directly via the CLI without modifying configuration files.

**New CLI Options**

```
--allow-dir
--allow-file
--allow-ext
--max-size
--separator
```

**Capabilities Introduced**

* Allow normally excluded directories
* Allow normally excluded filenames
* Extend allowed file extensions
* Override maximum file size limit
* Override output separator length

---

## Improvements

* CLI help text expanded for runtime configuration
* Filtering logic refactored to support runtime overrides
* Improved developer flexibility for debugging and analysis workflows

---

## Configuration Precedence

Configuration values are resolved in the following order:

```
CLI arguments
→ .filemerger.toml
→ config.py defaults
```

**Note:** CLI overrides always take precedence.

---

# v0.3.1 — AI Marker Mode

## Added

### `--ai-markers`

An explicit **AI-native file boundary format** designed for deterministic AI ingestion.

**Example**

```
<<<FILE 1: path/to/file.py>>>
<content>
<<<END FILE>>>
```

**Use Cases**

* LLM multi-file reasoning
* Deterministic AI parsing
* Large AI context ingestion

---

# v0.3.0

## Added

### LLM Output Modes

```
--llm
--llm-compact
```

Provides optimized output formatting specifically designed for AI systems.

---

### Configuration File

Optional configuration file support via:

```
.filemerger.toml
```

Allows customization of:

* Excluded directories
* Maximum file size
* Output separator length

---

### Statistics

```
--stats
```

Displays merge statistics including:

* File count
* Total lines
* Total bytes
* Skipped files

---

# v0.2.x

## Improvements

* Respect `.gitignore` when collecting files
* Improved filtering behavior
* More predictable file traversal

---

# v0.1.0

## Initial Release

### Core Functionality

* Merge project files into a single text output
* Default readable output format
* Directory traversal and filtering
* File extension filtering
* UTF-8 safety handling

---

✅ Improvements made:

* Consistent headings
* Clearer section hierarchy
* Better spacing
* Standardized bullet lists
* Better CLI option formatting
* More readable code blocks

---