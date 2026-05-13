# 贡献者指南 & 贡献者许可协议 (CLA)
# Contributor Guide & Contributor License Agreement (CLA)

> **Language / 语言**: 本文档采用中英双语对照撰写，如有歧义，以中文版本为准。  
> This document is written in bilingual format. In case of ambiguity, the Chinese version shall prevail.

---

## 一、欢迎贡献 / Welcome

感谢您对本项目「灵境行者 (Spirit Journey Rider)」的关注！我们欢迎并感谢所有形式的贡献，包括但不限于代码提交、文档改进、Bug 报告、功能建议、UI 设计、翻译工作等。

Thank you for your interest in the "Spirit Journey Rider" project! We welcome and appreciate all forms of contributions, including but not limited to code commits, documentation improvements, bug reports, feature suggestions, UI design, and translation work.

---

## 二、如何贡献 / How to Contribute

### 2.1 提交 Issue / Submitting Issues

- 在提交新 Issue 前，请先搜索是否已有重复问题。
- 请使用对应的 Issue 模板，尽可能提供复现步骤、环境信息和截图。
- 安全漏洞请通过邮件私下报告至 `925342921@qq.com`，勿公开提交。

Before submitting a new Issue, please search for duplicates. Use the appropriate issue template and provide reproduction steps, environment info, and screenshots. Security vulnerabilities should be reported privately via email to `925342921@qq.com`.

### 2.2 提交 Pull Request / Submitting Pull Requests

1. **Fork** 本仓库并克隆到本地。  
   Fork this repository and clone it locally.
2. 基于 `develop` 分支创建功能分支：`git checkout -b feature/your-feature-name`。  
   Create a feature branch based on `develop`: `git checkout -b feature/your-feature-name`.
3. 遵循项目的代码规范（见第三节）进行开发。  
   Follow the project's coding standards (see Section 3).
4. 确保本地测试通过，提交信息符合规范（见第四节）。  
   Ensure local tests pass and commit messages follow conventions (see Section 4).
5. 提交 PR 至 `develop` 分支，并填写 PR 模板。  
   Submit the PR to the `develop` branch and fill out the PR template.
6. 维护者将进行 Code Review，可能需要你进行修改。  
   Maintainers will conduct code review; modifications may be requested.

---

## 三、代码规范 / Coding Standards

| 技术栈 / Tech Stack | 规范标准 / Standard | 工具 / Tools |
|---|---|---|
| Vue3 前端 / Frontend | Vue3 官方风格指南 / Vue3 Style Guide | ESLint + Prettier |
| Java 后端 / Backend | Spring Boot 最佳实践 / Spring Boot Best Practices | Checkstyle + SpotBugs |
| Python 爬虫 / Crawler | PEP 8 | Black + Flake8 |

- 所有代码注释和文档优先使用中文，关键术语附英文对照。  
  All code comments and docs should primarily use Chinese, with English equivalents for key terms.
- 新增功能必须附带对应的单元测试。  
  New features must include corresponding unit tests.
- 禁止提交敏感信息（API Key、密码、私钥等）。  
  Do not commit sensitive information (API keys, passwords, private keys).

---

## 四、提交信息规范 / Commit Message Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 / Types:**
- `feat`: 新功能 / New feature
- `fix`: 修复 Bug / Bug fix
- `docs`: 文档更新 / Documentation
- `style`: 代码格式 / Formatting
- `refactor`: 重构 / Refactoring
- `test`: 测试 / Tests
- `chore`: 构建/工具 / Build/tools

**示例 / Example:**
```
feat(route): 添加骑行路径规划功能

- 集成高德地图骑行路线 API
- 支持速度优先、距离优先策略
- 添加路线缓存机制

Closes #123
```

---

## 五、贡献者许可协议 (CLA) / Contributor License Agreement

> ⚠️ **重要 / IMPORTANT**: 向本项目提交任何贡献（包括但不限于代码、文档、设计、翻译，以下统称"贡献"），即表示您已阅读、理解并同意以下条款。  
> By submitting any contribution (including but not limited to code, documentation, design, translation, collectively "Contributions") to this project, you acknowledge that you have read, understood, and agree to the following terms.

