# 🎯 考试题库自动下载与解密工具

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://python.org) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

> ⚠️ **免责声明**: 本代码仅用于参考和学习，造成的其他影响，与作者无关。

## 📋 项目简介

这是一个基于 Python 的考试题库自动化处理工具，专门用于从在线考试系统下载题库数据并解密其中的字体加密内容。该工具能够突破在线考试系统的字体反爬虫机制，将加密的题目内容转换为可读格式。

### ✨ 核心功能

- 🔍 **智能题库下载**: 自动化从在线考试系统获取题目数据
- 🔓 **字体解密技术**: 突破字体加密保护，还原真实题目内容
- 📊 **数据结构化**: 将原始数据转换为结构化的 JSON 格式
- 🎨 **多平台支持**: 支持 Windows 和 Linux 操作系统
- 🚀 **高效处理**: 使用多线程和进度条提升用户体验

## 🛠️ 技术架构

### 技术栈
- **语言**: Python 3.10+
- **核心库**:
  - `fonttools`: 字体文件处理和分析
  - `requests`: HTTP 请求处理
  - `beautifulsoup4`: HTML 内容解析
  - `tqdm`: 进度条显示
  - `hashlib`: 字形哈希计算

### 核心模块

| 模块 | 功能 | 描述 |
|------|------|------|
| `app.py` | 主程序入口 | 协调整个解密流程 |
| `FontDecryption.py` | 字体解密引擎 | 字形哈希计算和映射构建 |
| `solutionData.py` | 数据解析器 | 题目数据提取和格式化 |
| `fontDownload.py` | 字体下载器 | 从远程服务器下载加密字体文件 |

## 🚀 快速开始

### 环境准备

1. **克隆项目**
   ```bash
   git clone https://github.com/happy-join-github/KaoShiBao.git
   cd kaoshibao
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .env
   ```

3. **激活虚拟环境**
   
   Windows:
   ```bash
   .env\Scripts\Activate.ps1
   ```
   
   Linux/Mac:
   ```bash
   source .env/bin/activate
   ```

4. **安装依赖**
   ```bash
   pip install -r requirement.txt
   ```

### 使用步骤

1. **手动登录系统**
   - 打开浏览器，访问考试系统 [官网](https://www.kaoshibao.com/)

   - 使用账号密码登录

   

2. **开始数据获取**
   - 找到你要下载的题库

   - 点击题库名称，进入题库详情页面

   - 停在题库详情页面，按下 F12 打开开发者工具

   - 在console中输入下面的内容

     - ```javascript
       const axiosInstance = window.$nuxt.$axios;window.DecryptedQuestions=[];axiosInstance.interceptors.response.use(function (response) {if (response.config && response.config.url && response.config.url.includes('/questions/ids')) {console.log('%c=== 成功捕获解密后的明文数据 ===', 'color:white;background:#67c23a;font-size:16px;padding:10px;border-radius:5px;font-weight:bold;');if (Array.isArray(response.data.data)){window.DecryptedQuestions.push(response.data)}}return response;}, function (error) {return Promise.reject(error);});console.log("%c 注入完成",'color:white;background:#67c23a;font-size:16px;padding:10px;border-radius:5px;font-weight:bold;');
       ```

     - 当控制台输出注入成功，即为成功。如下图所示

     - ![success](https://github.com/happy-join-github/KaoShiBao/blob/main/explain/hook.png)

   - 点击顺序/随机练习，每次获取10题目，所以每次点击20，30，40，50……

   - 假设我们就要六十个题目

     -![dataImg](https://github.com/happy-join-github/KaoShiBao/blob/main/explain/hookData.png)

     - 在控制台(console)输入

       ```bash
       copy(window.DecrypteQuestions)
       ```

       ![copydata](https://github.com/happy-join-github/KaoShiBao/blob/main/explain/copydata.png)
   - 打开本文件夹，找到 `title.json` 文件，使用 `ctrl+V` 或者右键粘贴复制的数据

3. **启动主程序**
   ```bash
   python app.py
   ```
注意: 每次运行前，请确保title.json文件是空的。每次运行完程序，解析的数据保存到result文件夹下相应日期文件夹下的titleData_decrypted.json文件中。可视化的html文件保存到result文件夹下相应日期文件夹下的questions.html文件中。

## 📁 项目结构

```
kaoshibao/
├── app.py                    # 主程序入口
├── requirement.txt            # 依赖包列表
├── utils/                    # 工具模块
│   ├── FontDecryption.py      # 字体解密核心算法
│   ├── solutionData.py        # 数据解析处理
│   └── export.py            # 数据导出工具
├── fonts/                   # 字体文件存储
│   ├── fontDownload.py        # 字体下载器
│   ├── MSYH.TTC             # 微软雅黑基准字体
│   └──msyh_glyph_hashes.json  # 字形哈希映射表
├── result/                  # 处理结果输出
│   ├── 2025-06-01/            # 日期文件夹
│   │   ├── titleData_decrypted.json  # 解密后的数据
│   │   └── questions.html    # 可视化HTML文件
├── explain/                 # 使用说明图片
└── readme.md                # 项目说明文档
```

## 📊 输出格式

解密后的数据以结构化 JSON 格式保存：

```json
{
  "question": "采切轻向上象方法进行软件开发时...",
  "qtype": "1",
  "options": [
    {"Key": "A", "Value": "汽车和座位"},
    {"Key": "B", "Value": "汽车和车窗"},
    {"Key": "C", "Value": "汽车和发动机"},
    {"Key": "D", "Value": "汽车和音乐系统"}
  ],
  "answer": "D",
  "analysis": "这道题考查面向对象方法中组成关系的理解...",
  "decrypted_question": "采用面向对象方法进行软件开发时...",
  "special_font": "k9fddb066cb69ed65a1c9dbcc23f75f09"
}
```

## ⚡ 性能特点

- **高效解密**: 基于字形哈希的快速映射算法
- **批量处理**: 支持大量题目的并发解密
- **内存优化**: 流式处理大数据文件
- **错误恢复**: 完善的异常处理机制

## 🎯 应用场景

- 📚 **教育资源收集**: 教学资料和题库整理
- 🔬 **技术研究**: 字体加密和反爬虫机制研究
- 📝 **内容分析**: 考试题目数据分析和统计

## 📄 许可证

本项目采用 MIT 许可证。

## ⚠️ 免责声明

- 本工具仅供学习和研究使用
- 请遵守相关法律法规和网站使用条款
- 作者不承担任何滥用责任
- 使用本工具产生的任何后果由用户自行承担

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
