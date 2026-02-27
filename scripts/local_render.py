#!/usr/bin/env python3
"""
本地渲染脚本 - 与litematic插件联动
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
import shutil
from datetime import datetime

# 添加插件路径到Python路径
plugin_path = Path(__file__).parent.parent / "core"
sys.path.insert(0, str(plugin_path))

try:
    from litemapy import Schematic
except ImportError:
    print("警告: litemapy未安装，请运行: pip install litemapy")
    sys.exit(1)


class LocalRenderer:
    """本地渲染器 - 调用插件渲染功能"""
    
    def __init__(self, litematic_dir: str = "litematic_files", 
                 output_dir: str = "previews",
                 plugin_dir: str = "."):
        self.litematic_dir = Path(litematic_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.plugin_dir = Path(plugin_dir)
        
    def find_litematic_files(self, category: str = None):
        """查找所有litematic文件"""
        if category:
            search_path = self.litematic_dir / category
        else:
            search_path = self.litematic_dir
        
        return list(search_path.glob("**/*.litematic"))
    
    def render_file(self, file_path: Path, 
                   render_2d: bool = True,
                   render_3d: bool = True) -> Optional[Dict[str, Any]]:
        """渲染单个litematic文件"""
        try:
            print(f"\n正在渲染: {file_path.name}")
            
            # 加载litematic文件
            schematic = Schematic.load(str(file_path))
            
            # 获取分类
            category = file_path.parent.name
            
            # 创建输出目录
            output_category_dir = self.output_dir / category
            output_category_dir.mkdir(parents=True, exist_ok=True)
            
            result = {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "category": category,
                "previews": {},
                "metadata": self._extract_metadata(schematic, file_path)
            }
            
            # 渲染2D预览
            if render_2d:
                preview_2d = self._render_2d(schematic, file_path, output_category_dir)
                if preview_2d:
                    result["previews"]["2d"] = str(preview_2d)
            
            # 渲染3D预览
            if render_3d:
                preview_3d = self._render_3d(schematic, file_path, output_category_dir)
                if preview_3d:
                    result["previews"]["3d"] = str(preview_3d)
            
            # 分析材料
            materials = self._analyze_materials(schematic)
            result["materials"] = materials
            
            print(f"✓ 渲染完成: {file_path.name}")
            return result
            
        except Exception as e:
            print(f"✗ 渲染失败: {file_path.name} - {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _render_2d(self, schematic: Schematic, file_path: Path, 
                    output_dir: Path) -> Optional[Path]:
        """渲染2D预览图"""
        try:
            # 尝试导入插件的2D渲染模块
            try:
                from core.image_render.render2D import Render2D
                from core.image_render.build_model import World
                
                # 创建世界对象
                world = World()
                world.add_blocks(schematic)
                
                # 创建渲染器
                renderer = Render2D(world, resource_base_path=str(self.plugin_dir / "resource"))
                
                # 渲染综合视图
                image = renderer.render_all_views(scale=2)
                
                # 保存预览图
                output_path = output_dir / f"{file_path.stem}_2d.png"
                image.save(str(output_path), "PNG")
                
                print(f"  ✓ 2D预览已生成")
                return output_path
                
            except ImportError as e:
                print(f"  ✗ 2D渲染模块未找到: {e}")
                return None
                
        except Exception as e:
            print(f"  ✗ 2D渲染失败: {e}")
            return None
    
    def _render_3d(self, schematic: Schematic, file_path: Path,
                    output_dir: Path) -> Optional[Path]:
        """渲染3D预览动画"""
        try:
            # 尝试导入插件的3D渲染模块
            try:
                from core.render_3d.pyvista_renderer import PyVistaRenderer
                from core.model_3d.model_builder import ModelBuilder
                from core.model_3d.surface_detector import SurfaceDetector
                from core.model_3d.color_mapper import ColorMapper
                from core.render_3d.animation_generator import AnimationGenerator
                
                # 创建3D模型
                model_builder = ModelBuilder()
                model_data = model_builder.build_model(schematic)
                
                # 检测表面
                surface_detector = SurfaceDetector()
                surface_data = surface_detector.detect_surfaces(model_data)
                
                # 创建颜色映射器
                color_mapper = ColorMapper()
                
                # 创建渲染器
                renderer = PyVistaRenderer(
                    model_data,
                    surface_data,
                    color_mapper,
                    resource_dir=str(self.plugin_dir / "resource")
                )
                
                # 渲染动画
                animation_gen = AnimationGenerator(renderer)
                gif_path = animation_gen.generate_animation(
                    animation_type="rotation",
                    frames=36,
                    duration=100
                )
                
                # 移动GIF文件
                output_path = output_dir / f"{file_path.stem}_3d.gif"
                shutil.move(gif_path, str(output_path))
                
                print(f"  ✓ 3D动画已生成")
                return output_path
                
            except ImportError as e:
                print(f"  ✗ 3D渲染模块未找到: {e}")
                return None
                
        except Exception as e:
            print(f"  ✗ 3D渲染失败: {e}")
            return None
    
    def _analyze_materials(self, schematic: Schematic) -> Dict[str, Any]:
        """分析材料"""
        try:
            # 尝试导入插件的材料分析模块
            try:
                from core.material.material import Material
                
                material_analyzer = Material("材料分析", 0)
                
                # 获取方块和实体统计
                block_counts = material_analyzer.block_collection(schematic)
                entity_counts = material_analyzer.entity_collection(schematic)
                tile_counts = material_analyzer.tile_collection(schematic)
                
                print(f"  ✓ 材料分析完成: {len(block_counts)} 种方块")
                
                return {
                    "total_blocks": sum(block_counts.values()),
                    "unique_blocks": len(block_counts),
                    "blocks": block_counts,
                    "entities": entity_counts,
                    "tiles": tile_counts
                }
                
            except ImportError as e:
                print(f"  ✗ 材料分析模块未找到: {e}")
                return {}
                
        except Exception as e:
            print(f"  ✗ 材料分析失败: {e}")
            return {}
    
    def _extract_metadata(self, schematic: Schematic, file_path: Path) -> Dict[str, Any]:
        """提取元数据"""
        metadata = {
            "name": file_path.stem,
            "file_name": file_path.name,
            "category": file_path.parent.name,
            "file_path": str(file_path.relative_to(self.litematic_dir)),
            "file_size": file_path.stat().st_size,
            "created_at": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "minecraft_version": getattr(schematic, 'minecraft_version', 'Unknown'),
            "regions": []
        }
        
        # 获取区域信息
        for region_name, region in schematic.regions.items():
            region_info = {
                "name": region_name,
                "position": {
                    "x": region.position.x,
                    "y": region.position.y,
                    "z": region.position.z
                },
                "size": {
                    "x": region.size.x,
                    "y": region.size.y,
                    "z": region.size.z
                },
                "volume": region.size.x * region.size.y * region.size.z
            }
            metadata["regions"].append(region_info)
        
        # 计算总体积
        total_volume = sum(r["volume"] for r in metadata["regions"])
        metadata["total_volume"] = total_volume
        metadata["estimated_block_count"] = int(total_volume * 0.7)
        
        # 检查预览图
        category = file_path.parent.name
        preview_2d = Path(f"previews/{category}/{file_path.stem}_2d.png")
        preview_3d = Path(f"previews/{category}/{file_path.stem}_3d.gif")
        
        metadata["previews"] = {
            "2d": str(preview_2d) if preview_2d.exists() else None,
            "3d": str(preview_3d) if preview_3d.exists() else None
        }
        
        return metadata
    
    def render_all(self, render_2d: bool = True, render_3d: bool = True):
        """渲染所有文件"""
        files = self.find_litematic_files()
        print(f"\n找到 {len(files)} 个litematic文件\n")
        
        results = []
        for file_path in files:
            result = self.render_file(file_path, render_2d, render_3d)
            if result:
                results.append(result)
        
        return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="本地渲染litematic文件")
    parser.add_argument("--file", help="渲染单个文件")
    parser.add_argument("--category", help="渲染指定分类")
    parser.add_argument("--litematic-dir", default="litematic_files",
                       help="litematic文件目录")
    parser.add_argument("--output-dir", default="previews",
                       help="输出目录")
    parser.add_argument("--no-2d", action="store_true",
                       help="不渲染2D预览")
    parser.add_argument("--no-3d", action="store_true",
                       help="不渲染3D预览")
    
    args = parser.parse_args()
    
    # 创建渲染器
    renderer = LocalRenderer(
        litematic_dir=args.litematic_dir,
        output_dir=args.output_dir
    )
    
    render_2d = not args.no_2d
    render_3d = not args.no_3d
    
    # 渲染文件
    if args.file:
        file_path = Path(args.file)
        result = renderer.render_file(file_path, render_2d, render_3d)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.category:
        category_dir = Path(args.litematic_dir) / args.category
        files = list(category_dir.glob("*.litematic"))
        for file_path in files:
            renderer.render_file(file_path, render_2d, render_3d)
    else:
        renderer.render_all(render_2d, render_3d)


if __name__ == "__main__":
    main()
