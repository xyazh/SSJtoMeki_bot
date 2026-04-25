# 角色卡技能（card）

## 触发条件
当用户涉及：
- st / 设置属性
- show / 查看属性
- pc / 角色卡操作

## 行为

### 设置属性
→ `setAttribute`

### 查看属性
→ `showAttribute`

### 角色卡操作
- 新建 → `playerCardNew`
- 绑定 → `playerCardBind`
- 删除 → `playerCardDelte`
- 列表 → `playerCardList`
- 重命名 → `playerCardNewName`
- 复制 → `playerCardCopy`
- 显示 → `playerCardShow`

## 必须
- 根据用户意图选择正确 tool

## 禁止
- 不要伪造角色卡数据
