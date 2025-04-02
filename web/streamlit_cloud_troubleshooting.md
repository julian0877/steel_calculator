# Streamlit Cloud 部署故障排除指南

在部署 Streamlit 应用到 Streamlit Cloud 的过程中，您可能会遇到一些常见问题。本指南将帮助您识别和解决这些问题。

## 1. 部署失败问题

### 1.1 依赖问题

**症状**: 部署日志显示 `ModuleNotFoundError` 或 `ImportError`

**解决方案**:
1. 检查 `requirements.txt` 文件是否包含所有必要的依赖
2. 确保依赖版本兼容
3. 更新 `requirements.txt` 并重新推送到 GitHub

**示例错误**:
```
ModuleNotFoundError: No module named 'xlsxwriter'
```

**修复**:
确保 `requirements.txt` 包含:
```
xlsxwriter==3.1.2
```

### 1.2 Python 版本问题

**症状**: 部署日志显示语法错误或不兼容的功能

**解决方案**:
1. 在 Streamlit Cloud 的高级设置中指定与您本地开发环境相匹配的 Python 版本
2. 或者修改代码以兼容 Streamlit Cloud 默认的 Python 版本 (3.9)

**示例错误**:
```
SyntaxError: invalid syntax (feature only available in Python 3.10+)
```

**修复**:
在 Streamlit Cloud 部署设置中将 Python 版本设置为 3.10 或更高

### 1.3 文件路径问题

**症状**: 找不到文件或模块

**解决方案**:
1. 确保在 "Main file path" 中指定了正确的路径 (例如 "web/steel_calculator.py")
2. 确保所有导入使用相对路径而非绝对路径

**示例错误**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'web/steel_calculator.py'
```

**修复**:
检查仓库结构，确保文件路径与指定的主文件路径匹配

## 2. 应用运行问题

### 2.1 应用启动但显示错误

**症状**: 应用加载但显示 Streamlit 错误消息

**解决方案**:
1. 查看错误消息以确定具体问题
2. 在本地测试应用，确保它在本地运行正常
3. 检查是否有依赖于本地文件系统的代码

**示例错误**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'local_data.csv'
```

**修复**:
修改代码以使用相对路径或将数据文件包含在仓库中

### 2.2 应用加载缓慢

**症状**: 应用需要很长时间才能加载

**解决方案**:
1. 优化代码，特别是应用启动时执行的代码
2. 使用 `@st.cache_data` 装饰器缓存数据加载和处理函数
3. 减少不必要的依赖

**示例优化**:
```python
# 优化前
def load_data():
    # 耗时的数据处理
    return processed_data

# 优化后
@st.cache_data
def load_data():
    # 相同的数据处理，但结果会被缓存
    return processed_data
```

### 2.3 会话状态问题

**症状**: 应用状态不保持，用户输入丢失

**解决方案**:
1. 确保正确使用 `st.session_state` 来存储会话数据
2. 了解 Streamlit 的执行模型（每次交互都会重新运行脚本）

**示例修复**:
```python
# 初始化会话状态
if 'components' not in st.session_state:
    st.session_state.components = []

# 使用会话状态存储数据
if st.button("添加构件"):
    st.session_state.components.append(comp_data)
```

## 3. 资源限制问题

### 3.1 内存错误

**症状**: 应用崩溃，日志显示内存错误

**解决方案**:
1. 减少内存使用，特别是大型数据结构
2. 使用流式处理而非一次性加载大量数据
3. 优化算法和数据结构

**示例错误**:
```
MemoryError: ...
```

**修复**:
分批处理数据或减少同时加载的数据量

### 3.2 计算超时

**症状**: 长时间运行的操作导致应用超时

**解决方案**:
1. 优化计算密集型操作
2. 将长时间运行的任务拆分为更小的步骤
3. 考虑预计算结果并存储

**示例优化**:
将复杂计算拆分为多个步骤，让用户可以分阶段执行

## 4. 环境变量和配置问题

### 4.1 缺少环境变量

**症状**: 应用尝试访问未定义的环境变量

**解决方案**:
1. 在 Streamlit Cloud 的应用设置中添加必要的环境变量
2. 为环境变量提供默认值

**示例代码**:
```python
import os
api_key = os.environ.get("API_KEY", "default_key")  # 提供默认值
```

### 4.2 配置文件问题

**症状**: 应用无法找到或加载配置文件

**解决方案**:
1. 将配置直接包含在代码中
2. 使用环境变量而非配置文件
3. 确保配置文件包含在仓库中并使用相对路径

## 5. 更新和维护问题

### 5.1 更新不生效

**症状**: 推送更改到 GitHub 后，应用没有更新

**解决方案**:
1. 确认更改已成功推送到正确的分支
2. 检查 Streamlit Cloud 构建日志
3. 手动重新部署应用

**验证步骤**:
1. 在 GitHub 上检查您的仓库，确认更改已推送
2. 在 Streamlit Cloud 仪表板中，点击应用的 "⋮" 菜单，选择 "Reboot app"

### 5.2 应用自动休眠

**症状**: 应用在一段时间不活动后变得不可用

**解决方案**:
这是 Streamlit Cloud 免费版的正常行为。应用在不活动 7 天后会自动休眠，当有人访问时会自动唤醒（可能需要几秒钟）。

如果需要应用始终运行：
1. 升级到 Streamlit Cloud 的付费版本
2. 或使用其他托管服务，如 Heroku、AWS 等

## 6. 浏览器兼容性问题

**症状**: 应用在某些浏览器中显示不正确

**解决方案**:
1. 测试应用在不同浏览器中的表现
2. 避免使用特定浏览器的功能
3. 添加浏览器兼容性检查

## 7. 联系 Streamlit 支持

如果您尝试了上述所有解决方案但问题仍然存在，可以联系 Streamlit 支持：

1. 访问 [Streamlit 论坛](https://discuss.streamlit.io/)
2. 在 [GitHub Issues](https://github.com/streamlit/streamlit/issues) 上报告问题
3. 联系 Streamlit 支持团队 (support@streamlit.io)

提供问题的详细描述、错误消息和重现步骤，以便获得更有效的帮助。

## 结论

大多数 Streamlit Cloud 部署问题都与依赖管理、文件路径或资源限制有关。通过仔细检查这些方面，您通常可以解决大部分问题。记住，在本地测试应用是确保顺利部署的关键步骤。
