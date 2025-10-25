# AI-hospital

## 功能（v0.0.1）：

1. 多模态输入
   - 图像输入
     - X-ray/CT等 mimic中包含的图像模态(png/jpg)
     - 患者拍照的医嘱图像（需要使用OCR----待定，可留接口）
   - 文本输入（report--txt/pdf）
   - 语音输入

2. 实时聊天功能
   - （待补充具体内容）

3. 疾病诊断+格式化report输出

4. 多科室会诊

5. 患者历史记录管理


## 具体过程：

phase 0:
1. 数据集重构
   - 用LLM+Agent对mimic原始数据进行处理，该处理包括数据结构的转换（csv--->json）和数据清洗（待定）。形成新的更时候大模型操作的医疗数据集
   - 先使用mimic-iv-demo进行实验
   - 具体步骤：待定

2. 数据操作
  - RAG（检索增强）: 将重构的MIMIC数据作为医疗知识库，实时检索相关病例
  - Few-shot Learning: 将典型病例作为示例输入给LLM

3. 增强LLM输出（可以由多个大模型组合，暂定使用大模型API，不涉及本地部署以及后训练 -v0.0.1）
   - ReAct + Multi-Agent
   - ReAct:
   - Multi-Agent:

4. 系统集成和优化：
   - 用MIMIC数据进行系统验证
   - 基于反馈进行持续优化
   

## 疑问：
1. 框架搭建： langgraph 还是 自己搭建状态机呢？
2. workflow
3. mimic数据该怎么用
4. 选用什么样子的模型呢？