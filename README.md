# Galaxy Missed Bioinformatics Softwares

[![Galaxy Tool Wrapper](https://img.shields.io/badge/Galaxy-Wrapper-blue)](https://docs.galaxyproject.org/)
[![Tool Shed](https://img.shields.io/badge/Galaxy-Toolshed-orange)](https://toolshed.g2.bx.psu.edu/)

This project provides Galaxy tool wrappers and Docker container images for **bioinformatics software that is not available in the Galaxy Tool Shed**, enabling easy integration into Galaxy for scientific research.

## Overview

Many valuable bioinformatics tools exist but have not been integrated into Galaxy's official [Tool Shed](https://toolshed.g2.bx.psu.edu/). This project bridges that gap by creating complete Galaxy integrations for these missing tools, including:

- **Galaxy XML wrappers** conforming to the Galaxy Tool XML Schema
- **Docker container images** for reproducible deployments
- **Configuration files** for seamless Galaxy integration

## Supported Tools

| Tool | Description | Version |
|------|-------------|---------|
| [STRling](./strling/) | STR expansion detection using k-mer counting | 0.6.0 |
| [GangSTR](./gangstr/) | Genome-wide STR genotyping from short reads | 2.5.0 |
| [ExpansionHunter](./expansionhunter/) | STR genotyping using repeat-specific graphs | 5.0.0 |
| [ExpansionHunter Denovo](./expansionhunter_denovo/) | STR expansion detection without prior loci | 0.9.0 |
| [haplogrep3](./haplogrep3/) | Haplogroup classification for mtDNA | 3.2.2 |
| [MitoZ](./mitoz/) | Mitochondrial genome assembly and annotation | 3.6 |
| [MutServe](./mutserve/) | mtDNA mutation detection from NGS data | 2.0.0-rc15 |

## Quick Start

### Lint Galaxy Wrapper

```bash
# Install planemo
pip install planemo

# Validate wrapper syntax
planemo lint ./strling/strling.xml
```

### Build Docker Image

```bash
cd strling/docker
docker build -t strling:0.6.0 --platform=linux/amd64 .
```

### Test with Galaxy

```bash
planemo test --galaxy_root=/path/to/galaxy ./strling/strling.xml
```

## Integration into Galaxy

### 1. Copy Tool Files

Copy the tool directory to your Galaxy's `tools/` folder:

```bash
cp -r strling /path/to/galaxy/tools/
```

### 2. Update Configuration

Add to `config/local_tool_conf.xml`:

```xml
<section id="str" name="Short Tandem Repeat">
    <tool file="strling/strling.xml"/>
</section>
```

### 3. Configure Job Execution

Update `config/job_conf.xml` to assign the tool to a destination:

```xml
<dest id="docker_local">
    <param id="docker_enabled">true</param>
    <param id="docker_image">strling:0.6.0</param>
</dest>
```

### 4. Restart Galaxy

```bash
# If using systemd
sudo systemctl restart galaxy

# Or using supervisor
sudo supervisorctl restart galaxy:*

# Or manually (if running in foreground)
# Press Ctrl+C to stop, then restart the server
```

## Why This Project?

### Galaxy Tool Shed Limitations

While the Galaxy Tool Shed hosts thousands of tools, many are:

- Outdated or unmaintained
- Missing from official repositories
- Difficult to install due to complex dependencies

### Our Solution

This project provides:

1. **Up-to-date wrappers** - Latest tool versions with proper Galaxy integration
2. **Containerized deployment** - Docker images eliminate dependency issues
3. **Best practice parameters** - Parameters validated through literature review
4. **Easy deployment** - Drop-in integration for existing Galaxy instances

## For Tool Developers

To add a new tool to this project:

1. Create a new directory named after the tool
2. Develop the Galaxy XML wrapper following existing patterns
3. Create a Dockerfile in `docker/` directory
4. Add `tool_conf.xml` for tool section configuration
5. Write documentation in both English and Chinese
6. Validate with `planemo lint`

## Contributing

Contributions are welcome! Please ensure:

- Follow Galaxy IUC standards
- Include Docker containerization
- Provide bilingual documentation
- Test with planemo before submitting

## Resources

- [Galaxy Tool XML Schema](https://docs.galaxyproject.org/en/latest/dev/schema.html)
- [Planemo Documentation](https://planemo.readthedocs.io/)
- [Galaxy IUC Standards](https://galaxy-iuc-standards.readthedocs.io/)
- [Official Tool Shed](https://toolshed.g2.bx.psu.edu/)

## License

This project is licensed under the MIT License. Each individual tool follows its respective license as specified in its directory.

---

**Note**: This is an independent project and is not affiliated with the Galaxy Project or the Galaxy Tool Shed. Tools are provided for integration convenience.
