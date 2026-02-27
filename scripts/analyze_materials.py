#!/usr/bin/env python3
"""
litematic文件材料分析脚本
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from tqdm import tqdm

try:
    from litemapy import Schematic
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)


class MaterialAnalyzer:
    """材料分析器"""
    
    def __init__(self, litematic_dir: str = "litematic_files",
                 output_file: str = "data/materials.json"):
        self.litematic_dir = Path(litematic_dir)
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(exist_ok=True)
        
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个文件的材料"""
        try:
            schematic = Schematic.load(str(file_path))
            
            result = {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "category": file_path.parent.name,
                "total_blocks": 0,
                "unique_blocks": 0,
                "blocks": {},
                "entities": {},
                "tiles": {}
            }
            
            # 简单的材料统计
            if hasattr(schematic, 'regions'):
                for region_name, region in schematic.regions.items():
                    if hasattr(region, 'blocks'):
                        for block in region.blocks:
                            block_id = str(block)
                            result["blocks"][block_id] = result["blocks"].get(block_id, 0) + 1
            
            result["total_blocks"] = sum(result["blocks"].values())
            result["unique_blocks"] = len(result["blocks"])
            
            return result
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def analyze_all(self) -> Dict[str, Any]:
        """分析所有文件"""
        files = list(self.litematic_dir.glob("**/*.litematic"))
        print(f"Found {len(files)} litematic files")
        
        materials = {}
        
        for file_path in tqdm(files, desc="Analyzing"):
            result = self.analyze_file(file_path)
            if result:
                materials[str(file_path)] = result
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)
        
        print(f"Materials saved to {self.output_file}")
        return materials


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="分析litematic文件材料")
    parser.add_argument("--litematic-dir", default="litematic_files",
                       help="litematic文件目录")
    parser.add_argument("--output-file", default="data/materials.json",
                       help="输出文件")
    
    args = parser.parse_args()
    
    analyzer = MaterialAnalyzer(
        litematic_dir=args.litematic_dir,
        output_file=args.output_file
    )
    
    analyzer.analyze_all()


if __name__ == "__main__":
    main()
