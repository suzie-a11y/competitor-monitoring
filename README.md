# iPhone 18 配件竞品动态监控

## 监控目标

每日记录 Spigen、BURGA、RHINOSHIELD（犀牛盾）、OtterBox 在德国区及 Global 的全部重要公开更新。抓取阶段不使用 iPhone 18 作为筛选条件；先回答“他们今天发布了什么、在说什么、释放了什么信号”，最后再单独判断这些信号是否可用于 iPhone 18 配件项目。

## 每日输出

每次运行生成一份 `competitor-monitoring/reports/YYYY-MM-DD.md`，并将去重后的新条目追加到 `competitor-monitoring/data/updates.jsonl`。每条记录至少包含：

- 品牌、平台、发布时间、标题/首句、原文链接
- 社媒必须提供“原帖直链”：Instagram 使用 `/p/` 或 `/reel/`，Facebook 使用具体帖子 permalink，X 使用 `/status/`；账号主页链接不能替代原帖链接
- 动作类型：新品/预热、促销、联名、功能卖点、渠道/零售、用户互动、媒体报道
- iPhone 18 关联度：直接提及 / 型号或尺寸线索 / 非直接但相关
- 今日释放信号：产品方向、技术卖点、价格/促销、渠道/上市节奏、内容主题、联名/人群、用户反馈或品牌定位
- 核心信息与对 TORRAS 的启示
- 证据等级：官方原文 / 官方社媒 / 第三方媒体 / 搜索摘要

## 监控入口

| 品牌 | 官网/新闻入口 | Instagram | Facebook | X |
|---|---|---|---|---|
| Spigen | https://www.spigen.com/blogs/news | https://www.instagram.com/spigen/ | https://www.facebook.com/SpigenWorld/ | https://x.com/Spigen |
| BURGA | https://burga.com/pages/iphone-18-access | https://www.instagram.com/burgaofficial/ | https://www.facebook.com/burgaofficial/ | 搜索 `BURGA iPhone 18` |
| RHINOSHIELD | https://rhinoshield.io/featured/iphone-17 | https://www.instagram.com/rhinoshield/ | https://www.facebook.com/RhinoShield/ | 搜索 `RHINOSHIELD iPhone 18` |
| RHINOSHIELD Japan | https://rhinoshield.jp/blogs/news | https://www.instagram.com/rhinoshield_jp/ | https://www.facebook.com/RhinoShieldJapan | https://x.com/RHINOSHIELD_JP |
| OtterBox | https://media.otterbox.com/press-releases?l=100 | https://www.instagram.com/otterbox/ | https://www.facebook.com/otterbox/ | https://x.com/OtterBox |

## 德国重点新闻源白名单

新闻抓取不只依赖品牌官网。每天至少检查以下德国科技/手机媒体的最新文章，并在报告中保留文章直链、发布时间、媒体名称和证据等级：

| 优先级 | 媒体 | 重点栏目 | 入口 |
|---|---|---|---|
| A | heise online | Smartphone / Mobiles | https://www.heise.de/thema/Smartphone |
| A | ComputerBase | Smartphones | https://www.computerbase.de/news/smartphones/ |
| A | NETZWELT | Handy / Technology | https://www.netzwelt.de/handy/index.html |
| A | inside digital | Handy-News | https://www.inside-digital.de/handy/news |
| A | connect | iPhone / Smartphones & Tarife | https://www.connect.de/thema/iphone/ |
| A | teltarif.de | Handy & Co. | https://www.teltarif.de/h/index.html |
| B | Golem | Mobile / IT-News | https://www.golem.de/ |
| B | t3n | Tech / Apple / E-Commerce | https://t3n.de/ |
| B | CHIP | Handy / Apple | https://www.chip.de/ |
| B | Macwelt | Apple / iPhone | https://www.macwelt.de/ |

### 新闻筛选口径

不以 iPhone 18 为必要条件。优先收录竞品品牌、手机壳/保护膜/MagSafe/充电配件、零售上架、联名、促销、供应链、产品评测和用户趋势；每条新闻都要总结“报道了什么”和“释放了什么信号”，最后再判断与 iPhone 18 配件项目的关联度。相同新闻转载时保留首发或信息最完整的来源，并把其他媒体作为补充。

## 免费公开源模式

当前不使用 Meltwater、Brandwatch 等付费监听 API，改用以下免费方式：

1. 德国新闻：检查白名单媒体栏目、公开 RSS 和 Google News RSS；按品牌名、配件类别、促销、联名、零售和手机关键词检索，不把 iPhone 18 作为必要条件。
2. Instagram：使用公开账号页和搜索引擎查询 `site:instagram.com/账号/ (p OR reel)`；只有取得具体 `/p/` 或 `/reel/` 原帖链接时才记为已验证内容。
3. Facebook：使用公开页面、搜索结果和具体帖子 permalink；无法取得帖子直链时记为不可验证。
4. X：使用公开账号页和 `/status/` 帖子链接；无法取得具体帖子时记为不可验证。
5. 不绕过登录、验证码、限流或平台权限；免费模式不能保证抓到 Instagram 每一条帖子，报告必须明确缺口。

## 德国区优先规则

