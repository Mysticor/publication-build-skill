# Publication Build / publication-build
第四阶段将审后冻结稿构建为期刊合规的 LaTeX、PDF 和独立可编译源码包。
源码保存在本目录；安装入口 ~/.codex/skills/publication-build 仅为符号链接。
核心执行器是同级 academic-typesetting（latex-document-skill 的适配执行器）。

调用：
- 使用 $publication-build，接收当前 PUBLICATION_HANDOFF，开始第四阶段。
- 继续 publication-build，使用我上传的模板 ZIP；以交接包中的目标期刊为准。
- 第四阶段定稿，完成全部检查并生成投稿源码包。

没有期刊时按文档用途选择通用排版；附带 Academic Paper 模板仅为可选起点，没有固定页数。
用户 ZIP/目录/tex 优先；URL 先下载并验证来源，再载入。当前官方规则在实际构建时查询。
可执行工具及 13 阶段入口见 SKILL.md，CLI 用 --help。报告模板在 templates/。
本机 Python 使用 3.11+；使用项目内置 academic-typesetting 执行器，需要 Pandoc、TeX 引擎、
latexmk、BibTeX/Biber（按模板）、Poppler。Pillow 用于栅格有效分辨率检查。
不自动安装系统依赖。测试使用明确标识的 MOCK，不是论文或期刊实测认证。
源码/安装发现/真实编译及失败注入结果见模块 validation/publication-build/。

统一入口：普通文件排版与第四阶段出版构建都使用「Publication Build」。
技术调用名保留 publication-build。原 academic-typesetting 不再作为独立 Skill 安装，
其项目源码保留为内部执行器，避免复制或丢失现有编译能力。
