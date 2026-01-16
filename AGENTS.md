# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Galaxy bioinformatics tool wrappers for **Short Tandem Repeat (STR) analysis**. Each tool has its own directory containing:
- `{tool}.xml` - Galaxy tool wrapper
- `docker/Dockerfile` - Container image
- `tool_conf.xml` - Tool section configuration

**Current tools**: STRling, GangSTR, ExpansionHunter, ExpansionHunter Denovo, haplogrep3, mitoz, mutserve

## Development Commands

```bash
# Lint Galaxy XML wrapper
planemo lint ./strling/strling.xml

# Test with Galaxy
planemo test --galaxy_root=/path/to/galaxy ./strling/strling.xml

# Validate XML syntax
xmllint --noout ./strling/strling.xml

# Build Docker image
docker build -t strling:0.6.0 ./strling/docker/
```

## Galaxy XML Patterns

**Version tokens in macros**:
```xml
<macros>
    <token name="@TOOL_VERSION@">0.6.0</token>
    <token name="@VERSION_SUFFIX@">+galaxy0</token>
</macros>
```

**BAM/CRAM input handling**:
```cheetah
#if $reads.is_of_type('bam')
    ln -s '$reads' input.bam &&
    ln -s '$reads.metadata.bam_index' input.bam.bai &&
#else
    ln -s '$reads' input.cram &&
    ln -s '$reads.metadata.cram_index' input.cram.crai &&
#end if
```

**Conditional parameters**:
```cheetah
#if str($advanced.min_support) != ''
    --min-support $advanced.min_support
#end if
```

## Dockerfile Conventions

- Use `--platform=linux/amd64` for bioconda packages
- Install via conda with `bioconda` and `conda-forge` channels
- Clean cache with `conda clean -afy`
- Verify installation with `--help` or `--version`

## Key Conventions

- Help content in Chinese
- 4-space indentation, no tabs
- `<command>` and `<help>` wrapped in `<![CDATA[]]>`
- Tool version in format `X.Y.Z+galaxy0`
- Output parameter names prefixed with `output_`

## Git Commit Style

```
feat: Add {ToolName} galaxy wrapper support
fix: Fix {ToolName} parameter handling
docs: Update {ToolName} help documentation
```

## References

- [Galaxy Tool XML Schema](https://docs.galaxyproject.org/en/latest/dev/schema.html)
- [Planemo](https://planemo.readthedocs.io/)
- [Galaxy IUC Standards](https://galaxy-iuc-standards.readthedocs.io/)
