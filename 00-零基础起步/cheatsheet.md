# 速查表

## 流程

| 场景 | 动作 |
|---|---|
| 刚拿到题 | 三要素各写一句，写不出就重读题 |
| 模型跑出怪结果 | 查量纲、量级、极端值 |
| 时间不够 | 砍第三问精细度，保摘要与检验 |
| 交卷前 | 摘要数字对正文、符号表全覆盖、PDF 无乱码 |

## 常用命令

| 目的 | 命令 |
|---|---|
| 装建模库 | `pip install numpy scipy pandas matplotlib scikit-learn openpyxl` |
| 线性规划 | `linprog(c, A_ub=A, b_ub=b, bounds=..., method="highs")` |
| 读 Excel | `pd.read_excel("data.xlsx")` |
| 画折线 | `plt.plot(x, y); plt.xlabel("月份"); plt.ylabel("销量/件")` |
| 保存图 | `plt.savefig("fig1.png", dpi=300, bbox_inches="tight")` |

## 数字口径

| 指标 | 常见写法 |
|---|---|
| 误差 | MAPE 平均绝对百分比误差、RMSE 均方根误差 |
| 拟合优度 | R²，越接近 1 越好，但要看变量个数 |
| 显著性 | p < 0.05 常作界线，必须说明原假设是什么 |