### 5.1 著作权转让 / Copyright Assignment

您同意将您对本项目所提交的全部贡献的**全部著作权**（包括但不限于复制权、修改权、发行权、信息网络传播权、改编权等著作人身权与财产权）**无偿、永久、不可撤销地转让给本项目著作权人（河北经贸大学 灵境行者团队，以下简称"项目方"）**。

You agree to assign all copyright interests in your Contributions (including but not limited to the rights of reproduction, modification, distribution, information network dissemination, adaptation, and other moral and economic rights) **gratuitously, perpetually, and irrevocably to the copyright holder of this project (Hebei University of Economics and Business, Spirit Journey Rider Team, hereinafter "the Project Owner")**.

**转让目的 / Purpose of Assignment:**
本项目采用**双重许可模式（Dual Licensing）**——非商业用途免费开源，商业用途需付费授权。为实现统一的许可管理，项目方必须拥有完整的著作权，以便同时行使开源许可与商业授权。

This project adopts a **Dual Licensing model** — free and open source for non-commercial use, and commercial use requires a paid license. To enable unified license management, the Project Owner must hold complete copyright to exercise both open-source and commercial licenses.

### 5.2 保留权利 / Reserved Rights

- **署名权 / Moral Right of Attribution**: 项目方承诺通过 Git Commit 记录保留您的署名。您有权在贡献中被识别为作者。  
  The Project Owner promises to preserve your attribution through Git commit records. You have the right to be identified as the author of your contribution.
- **收益分成 / Revenue Sharing** (可选 / Optional): 若您希望保留商业授权收益分成权利，请在**首次贡献前**通过邮件书面联系项目方另行约定。未事先约定的，视为放弃此项权利。  
  If you wish to retain revenue-sharing rights from commercial licensing, you must contact the Project Owner in writing via email **before your first contribution**. Without prior agreement, this right is deemed waived.

### 5.3 保证与声明 / Representations and Warranties

您声明并保证：

You represent and warrant that:

1. **原创性 / Originality**: 您提交的贡献是您的原创作品，或您已获得原始著作权人的充分授权，可以按本协议条款转让给项目方。  
   Your Contributions are your original creation, or you have obtained sufficient authorization from the original copyright holder to assign them to the Project Owner under these terms.
2. **无侵权 / Non-infringement**: 您的贡献不侵犯任何第三方的知识产权、商业秘密、隐私权或其他合法权益。  
   Your Contributions do not infringe upon any third party's intellectual property rights, trade secrets, privacy rights, or other lawful interests.
3. **无已知限制 / No Known Restrictions**: 据您所知，您的贡献不受任何第三方许可协议、雇佣合同或学术机构政策的限制，导致无法按本协议转让。  
   To your knowledge, your Contributions are not restricted by any third-party license agreement, employment contract, or academic institutional policy that would prevent assignment under this Agreement.

### 5.4 责任限制 / Limitation of Liability

对于因您违反上述保证而给项目方或第三方造成的任何损失，您应承担全部赔偿责任。项目方保留追究您法律责任的权利。

You shall bear full liability for any losses caused to the Project Owner or third parties due to your breach of the above warranties. The Project Owner reserves the right to pursue legal remedies.

### 5.5 协议生效 / Agreement Effectiveness

**您向本项目提交 Pull Request、Issue、代码补丁、文档或其他任何形式的贡献之时，即视为您已签署本 CLA，本协议立即生效。**

**By submitting a Pull Request, Issue, code patch, documentation, or any other form of contribution to this project, you are deemed to have signed this CLA, and this Agreement takes effect immediately.**

---

## 六、联系方式 / Contact

- **项目负责人 / Project Lead**: 陈冠衡 (Chen Guanheng)
- **邮箱 / Email**: 925342921@qq.com
- **所属院校 / Institution**: 河北经贸大学 / Hebei University of Economics and Business
- **项目地址 / Repository**: https://github.com/qingxuandaoming/Intangible_Cultural_Heritage_Cycling_Tour

---

**最后更新 / Last Updated**: 2025年5月  
*灵境行者团队 版权所有 / Copyright © Spirit Journey Rider Team*
