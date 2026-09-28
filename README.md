# Publication Build

**Research Workflow Skills · 04 · Publication**

将已有文档或审后稿件转换为经核验的 LaTeX/PDF，支持用户或期刊模板及可独立编译的源码包。

## Research Workflow Skills 系列

四个独立安装、按证据交接衔接的科研工作流 Skill。可按需使用单个阶段；按阶段接续时，输入必须满足对应交接契约。

| 阶段 | Skill | 职责 |
|---|---|---|
| 01 · Planning | [Research Planning Mini](https://github.com/Mysticor/research-planning-mini-skill) | 选题、研究设计与证据交接 |
| 02 · Writing | [Manuscript Writing Mini](https://github.com/Mysticor/manuscript-writing-mini-skill) | 证据驱动的正文、图表与初稿 |
| 03 · Review | [Manuscript Review Mini](https://github.com/Mysticor/manuscript-review-mini-skill) | 独立审查、修订与审后交接 |
| 04 · Publication | [Publication Build](https://github.com/Mysticor/publication-build-skill) | 模板适配、LaTeX/PDF 与投稿源码包 |

研究规划 → 论文写作 → 审稿修订 → 出版排版。研究事实、引用与数值追溯贯穿全流程；通用版不预设个人领域、期刊、模型、账号或固定页数。排版也支持独立的普通文档转换。

## 安装

需要 Python 3.11+。完整保留仓库目录，不能只复制 SKILL.md。以下为 macOS/Linux 示例；Windows 使用对应虚拟环境和目录链接命令。

```bash
git clone https://github.com/Mysticor/publication-build-skill.git
cd publication-build-skill
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/module/codex-skill/publication-build" "${CODEX_HOME:-$HOME/.codex}/skills/publication-build"
```

已有同名 Skill 时先检查位置，不覆盖。重新加载 Codex Skill 列表后调用 `$publication-build`，提供独立的研究项目目录；运行脚本时使用已安装依赖的 Python 环境。不要把研究资料保存在本工具仓库中。

普通 Markdown/DOCX/LaTeX 排版无需 Stage 3 交接；正式出版模式接收 PUBLICATION_HANDOFF。需安装 Pandoc、TeX 发行版、latexmk、相应 BibTeX/Biber 和 Poppler；SVG 路线可能需要 rsvg-convert。系统依赖不自动安装。

## 目录与交接

- `module/codex-skill/publication-build/`：指令、脚本、模板、图标和 UI 元数据。
- `workflow-contract/`：共享状态与跨阶段版本校验库。
- `test-fixtures/`：仅供自动化校验的合成样例。

## 依赖与边界

共享状态库位于 workflow-contract。必要 Nature Skills 工具随写作/审稿仓库提供；已安装的同名工具可覆盖内置版本。需要凭据的可选服务由使用者配置，仓库不含个人账户或密钥。跨阶段 Skill 单独安装；缺少时交付材料并报告可用的下一步，不假装已经执行。审稿中的独立评审需要支持隔离 Agent 的运行环境，无法隔离时应明确限制。

保留真实证据、数值与引用追溯、内容一致性检查和 MOCK 隔离。自动化测试不能替代科学判断或逐页视觉审查，也不能保证网络和长会话稳定性。

## 验证

```bash
python -B module/codex-skill/publication-build/tests/exercise.py /tmp/publication-test-UNIQUE
bash module/codex-skill/academic-typesetting/tests/test_final_typesetting.sh
python -B -m unittest discover -s workflow-contract/tests -p 'test_*.py'
```

测试数据仅为合成 MOCK/FIXTURE，不是真实研究。可选跨阶段测试通过 `DOWNSTREAM_SKILL_ROOT` 指定另一个仓库的 Skill 目录，未提供时明确跳过。排版验收请使用不存在的新临时目录；所需系统工具缺失时先安装依赖。

## 许可证与来源

原创部分采用 MIT，见 LICENSE。第三方代码遵循其各自许可，见 THIRD_PARTY.md 与组件内保留的声明。