1. 每个品牌先查德国官方站点、德国/德语新闻稿、德国区 Instagram/Facebook/X 账号，以及德国零售或本地活动页面。
2. 只有在德国区没有可验证官方入口、当天无公开更新，或入口无法访问时，才回退到 Global 官方入口。
3. 报告中必须标注 `DE` 或 `Global`，并记录“德国区无独立账号/入口”或“德国区不可验证”的原因；不能把 Global 动态默认为德国区动作。
4. 账号归属须以官网社媒链接、账号认证信息或品牌官方交叉链接确认；无法确认的账号只作为线索，不进入重点结论。

## 社媒抓取操作

### Instagram 自动采集器（Instaloader + GitHub Actions）

当前项目已加入公开账号自动采集器：`.github/workflows/instagram-monitor.yml`。它每天 09:00（Asia/Shanghai）运行一次，使用 [Instaloader](https://github.com/instaloader/instaloader) 读取四个 Global 公开账号最近 24 小时的帖子，不使用账号密码、Cookie 或代理。

采集结果写入：

- `data/instagram_runs/YYYY-MM-DD.json`：当天四个品牌各自的状态、失败原因、帖子正文、发布时间、类型、互动数和原帖直链。
- `data/updates.jsonl`：去重后追加的新 Instagram 条目。

首次启用步骤：

1. 将 `competitor-monitoring` 放入一个 GitHub 仓库，并确保 Actions 有写入仓库内容的权限。
2. 在 GitHub 仓库的 Actions 页面手动运行 `Instagram competitor monitor`，先观察一次结果。
3. 确认 `data/instagram_runs/` 有当天 JSON 后，再等待每日定时运行。
4. 日报和看板读取当天 JSON；`status=不可验证` 时必须展示原因，不能改写成“无动态”。

这套方式只保证“公开可验证内容的自动检查”，不保证 Instagram 每条帖子都能抓到。Instagram 需要登录、触发限流或改变页面结构时，运行仍会保留品牌状态和失败原因，不绕过平台限制。

1. 先打开德国区官方账号或官网社媒入口，确认账号归属；德国区没有独立账号时再使用 Global 账号。
2. 以过去 24 小时为窗口，读取公开可见的帖子、Reels、视频、图片、置顶帖更新和公开评论；不先用 iPhone 18 关键词过滤，先记录品牌当天的全部重要更新，再做项目关联分析。
3. 每条入库记录必须保存：平台、账号、帖子发布时间、帖子首句/标题、原帖直链、内容类型、截图或可验证摘要、DE/Global 标记。
4. 原帖直链优先从帖子本身复制；不要只保存搜索结果链接、账号主页链接或第三方转述链接。第三方报道可作为补充来源，但不能替代官方社媒原帖。
5. Instagram/Facebook/X 如果需要登录、被限流、只有搜索摘要或只能看到账号主页，标记“不可验证”，并把缺失的原帖直链写入“不可验证项”，不要编造 URL。
6. 归档时按原帖直链去重；同一帖子在多个平台转载，分别记录平台链接，并标注“同源转载”。

### 社媒链接格式

| 平台 | 合格的原帖链接示例 | 不合格替代 |
|---|---|---|
| Instagram | `https://www.instagram.com/p/短码/`、`https://www.instagram.com/reel/短码/` | `https://www.instagram.com/账号/` |
| Facebook | 帖子具体 permalink | Facebook 主页或搜索结果页 |
| X | `https://x.com/账号/status/数字ID` | 账号主页或搜索结果页 |

## 每日检索词

- `iPhone 18 case`, `iPhone 18 Pro case`, `iPhone 18 Pro Max case`, `iPhone 18 Ultra case`
- `iPhone 18 MagSafe`, `iPhone 18 compatible`, `iPhone 18 launch`, `iPhone 18 early access`
- 各品牌名 + `case`、`MagSafe`、`launch`、`preorder`、`collab`、`drop`、`sale`、`new`、`creator`、`review`

## 去重与质量规则

1. 以规范化 URL 为主键；无 URL 时使用品牌 + 平台 + 发布时间 + 标题指纹。
2. 同一新闻被多家媒体转载时保留官方原文，并把媒体报道作为补充证据。
3. 搜索摘要只能作为线索，标注为“搜索摘要”，不得写成已被官方确认。
4. 不要求条目直接提及 iPhone 18；只要能反映竞品当天的产品、上市节奏、价格/促销、渠道、内容主题、用户人群或传播打法，就进入日常更新摘要。只有对项目有明显启发的条目才进入“重点关注”。
5. 社媒需要登录、无法读取或疑似限流时，记录“不可验证”，不填充为“无动态”；没有原帖直链的社媒线索不得进入“已确认动态”。

## 当前基线（2026-08-21）

- BURGA：iPhone 18 Early Access 页面已公开，宣称覆盖 Pro、Pro Max、Ultra；首发优惠为买 4 付 2，另有磁吸套装 20% off。
- Spigen：出现 iPhone 18 Series 预热/产品线索，包含 Thin Fit MagFit、Rugged Armor MagFit；页面仍声明图片将在官方发布后替换，需持续验证。
- OtterBox：官方新闻稿中心仍在更新新品；第三方媒体报道其零售渠道提前出现 iPhone 18 Pro 兼容性包装，需等待官方确认。
- RHINOSHIELD：官网当前主要呈现 iPhone 17 系列；其日本官方账号入口已确认，iPhone 18 动作暂未在本轮公开检索中确认。
