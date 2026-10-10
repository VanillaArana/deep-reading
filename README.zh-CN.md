# Deep Reading · 深度共读 V0.1 alpha

**AI 应该让你成为更好的读者，而不是代替你阅读。**

[English](README.md) · [审计与复用说明](docs/provenance.md) · [测试与发布检查](docs/test-report.md)

[GitHub 仓库](https://github.com/VanillaArana/deep-reading) · [下载源码 ZIP](https://github.com/VanillaArana/deep-reading/archive/refs/heads/main.zip)

这是优先支持 Codex 的 Agent Skill，从已经实际使用的 Human Insight Reading 共读流程中提炼而来。保留 Chapter Map、累计提问预算、Reading Session、Evidence Policy 和 Claim Audit，不把深度阅读简化成摘要或题库。

适合阅读心理学、非虚构、人文社科及复杂论证，希望获得解释、理解反馈和跨会话接续的读者。文学与哲学重视文本依据及解释分歧，不强套实证分级。

## 核心体验

- 按论证、上下文和阅读目标区分 A核心、B辅助、C次要、D可略读；只见节选时只给局部暂定地图。
- 启发优先、平衡模式（默认）、讲解优先。明确要求“直接解释”立即响应；每次默认最多3个主动理解检查，已经理解便继续。
- 区分[原文]、[解释]、[外部资料]、[待核实]；重要结论保留来源、范围、争议与纠错历史。
- 灵活安排长期计划和每次起止；疲劳、暂停或结束后都留下具体 Next Session。
- 已读、已讨论、已显示理解、用户确认和证据审计分别记录。
- 普通 Markdown 保存；Obsidian 可选，不需数据库或后台服务。

教学判断由宿主模型执行。可选脚本只负责安全建档与读取，不判断掌握或科学真伪。

## 搭配原书使用

**推荐边读原书，边用 Deep Reading 讨论。** 先由你阅读一个小节，再带着自己的理解或疑问共读；AI依据实际正文解释、校正和核验。让你与AI都能对照同一版本的电子书，更便于定位难点、核对作者表述和接续进度。

使用前自行准备有权使用的电子书，可从出版社、图书馆或公版书库获取。如果使用 Z-Library 等来源，也请确认具体文件的使用权限与版本。获取原书后，将文件放入自己的阅读目录，告诉 Codex 文件位置和本次阅读范围；Skill不附带原书，也不自动下载。

建议准备文字可提取的 EPUB 或 PDF。开始时核对作者、译者、版次和目录；电子书结构可读不等于内容完整无误。扫描版的文字识别可能出错，精确引文应对照原页面。纸书同样可以共读：提供所讨论段落及版本信息即可。

一个自然的使用顺序是：**准备原书 → 核对版本 → 自己阅读 → 表达理解或提问 → 对照正文讨论 → 保存进度与下次计划。**

## 安装

从上方下载源码ZIP并解压，或克隆仓库：

```sh
git clone https://github.com/VanillaArana/deep-reading.git
cd deep-reading
```

安装的是 `skills/deep-reading` 文件夹。复制到阅读工作区的 `.agents/skills/deep-reading`，或个人 `~/.agents/skills/deep-reading`。若已有同名 Skill，先比较，不覆盖。

在本包根目录运行 PowerShell 示例，输入自己的阅读工作区：

```powershell
$readingWorkspace = Read-Host '阅读工作区目录'
$skillDestination = Join-Path $readingWorkspace '.agents/skills/deep-reading'
if (Test-Path -LiteralPath $skillDestination) { throw '已有同名Skill，请先比较' }
New-Item -ItemType Directory -Path (Split-Path $skillDestination) -Force | Out-Null
Copy-Item -LiteralPath './skills/deep-reading' -Destination $skillDestination -Recurse
```

之后在 Codex 使用 `$deep-reading`。未出现时重启 Codex。2026-10-10已查阅[官方 Codex 技能文档](https://learn.chatgpt.com/docs/build-skills)及[Agent Skills 规范](https://agentskills.io/specification)确认元数据和发现路径；安装后的实际模型行为仍须按测试文档验收。macOS/Linux复制命令见英文README。

## 第一次怎么用

> 用 $deep-reading 共读这本书。我提供书名、已知版次、目录和第一小节正文。目标是理解论证，每次约20分钟，默认平衡模式。请把真实阅读记录保存在我指定的独立阅读目录。

能从文件取得的信息不反复问；ISBN、页码或日期未知就保留未知。先看实际材料、规划合理范围，再讨论你的理解。原来已有记录和布局就复用，不要求重建笔记库。共读示例见[原创合成演示](examples/demo-session.md)，不是真实用户记录。

## 保存和下次继续

数据放在公开项目和安装包以外，例如：

```text
你的阅读目录/book-id/book.md
你的阅读目录/book-id/sessions/S001.md
```

book.md是唯一现行进度入口，保存版次、目标、实际停点、累计问题数、未解/复习事项和下一次计划；Session笔记保留原话、讨论与历史。概念卡、错误日志按需创建。实质修改前保留有日期、名称不同的备份。先写实际记录，再更新索引并核对；多文件保存不是事务，失败时须说明已写与未写部分。

新聊天可说：

> 用 $deep-reading 从这份书籍索引继续，先读取最近实际Session和相关错误记录，再决定本次范围。

没有写文件权限或你说“不保存”时，输出可复制状态，并明确未保存。不能把聊天里的计划当文件或实际完成。

可选脚本无需第三方包，需 Python 3.10+，从本包根目录运行（路径换成你自己的）：

```sh
python skills/deep-reading/scripts/reading_state.py init --root /你的阅读目录 --book-id sample-book
python skills/deep-reading/scripts/reading_state.py resume --root /你的阅读目录 --book-id sample-book
```

初始化拒绝已有书籍目录和包内数据位置，不创建虚假已读会话。恢复只读取索引、实际链接的会话与可选错误日志；拒绝越界、联接/符号链接和缺失链接。安装后按实际安装位置运行脚本。不使用Python也可手动复制模板。

## 常见问题与局限

**必须用Obsidian吗？** 不必，普通文本编辑器可完成全流程。基础共读不需Python或API密钥，宿主Codex由你自己的环境提供。

**可以跳过问题吗？** 可以，要求直接解释、调整计划、暂停或深入次要内容都由读者决定。提问预算是上限，不是配额。

**只给ISBN能解释某页吗？** 不能。ISBN用于识别版本，不证明获得正文。文件页、纸书页和阅读器动态页不能混用，也不自动下载书籍。

**能保证正确吗？** 不能。标签与审计呈现依据和边界，不能消除模型错误；作者确实这样说不等于世界确实如此，理解也不等于审计通过。

**会自动安排提醒吗？** 不会。复习事项在读者主动开始时使用；V0.1没有云账户、同步、向量库、后台提醒或图形界面。

**测试到什么程度？** 见[测试报告](docs/test-report.md)。23项自动测试中22通过、1跳过；三轮冻结的模型行为测试经独立模型评审，依次为27/30、28/30、30/30，前两轮失败均保留。已执行本地CLI连续共读、停止保存和全新会话恢复。测试材料是合成的，不能推导普遍准确率或真实学习效果；模型具体设置未披露。其他平台及macOS/Linux原生运行尚未验证。

**为什么历史备份里的相对链接可能打不开？** 原样副本保留了相对原笔记位置的路径。应按原笔记目录解析引用，或在独立复制的原目录结构中查看，保留当前笔记。备份不能作为当前进度入口。若希望备份也能直接导航，应使用保留原目录结构的归档。

## 许可证与发布状态

[MIT许可证](LICENSE)适用于本包项目材料，不涵盖读者原书或私人笔记。仓库发布的是早期alpha，本地技术与行为检查及其限制见测试报告。包中不含原书、私人记录、设备配置或旧聊天。标为稳定版前，建议再完成一次真实读者试用。
