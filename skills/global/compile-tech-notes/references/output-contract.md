# Output Contract

Use this reference to shape the intermediate objects and the final deliverable.
This skill is no longer limited to one note shape.
The contract should work for status updates, meeting memos, feasibility briefs, material digests, learning notes, and shareable syntheses.

## Required objects

Create these objects before calling the work complete.

### 1. `job_contract`

Format:

```md
## 任务契约

- deliverable:
- target_reader:
- central_question:
- time_window:
- stop_condition:
- evidence_bar:
```

Rule:

- `central_question` must be answerable and useful to the target reader.
- For status or secretary work, the central question can be operational, for example:
  - `What changed, what is blocked, and what matters now?`
  - `What was decided in this meeting and who owns the next actions?`

### 2. `source_map`

Format:

```md
## 来源映射

| id | 来源 | 类型 | 本地/外部 | 可信度 | 作用 | 支撑内容 |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | 会议转写 | transcript | local | 高：事件事实 | 主锚点 | 决策、action items |
```

Rule:

- Every major section should map to at least one source.
- Strong claims should usually have an anchor plus a validator or comparator.

### 3. `claim_layers`

Format:

```md
## 事实 / 判断 / 推断 / 延展

### Facts
- ...

### Judgments
- ...

### Inferences
- ...

### Extensions
- ...
```

Rule:

- Do not mix layers in one bullet.
- Move uncertain statements downward instead of dressing them up.

### 4. `action_and_decision_register`

Required when the deliverable includes work tracking, meetings, feasibility recommendations, or next steps.
If genuinely not applicable, explicitly say `not applicable`.

Format:

```md
## 决策与行动寄存器

| type | 内容 | owner | due | status | confidence | source |
| --- | --- | --- | --- | --- | --- | --- |
| decision | 先做 A，再评估 B | team | 2026-04-25 | agreed | high | S1 |
| action | 整理对比表并补官方定义 | ocean | 2026-04-22 | open | medium | S2 |
```

Rule:

- Do not invent owners or deadlines when they are missing.
- If owner or due date is inferred rather than explicit, say so in `confidence` or the draft.

### 5. `deliverable_outline`

Pick the skeleton that matches the deliverable instead of forcing a note structure on everything.

#### `task-status-update`

```md
1. 范围与时间窗
2. 本次最重要的变化
3. 已完成 / 已验证
4. 当前阻塞与风险
5. 下一步动作
6. 参考来源
```

#### `meeting-secretary-memo`

```md
1. 会议范围与参与者
2. 一段话总结
3. 核心结论 / 决策
4. 行动项与 owner
5. 仍待确认的问题
6. 参考来源
```

#### `feasibility-brief`

```md
1. 要回答的问题
2. 先给建议
3. 方案与证据
4. 风险 / 边界 / 代价
5. 推荐下一步
6. 参考来源
```

#### `material-digest`

```md
1. 材料范围与筛选原则
2. 先给浓缩结论
3. 主题分组
4. 重要分歧与空白
5. 建议补充检索
6. 参考来源
```

#### `systematic-learning-note`

```md
1. 资料范围与边界
2. 这篇笔记要解决什么问题
3. 先给结论
4. 主体内容重构
5. 关键机制 / 案例 / 结构
6. 边界、误区与取舍
7. 延展理解
8. 实践清单 / 下次怎么用
9. 参考来源
```

#### `blog-style-synthesis`

```md
1. 读者为什么要关心
2. 先给观点
3. 关键论点展开
4. 机制 / 案例 / 对比
5. 边界与反例
6. 结论与启发
7. 参考来源
```

### 6. `final_draft`

The final draft should be readable as a standalone deliverable for its target reader.

Minimum expectations:

- clear scope and reader
- an answer or synthesis block near the top
- traceable evidence behind the key claims
- at least one reusable organizing frame
- when relevant, a visible action/decision register
- at least one concrete next-use hint or next action

## Narrative skeleton chooser

Use the following quick chooser when the shape is unclear:

- `status-and-blockers`
  Best when the question is `what changed, what is blocked, and what matters now?`
- `decision-and-actions`
  Best when the question is `what did we decide and who owns the next moves?`
- `problem-driven`
  Best when the question is `why does this exist and what pain does it remove?`
- `system-dissection`
  Best when the question is `how do the parts fit together?`
- `case-synthesis`
  Best when the question is `what can we learn by comparing examples or sources?`
- `comparison-evaluation`
  Best when the question is `which option fits which context?`

## Downgraded outputs

If the material is not strong enough for a full draft, choose one of these instead.

### `checkpoint-only`

Use for thin work updates when only the operational surface is stable.

```md
## 时间窗
## 已确认变化
## 未确认项
## 下一步
```

### `action-register-only`

Use for thin meeting or secretary work when the only stable artifact is decisions plus follow-up.

```md
## 会议范围
## 已确认决策
## 行动项与 owner
## 仍待确认的问题
```

### `source-map-plus-gaps`

Use when the material is rich but still too noisy to organize cleanly.

```md
## 已有来源
## 关键空白
## 建议补充检索
## 下一版骨架
```

### `options-and-gaps memo`

Use when the user wants a feasibility answer but the evidence only supports options framing.

```md
## 目前可行选项
## 各自证据
## 主要风险
## 还缺的关键事实
```

### `open-questions memo`

Use when important claims conflict or remain unstable.

```md
## 当前最稳的事实
## 互相冲突的说法
## 现阶段更可信的一侧
## 还不能下结论的地方
```
