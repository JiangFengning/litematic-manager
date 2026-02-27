# Litematic文件管理系统

基于GitHub Actions + GitHub Pages的完全免费的litematic文件管理系统。

## 功能特性

- 📁 文件管理：按分类组织litematic文件
- 📸 2D预览：自动生成俯视图、正视图、侧视图
- 🧊 3D预览：自动生成3D旋转动画
- 🧱 材料分析：自动统计方块和实体
- 📊 元数据展示：显示文件尺寸、版本、作者等信息
- 🌐 静态网站：通过GitHub Pages提供全球访问

## 快速开始

### 1. 添加litematic文件

将你的.litematic文件复制到对应的分类目录：

```bash
# 建筑类文件
cp "你的建筑.litematic" litematic_files/建筑/

# 红石类文件
cp "你的红石装置.litematic" litematic_files/红石/

# 装饰类文件
cp "你的装饰.litematic" litematic_files/装饰/
```

### 2. 提交到Git

```bash
git add litematic_files/
git commit -m "添加新文件"
git push origin main
```

### 3. 等待自动渲染

推送代码后，GitHub Actions会自动：
1. 渲染2D预览图
2. 渲染3D预览动画
3. 分析材料统计
4. 生成元数据
5. 生成静态网站
6. 部署到GitHub Pages

### 4. 访问网站

等待5-10分钟后，访问：
```
https://JiangFengning.github.io/litematic-manager/
```

## 项目结构

```
litematic-manager/
├── .github/workflows/    # GitHub Actions工作流
├── litematic_files/       # litematic文件存储
│   ├── 建筑/
│   ├── 红石/
│   └── 装饰/
├── scripts/              # 渲染脚本
├── templates/            # 网站模板
├── data/                 # 元数据存储
└── previews/             # 预览图存储（自动生成）
```

## 技术栈

- **前端**: HTML + CSS + JavaScript
- **后端**: Python 3.10
- **渲染**: Pillow + PyVista
- **解析**: litemapy
- **部署**: GitHub Actions + GitHub Pages

## 当前状态

- ✅ 项目结构已创建
- ✅ GitHub Actions工作流已配置
- ✅ 代码已推送到GitHub
- ✅ 渲染脚本已修复
- ⏳ 等待配置GitHub Pages

## 下一步

1. 访问 https://github.com/JiangFengning/litematic-manager/settings/pages
2. 配置GitHub Pages（选择"GitHub Actions"作为Source）
3. 等待Actions工作流完成
4. 访问网站验证功能

## 许可证

MIT License
