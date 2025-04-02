# Streamlit Cloud 部署详细指南

Streamlit Cloud 是部署 Streamlit 应用最简单的方式，完全免费且无需服务器管理。以下是详细的步骤指南：

## 1. 准备 GitHub 仓库

首先，您需要将您的应用代码上传到 GitHub 仓库：

### 1.1 创建 GitHub 账户（如果没有）

1. 访问 [GitHub](https://github.com/)
2. 点击 "Sign up" 并按照指示创建账户

### 1.2 创建新仓库

1. 登录 GitHub
2. 点击右上角的 "+" 图标，选择 "New repository"
3. 输入仓库名称，如 "steel-calculator"
4. 选择 "Public"（Streamlit Cloud 需要公开仓库，除非您使用付费版本）
5. 点击 "Create repository"

### 1.3 准备本地代码

确保您的项目结构如下：

```
steel-calculator/
├── web/
│   └── steel_calculator.py
├── requirements.txt
└── README.md (可选)
```

### 1.4 创建 requirements.txt 文件

确保 requirements.txt 包含所有必要的依赖：

```
streamlit==1.32.0
pandas==2.1.4
xlsxwriter==3.1.2
```

### 1.5 将代码推送到 GitHub

在命令行中执行以下命令：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit"

# 设置主分支名称
git branch -M main

# 添加远程仓库
git remote add origin https://github.com/您的用户名/steel-calculator.git

# 推送代码到 GitHub
git push -u origin main
```

## 2. 在 Streamlit Cloud 上部署应用

### 2.1 注册 Streamlit Cloud

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 点击 "Continue with GitHub" 使用您的 GitHub 账户登录
3. 授权 Streamlit 访问您的 GitHub 账户

### 2.2 创建新应用

1. 登录后，点击右上角的 "New app" 按钮
2. 在 "Repository" 下拉菜单中选择您的 "steel-calculator" 仓库
3. 在 "Branch" 中选择 "main"
4. 在 "Main file path" 中输入 "web/steel_calculator.py"
5. 高级设置（可选）：
   - 可以设置 Python 版本（默认为 3.9）
   - 可以添加环境变量（如果您的应用需要）
   - 可以设置包管理器（pip 或 conda）
6. 点击 "Deploy!" 按钮

### 2.3 等待部署完成

1. Streamlit Cloud 将开始构建您的应用
2. 您可以在构建日志中查看进度
3. 部署通常需要 2-5 分钟完成

### 2.4 访问您的应用

部署完成后，您的应用将在以下 URL 可用：
```
https://[您的用户名]-steel-calculator-web-steel-calculator-[随机字符].streamlit.app
```

您可以通过点击 "View app" 按钮或直接访问该 URL 来查看您的应用。

## 3. 管理您的 Streamlit 应用

### 3.1 查看应用状态

1. 在 Streamlit Cloud 仪表板中，您可以看到所有已部署的应用
2. 每个应用都显示其当前状态（运行中、休眠、错误等）

### 3.2 更新应用

当您推送新的更改到 GitHub 仓库时，Streamlit Cloud 会自动重新部署您的应用：

1. 在本地修改代码
2. 提交并推送更改到 GitHub：
   ```bash
   git add .
   git commit -m "更新应用"
   git push
   ```
3. Streamlit Cloud 将自动检测更改并重新部署

### 3.3 应用设置

在应用页面中，点击右上角的 "⋮" 菜单，您可以：

1. 重启应用
2. 查看构建日志
3. 管理环境变量
4. 设置应用休眠时间（免费版默认为不活动 7 天后休眠）
5. 删除应用

### 3.4 应用休眠与唤醒

- 免费版 Streamlit Cloud 应用在不活动一段时间后会自动休眠
- 当有人访问休眠的应用时，它会自动唤醒（可能需要几秒钟）
- 唤醒后，应用将正常运行，就像在您的本地机器上一样

## 4. Streamlit Cloud 的限制与注意事项

### 4.1 免费版限制

- 公开仓库限制（私有仓库需要付费版本）
- 每个账户最多 3 个应用
- 应用不活动 7 天后自动休眠
- 有计算资源限制（但对于大多数应用足够）

### 4.2 安全注意事项

- 不要在代码中硬编码敏感信息（如密码、API 密钥）
- 使用 Streamlit Cloud 的环境变量功能存储敏感信息
- 记住您的应用是公开的，任何人都可以访问

### 4.3 性能优化

- 尽量减少应用的启动时间
- 考虑使用缓存（@st.cache_data 装饰器）来提高性能
- 大型数据集考虑使用云存储而非直接包含在仓库中

## 5. 故障排除

### 5.1 部署失败

如果部署失败，请检查：

1. requirements.txt 是否包含所有必要的依赖
2. 主文件路径是否正确
3. 查看构建日志以获取详细错误信息

### 5.2 应用错误

如果应用部署成功但运行出错：

1. 在本地测试应用确保其正常工作
2. 检查是否有路径问题（本地路径与云端可能不同）
3. 检查是否有环境变量缺失

### 5.3 常见问题

- **ImportError**: 检查 requirements.txt 是否包含所有依赖
- **FileNotFoundError**: 检查文件路径是否正确
- **MemoryError**: 应用可能超出了资源限制，尝试优化代码

## 6. 结论

Streamlit Cloud 是部署 Streamlit 应用最简单的方式，特别适合个人项目、演示和小型应用。通过遵循上述步骤，您可以轻松地将您的钢结构算量软件部署到云端，让其他人随时访问，而无需依赖您的本地机器。
