# Litematic文件管理系统

基于本地渲染、与litematic插件联动、GitHub Pages提供外网访问的文件管理系统。

## 📋 功能特性

- 📁 文件管理（分类、标签、搜索）
- 📸 2D/3D预览（本地渲染）
- 🧱 材料分析（自动统计）
- 🌐 Web访问（GitHub Pages）
- ⬇️ 文件下载（直接下载）
- 🔄 版本控制（Git管理）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install litemapy Pillow pyvista numpy pandas jinja2 tqdm pyyaml
```

### 2. 配置

编辑 `config.json` 文件，配置GitHub仓库信息。

### 3. 上传文件

将litematic文件复制到对应的分类目录：

```bash
cp "你的文件.litematic" litematic_files/建筑/
```

### 4. 本地渲染

```bash
python scripts/local_render.py --file "litematic_files/建筑/你的文件.litematic"
```

### 5. 生成网站

```bash
python scripts/generate_site.py
```

### 6. 上传到GitHub

```bash
python scripts/auto_upload.py --file "litematic_files/建筑/你的文件.litematic" --category "建筑"
```

### 7. 访问网站

等待几分钟后，访问你的GitHub Pages地址。

## 📁 项目结构

```
litematic-manager/
├── litematic_files/          # litematic文件存储
├── previews/                # 预览图存储
├── data/                    # 元数据存储
├── scripts/                 # 自动化脚本
├── templates/               # 网站模板
└── site/                    # 生成的静态网站
```

## 🔧 脚本说明

### local_render.py
本地渲染脚本，调用插件的渲染功能生成预览图。

### auto_upload.py
自动上传脚本，将文件和预览图上传到GitHub。

### generate_site.py
静态网站生成脚本，生成HTML页面。

## 📄 许可证

MIT License
