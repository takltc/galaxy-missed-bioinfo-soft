# Galaxy 缺失的生物信息学软件

[![Galaxy 工具包装器](https://img.shields.io/badge/Galaxy-Wrapper-blue)](https://docs.galaxyproject.org/)
[![Tool Shed](https://img.shields.io/badge/Galaxy-Toolshed-orange)](https://toolshed.g2.bx.psu.edu/)

本项目为**未集成在 Galaxy Tool Shed 中的生物信息学软件**提供 Galaxy 工具包装器和 Docker 容器镜像，便于集成到 Galaxy 平台用于科学研究。

## 项目概述

尽管 Galaxy 生态系统中已有大量工具，但仍有许多有价值的生物信息学软件尚未被集成到 Galaxy 官方的 [Tool Shed](https://toolshed.g2.bx.psu.edu/)。本项目旨在填补这一空白，为这些缺失的软件提供完整的 Galaxy 集成方案，包括：

- **符合 Galaxy Tool XML Schema 规范的 XML 包装器**
- **用于可重复部署的 Docker 容器镜像**
- **无缝集成到 Galaxy 的配置文件**

## 支持的工具

| 工具 | 描述 | 版本 |
|------|------|------|
| [STRling](./strling/) | 使用 k-mer 计数法检测 STR 扩展 | 0.6.0 |
| [GangSTR](./gangstr/) | 来自短读数据的全基因组 STR 基因分型 | 2.5.0 |
| [ExpansionHunter](./expansionhunter/) | 使用重复特异性图谱进行 STR 基因分型 | 5.0.0 |
| [Expansion Hunter Denovo](./expansionhunter_denovo/) | 无需先验位点的 STR 扩展检测 | 0.9.0 |
| [haplogrep3](./haplogrep3/) | 线粒体 DNA 单倍群分类 | 3.2.2 |
| [MitoZ](./mitoz/) | 线粒体基因组组装与注释 | 3.6 |
| [MutServe](./mutserve/) | 来自 NGS 数据的 mtDNA 突变检测 | 2.0.0-rc15 |

## 快速开始

### 验证 Galaxy 包装器

```bash
# 安装 planemo
pip install planemo

# 验证包装器语法
planemo lint ./strling/strling.xml
```

### 构建 Docker 镜像

```bash
cd strling/docker
docker build -t strling:0.6.0 --platform=linux/amd64 .
```

### 使用 Galaxy 测试

```bash
planemo test --galaxy_root=/path/to/galaxy ./strling/strling.xml
```

## 集成到 Galaxy

### 1. 复制工具文件

将工具目录复制到 Galaxy 的 `tools/` 文件夹：

```bash
cp -r strling /path/to/galaxy/tools/
```

### 2. 更新配置

添加到 `config/local_tool_conf.xml`：

```xml
<section id="str" name="短串联重复">
    <tool file="strling/strling.xml"/>
</section>
```

### 3. 配置作业执行

更新 `config/job_conf.xml` 将工具分配到目标执行环境：

```xml
<dest id="docker_local">
    <param id="docker_enabled">true</param>
    <param id="docker_image">strling:0.6.0</param>
</dest>
```

### 4. 重启 Galaxy

```bash
# 如果使用 systemd
sudo systemctl restart galaxy

# 或使用 supervisor
sudo supervisorctl restart galaxy:*

# 或手动重启（如果在前台运行）
# 按 Ctrl+C 停止，然后重新启动服务器
```

## 为什么创建这个项目

### Galaxy Tool Shed 的局限性

虽然 Galaxy Tool Shed 托管了数千个工具，但许多工具存在以下问题：

- 版本过时或缺乏维护
- 未包含在官方仓库中
- 由于依赖复杂而难以安装

### 我们的解决方案

本项目提供：

1. **最新版本的包装器** - 带有 proper Galaxy 集成的最新工具版本
2. **容器化部署** - Docker 镜像消除依赖问题
3. **最佳实践参数** - 通过文献综述验证的参数设置
4. **简化部署** - 可直接集成到现有 Galaxy 实例

## 为工具开发者贡献

要向本项目添加新工具，请按以下步骤操作：

1. 创建以工具名称命名的新目录
2. 按照现有模式开发 Galaxy XML 包装器
3. 在 `docker/` 目录中创建 Dockerfile
4. 添加 `tool_conf.xml` 配置工具分区
5. 提供中英文双语文档
6. 使用 `planemo lint` 进行验证

## 贡献指南

欢迎贡献！请确保：

- 遵循 Galaxy IUC 标准
- 包含 Docker 容器化配置
- 提供双语文档
- 提交前使用 planemo 测试

## 参考资源

- [Galaxy Tool XML Schema](https://docs.galaxyproject.org/en/latest/dev/schema.html)
- [Planemo 文档](https://planemo.readthedocs.io/)
- [Galaxy IUC 标准](https://galaxy-iuc-standards.readthedocs.io/)
- [官方 Tool Shed](https://toolshed.g2.bx.psu.edu/)

## 许可证

本项目采用 MIT 许可证。各独立工具遵循其各自目录中指定的许可证。

---

**注意**：本项目是独立项目，与 Galaxy Project 或 Galaxy Tool Shed 无关。提供的工具仅用于集成便利。
