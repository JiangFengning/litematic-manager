#!/usr/bin/env python3
"""
测试脚本 - 验证插件集成
"""

import sys
from pathlib import Path

# 获取正确的插件路径（父目录的core文件夹）
current_dir = Path(__file__).parent.parent
plugin_path = current_dir.parent / "core"

print("测试插件模块导入...")
print(f"当前目录: {current_dir}")
print(f"插件路径: {plugin_path}")
print()

# 测试1: 导入litemapy
print("测试1: 导入litemapy")
try:
    from litemapy import Schematic
    print("✓ litemapy导入成功")
except ImportError as e:
    print(f"✗ litemapy导入失败: {e}")
    print("请运行: pip install litemapy")
    sys.exit(1)
print()

# 测试2: 导入2D渲染模块
print("测试2: 导入2D渲染模块")
try:
    sys.path.insert(0, str(plugin_path))
    from core.image_render.render2D import Render2D
    from core.image_render.build_model import World
    print("✓ 2D渲染模块导入成功")
except ImportError as e:
    print(f"✗ 2D渲染模块导入失败: {e}")
    print(f"请检查插件路径是否正确: {plugin_path}")
print()

# 测试3: 导入3D渲染模块
print("测试3: 导入3D渲染模块")
try:
    from core.render_3d.pyvista_renderer import PyVistaRenderer
    from core.model_3d.model_builder import ModelBuilder
    from core.model_3d.surface_detector import SurfaceDetector
    from core.model_3d.color_mapper import ColorMapper
    from core.render_3d.animation_generator import AnimationGenerator
    print("✓ 3D渲染模块导入成功")
except ImportError as e:
    print(f"✗ 3D渲染模块导入失败: {e}")
    print(f"请检查插件路径是否正确: {plugin_path}")
print()

# 测试4: 导入材料分析模块
print("测试4: 导入材料分析模块")
try:
    from core.material.material import Material
    print("✓ 材料分析模块导入成功")
except ImportError as e:
    print(f"✗ 材料分析模块导入失败: {e}")
    print(f"请检查插件路径是否正确: {plugin_path}")
print()

# 测试5: 检查litematic文件
print("测试5: 检查litematic文件")
litematic_dir = Path("litematic_files")
if not litematic_dir.exists():
    print(f"✗ litematic目录不存在: {litematic_dir}")
    print("请先创建litematic目录并添加文件")
else:
    files = list(litematic_dir.glob("**/*.litematic"))
    print(f"✓ 找到 {len(files)} 个litematic文件")
    if len(files) == 0:
        print("提示: 目录为空，请添加litematic文件")
    else:
        print("文件列表:")
        for file in files[:5]:  # 只显示前5个
            print(f"  - {file}")
        if len(files) > 5:
            print(f"  ... 还有 {len(files) - 5} 个文件")
print()

print("=" * 50)
print("测试完成！")
print("=" * 50)
print()
print("如果所有测试都通过，你可以运行:")
print("  python scripts/local_render.py --help")
print()
print("查看可用的渲染选项")
