永久记录本目录分层架构（本次给你的完整文件夹树）
# Repository_Structure.md
## 文档说明
本文档永久记录 layered-section-geometry-lsg 仓库完整目录分层架构，按开发批次、版本标签分段记录，用于开源存证、现有技术证据链固定、版本溯源。
仓库基础约束：MIT协议 + 公有领域底层内核补充专利约束；Common-LSG底层几何算法永久归入人类公共知识领域。

## 全局版本迭代总览
1. v0.0-BaseFrame：批次0 仓库基础骨架、协议、顶层文档、空目录预创建
2. v0.1-CommonCore：批次1 Common-LSG通用底层内核完整实现，开源，锁定LSG理论本体 
3. v0.2-Core4Industry：批次2 四大成熟核心行业落地模块（医疗CT/超声、山区无人机导航、水下潜航测绘）
4. v0.3-Full12Industry：批次3 八大高价值工业场景补充模块，完成12大商用行业全覆盖，完整现有技术证据链成型



## 根目录一级文件夹&文件总览
layered-section-geometry-lsg/
├─ LICENSE # MIT 协议 + 3 条公有领域专利约束
├─ README.md # 仓库总介绍、理论、应用清单、开源防专利逻辑、预印本链接
├─ .gitignore # 编译缓存、原始影像、权重、日志、IDE 配置过滤规则
├─ requirements.txt # 全仓库分场景第三方依赖清单
├─ git_push_batch2.sh/.bat # 批次 2 一键提交存证脚本
├─ git_push_batch3.sh/.bat # 批次 3 一键提交存证脚本
├─ Common-LSG/ # 批次 1 底层通用几何内核（v0.1）
├─ 【批次 2 四大核心行业】│ ├─ Medical-CT/
│ ├─ Medical-Ultrasound/│ ├─ Geo-MountainNav/
│ └─ Ocean-SubNav/├─ 【批次 3 八大新增工业行业】
│ ├─ Aerospace-Space/│ ├─ Industrial-3DInspect/
│ ├─ Architecture-BIM/│ ├─ Robot-Vision/
│ ├─ Energy-OilGeo/
│ ├─ VirtualReality-VRAR/
│ ├─ Traffic-SmartRoad/
│ └─ Bio-Microscope/
├─ docs/ # 全仓库标准化文档集合
│ ├─ Repository_Structure.md    # 仓库架构总文档（已存在）
│ ├─ api_docs/                   # 底层库接口文档
│ ├─ exp_reports/                # 各行业实验验证报告
│ └─ preprints/                  # 预印本论文总目录【新增】
   ├─ GYY-GOES/                # 全域本源演化体系主论文
   │  ├─ main_manuscript_zh.md # 中文版完整预印本正文
   │  ├─ main_manuscript_en.md # 英文对照翻译稿
   │  ├─ appendix/             # 全套数学附录
   │  │  ├─ appendix_A_axioams.md    # 四条本源公理严格数学表述
   │  │  ├─ appendix_B_GDE_eq.md     # 普适动力学方程完整推导
   │  │  ├─ appendix_C_LSG_matrix.md  # LSG矩阵形式完整推导（本次新增）
   │  │  ├─ appendix_D_fdm_code.md   # 有限差分代码理论对应说明
   │  │  └─ appendix_E_prediction.md # 可实验定量预言计算过程
   │  ├─ figures/              # 论文矢量示意图、几何截面图
   │  └─ preprint_pdf/         # 编译完成PDF成品（中英双版）
   ├─ lsg_engineering/         # LSG工程应用专项论文（CT/导航/工业检测）
   └─ supplementary_material/  # 论文配套补充材料、数值算例数据
└─ 【批次 4 预留空文件夹（待开发 v1.0）】
├─ Meteorology-Atmosphere/
└─ Archaeology-RelicScan/

## 分批次详细目录拆解

### 批次0 v0.0-BaseFrame：基础框架固定内容（永久不变）
#### 根目录基础文件
- LICENSE
- README.md
- .gitignore
- requirements.txt（初始仅通用numpy/scipy）

#### docs/ 固定文档清单
1. docs/LSG_Theory_Base.md：LSG层级截面几何完整理论、四维公理、矩阵/积分/维度互易数学推导
2. docs/Repository_Structure.md：本文件，仓库架构永久记录文档
3. docs/Patent_Prevention_Logic.md：开源规避专利纠纷完整原理
4. docs/Preprint_Link.md：GYYG-OES预印本DOI、公开时间存证页面
5. docs/Dev_Standard.md：统一代码、矩阵、截面数据、跨场景接口开发规范

#### 预创建空目录（批次0仅建文件夹，无业务代码）
Common-LSG/、12大行业文件夹、2个小众拓展文件夹

