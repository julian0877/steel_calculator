# 钢结构算量软件部署指南索引

欢迎使用钢结构算量软件部署指南。本索引将帮助您找到所有相关的部署文档，以便将您的应用部署到云端，让其他人可以随时访问而不依赖于您的本地机器。

## 部署指南文档

1. [**部署方案比较**](deployment_comparison.md) - 比较不同部署选项的优缺点，帮助您选择最适合的方案

2. [**Streamlit Cloud 详细指南**](streamlit_cloud_guide.md) - 最推荐的部署方式，完整的步骤说明

3. [**Streamlit Cloud 截图指南**](streamlit_cloud_screenshots.md) - 关键步骤的截图说明

4. [**Streamlit Cloud 故障排除**](streamlit_cloud_troubleshooting.md) - 解决 Streamlit Cloud 部署中常见问题

5. [**其他部署方案指南**](deployment_guide.md) - 包括 Heroku、VPS 和 Docker 部署的基本说明

## 快速入门

如果您想快速部署您的应用，我们建议使用 **Streamlit Cloud**，这是最简单且免费的选项。请按照以下步骤操作：

1. 阅读 [部署方案比较](deployment_comparison.md) 确认 Streamlit Cloud 适合您的需求
2. 按照 [Streamlit Cloud 详细指南](streamlit_cloud_guide.md) 中的步骤操作
3. 参考 [Streamlit Cloud 截图指南](streamlit_cloud_screenshots.md) 获取视觉辅助
4. 如果遇到问题，查阅 [Streamlit Cloud 故障排除](streamlit_cloud_troubleshooting.md)

## 所需文件

我们已经为您准备了部署所需的所有配置文件：

- `requirements.txt` - 列出应用所需的 Python 依赖
- `Procfile` - Heroku 部署所需的配置文件
- `setup.sh` - Heroku 部署的设置脚本
- `Dockerfile` - Docker 容器化部署配置

## 部署后维护

部署应用后，您可能需要：

1. **更新应用**：修改代码后推送到 GitHub，Streamlit Cloud 会自动重新部署
2. **监控使用情况**：检查应用的访问情况和性能
3. **处理问题**：参考故障排除指南解决可能出现的问题

## 结论

通过这些指南，您可以轻松地将钢结构算量软件部署到云端，让其他人可以随时访问，而不依赖于您的本地机器。如果您有任何问题，请参考相应的故障排除指南。
