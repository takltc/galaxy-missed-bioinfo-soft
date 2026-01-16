# MitoZ Docker 镜像
# 线粒体基因组组装、注释和可视化工具包
# 版本: 3.6
# 参考: https://github.com/linzhi2013/MitoZ
# 使用官方预构建镜像以确保依赖兼容性

FROM guanliangmeng/mitoz:3.6

LABEL maintainer="Galaxy Tools"
LABEL version="3.6"
LABEL description="MitoZ: A toolkit for animal mitochondrial genome assembly, annotation and visualization"
LABEL doi="10.1093/nar/gkz173"

WORKDIR /data

ENTRYPOINT ["mitoz"]
CMD ["--help"]
