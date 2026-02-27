#!/usr/bin/env python3
"""
litematic文件预览图渲染脚本
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import json
from tqdm import tqdm

try:
    from litemapy import Schematic
    from PIL import Image
    import numpy as np
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)


class LitematicRenderer:
    """litematic文件渲染器"""
    
    def __init__(self, litematic_dir: str = "litematic_files", 
                 output_dir: str = "previews"):
        self.litematic_dir = Path(litematic_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def find_litematic_files(self, category: str = None) -> List[Path]:
        """查找所有litematic文件"""
        if category:
            search_path = self.litematic_dir / category
        else:
            search_path = self.litematic_dir
        
        return list(search_path.glob("**/*.litematic"))
    
    def render_2d_preview(self, file_path: Path, view_type: str = "combined") -> Path:
        """渲染2D预览图"""
        try:
            schematic = Schematic.load(str(file_path))
            
            category = file_path.parent.name
            output_path = self.output_dir / category / f"{file_path.stem}_2d.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建简单的预览图
            img = Image.new('RGB', (400, 300), color=(240, 240, 240))
            
            # 添加文件名
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            text = file_path.stem
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (400 - text_width) // 2
            y = (300 - text_height) // 2
            
            draw.text((x, y), text, fill=(50, 50, 50), font=font)
            
            img.save(str(output_path), "PNG")
            
            return output_path
            
        except Exception as e:
            print(f"Error rendering 2D preview for {file_path}: {e}")
            return None
    
    def render_3d_preview(self, file_path: Path, animation_type: str = "rotation") -> Path:
        """渲染3D预览动画"""
        try:
            schematic = Schematic.load(str(file_path))
            
            category = file_path.parent.name
            output_path = self.output_dir / category / f"{file_path.stem}_3d.gif"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建简单的GIF动画
            from PIL import ImageDraw
            
            frames = []
            for i in range(10):
                img = Image.new('RGB', (400, 300), color=(240, 240, 240))
                draw = ImageDraw.Draw(img)
                
                # 绘制旋转的方块
                angle = i * 36
                import math
                x_offset = int(50 * math.cos(math.radians(angle)))
                y_offset = int(50 * math.sin(math.radians(angle)))
                
                draw.rectangle([200 + x_offset - 20, 150 + y_offset - 20, 
                              200 + x_offset + 20, 150 + y_offset + 20], 
                           fill=(100, 150, 200))
                
                frames.append(img)
            
            frames[0].save(str(output_path), save_all=True, append_images=frames[1:], 
                          duration=100, loop=0)
            
            return output_path
            
        except Exception as e:
            print(f"Error rendering 3D preview for {file_path}: {e}")
            return None
    
    def render_all(self, files: List[Path] = None, 
                  render_2d: bool = True, 
                  render_3d: bool = True):
        """渲染所有文件"""
        if files is None:
            files = self.find_litematic_files()
        
        print(f"Found {len(files)} litematic files")
        
        for file_path in tqdm(files, desc="Rendering"):
            category = file_path.parent.name
            print(f"\nRendering {file_path} (category: {category})")
            
            if render_2d:
                self.render_2d_preview(file_path)
            
            if render_3d:
                self.render_3d_preview(file_path)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="渲染litematic文件预览图")
    parser.add_argument("--type", choices=["2d", "3d", "all"], default="all",
                       help="渲染类型")
    parser.add_argument("--files", help="要渲染的文件列表（逗号分隔）")
    parser.add_argument("--category", help="只渲染指定分类")
    parser.add_argument("--litematic-dir", default="litematic_files",
                       help="litematic文件目录")
    parser.add_argument("--output-dir", default="previews",
                       help="输出目录")
    
    args = parser.parse_args()
    
    renderer = LitematicRenderer(
        litematic_dir=args.litematic_dir,
        output_dir=args.output_dir
    )
    
    if args.files:
        files = [Path(f.strip()) for f in args.files.split(",")]
    else:
        files = renderer.find_litematic_files(category=args.category)
    
    render_2d = args.type in ["2d", "all"]
    render_3d = args.type in ["3d", "all"]
    
    renderer.render_all(files, render_2d=render_2d, render_3d=render_3d)


if __name__ == "__main__":
    main()
