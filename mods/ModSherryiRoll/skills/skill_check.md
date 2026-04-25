# 检定技能（check）

## 触发条件
当用户：
- 提到“检定 / ra / rb / rp”
- 或表达类似：力量检定、侦查检定

## 行为

根据类型调用：

### 普通检定
→ 调用 `rollAttribute`

### 奖励检定
→ 调用 `rollAttributeBonus`

### 惩罚检定
→ 调用 `rollAttributePunishment`

## 参数解析

- 属性名：如 力量 / 侦查
- 次数：如 3# 表示 count=3，否则默认1
- 数值/表达式：
  - 如 力量50 → value=50
  - 如 力量1d100 → expression

## 必须
- 始终调用工具，不允许自行生成结果

## 禁止
- 不要跳过工具直接输出“成功/失败”