---

### 批次1 v0.1-CommonCore：Common-LSG底层内核完整实现
Common-LSG/
├─ README.md # 底层库数学说明、跨场景调用示例
├─ axiom_calc/ # LSG 几何公理计算库
├─ slice_rebuild/ # 通用非正交截面重建内核
├─ constraint_algo/ # 全局基础约束、平滑、畸变修正算子
├─ core_gde_solver/ # 【新增 v0.1.1】GDE 全域对偶演化矩阵求解器
│ ├─ gde_lsg_solver.py # LSG 多层截面 GDE 演化主求解器类
│ ├─ operators.py # 三维拉普拉斯 / 梯度 / 层级耦合稀疏算子库
│ ├─ test_gde_solver.py # 单元测试与守恒性验证脚本
│ └─ README.md # 模块定位、理论溯源、调用接口文档
└─ io_utils/ # 通用数据解析、STL/OBJ/ 点云三维导出工具
批次完成动作：完整底层代码+配套数学文档提交，打上v0.1-CommonCore标签，底层内核公有领域存证锁定。
> 【v0.1.1 增量更新】新增 core_gde_solver 模块，完成「本源公理→普适动力学方程→LSG矩阵形式→有限差分数值实现」全链条代码落地，统一全仓库底层几何计算口径，为所有行业模块提供标准化正演与重建底座。
---

### 批次2 v0.2-Core4Industry：四大成熟核心行业模块
所有行业统一标准子目录结构：
`行业文件夹/ ├─ scene_constraint/ ├─ noise_optimize/ ├─ hardware_adapt/ ├─ demo_case/ └─ README.md`

包含模块：
1. Medical-CT：医学CT影像三维重建模块
2. Medical-Ultrasound：超声成像三维重建模块
3. Geo-MountainNav：山区无人机离线高精地形导航模块
4. Ocean-SubNav：水下潜航多波束海底测绘导航模块

批次完成动作：4套场景专属优化代码、Demo、README全部入库，更新总README与本文档，提交并打标签v0.2-Core4Industry，覆盖医疗、空对地、水下测绘三大核心赛道。

---

### 批次3 v0.3-Full12Industry：八大高价值工业场景模块（本次新增）
沿用统一行业目录模板：`scene_constraint/ + noise_optimize/ + hardware_adapt/ + demo_case/ + README.md`
本次新增8大行业完整代码模块：
1. Aerospace-Space 航空航天遥感大尺度测绘
2. Industrial-3DInspect 工业CT三维无损缺陷检测
3. Architecture-BIM 倾斜摄影建筑BIM逆向建模
4. Robot-Vision 机器人RGB-D嵌入式低算力环境感知
5. Energy-OilGeo 油气地震勘探地层三维建模
6. VirtualReality-VRAR VR/AR轻量化实时空间重建
7. Traffic-SmartRoad 车载激光雷达智慧道路高精地图
8. Bio-Microscope 共聚焦生物显微亚微米三维成像

#### 批次3配套同步更新内容
1. 根目录 requirements.txt：追加8个模块对应第三方依赖包清单
2. 新增脚本 git_push_batch3.sh / git_push_batch3.bat：批次3一键提交、打标签、推送远程
3. 总根目录 README.md：应用领域清单补充8个新增行业完整简介
4. 本文档 Repository_Structure.md：新增批次3完整架构记录，标记v0.3-Full12Industry版本节点

#### 批次完成核心价值
当前仓库共计12个商用行业完整实现模块，覆盖医疗、航空、工业制造、建筑、机器人、能源、交通、生命科学全主流赛道，完整现有技术证据链成型，封堵绝大多数细分赛道专利独占抢注路径。
提交动作：全8模块代码、Demo、文档、依赖、脚本统一暂存提交，打上版本标签 v0.3-Full12Industry 推送远程永久开源存证。

---

### 批次4（待开发，v1.0-LSG_Full_OpenSource预留结构）
仅预创建空目录，轻量化场景实现，无复杂硬件适配：
1. Meteorology-Atmosphere 大气气象分层重建
2. Archaeology-RelicScan 文物扫描逆向复原

收尾整合动作（批次4完成后执行）：
1. 全仓库Demo兼容性校验，统一接口无冲突
2. 总README完整迭代，汇总12主行业+2拓展领域、三层开源防专利约束逻辑
3. 整合 docs/Patent_Prevention_Logic.md，汇总底层公有领域声明、全行业开源覆盖、MIT附加专利约束三大法律防护体系
4. 同步更新预印本文档，绑定GitHub开源仓库链接，完成理论+代码双重公开存证闭环
5. 最终稳定版本标签 v1.0-LSG_Full_OpenSource
