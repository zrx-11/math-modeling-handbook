# 速查表

## 核心公式

| 场景 | 内容 |
|---|---|
| 线性规划标准型 | max z = cᵀx，s.t. Ax ≤ b，x ≥ 0 |
| 影子价格 | 右端项加 1 引起的最优值增量，等于对偶变量 |
| 整数规划松弛 | 连续解是整数解的上界，用于分枝定界剪枝 |
| KKT 梯度平衡 | ∇f + ∑λᵢ∇gᵢ = 0，λᵢgᵢ = 0 |
| SVM 间隔 | 2/‖w‖（支持向量处 wᵀx + b = ±1） |
| 最小二乘斜率 | ∑(xᵢ−x̄)(yᵢ−ȳ) / ∑(xᵢ−x̄)² |
| 一阶差分平衡点 | x* = b/(1−a)，稳定条件 |a| < 1 |
| SIR 基本再生数 | R₀ = β/γ |
| 极差标准化 | 效益型 (x−min)/(max−min)，成本型 (max−x)/(max−min) |
| 熵权 | wⱼ = (1−eⱼ)/∑(1−eⱼ) |
| GM(1,1) | x̂¹(k+1) = (x⁰(1) − b/a)e^(−ak) + b/a |
| 退火接受概率 | P = exp(−Δ/T) |

## 常用调用

| 目的 | 写法 |
|---|---|
| 线性/整数规划 | `linprog(c, A_ub=A, b_ub=b, bounds=..., method="highs")` |
| 非线性规划 | `minimize(fun, x0, method="SLSQP", constraints=cons)` |
| 最短路 | `scipy.sparse.csgraph.dijkstra` |
| 最小生成树 | `scipy.sparse.csgraph.minimum_spanning_tree` |
| 插值 | `CubicSpline(x, y)`、`interp1d` |
| 常微分方程 | `solve_ivp(f, [t0, t1], y0, method="RK45")` |
| 聚类 | `KMeans(n_clusters=3).fit(X)` |
| 主成分 | `PCA(n_components=2).fit_transform(X)` |
| SVM | `SVC(C=1.0, kernel="rbf", gamma="scale")` |

## 检查清单

| 检查项 | 标准 |
|---|---|
| 单位 | 等号两边量纲一致 |
| 量级 | 结果落在常识范围 |
| 极端值 | 变量取 0 或上界时公式仍合理 |
| 结果复现 | 换个随机种子结果波动可接受 |
| 论文一致 | 摘要数字与正文、代码输出三处一致 |
