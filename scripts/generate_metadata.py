#!/usr/bin/env python3
"""
生成litematic文件元数据
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

try:
    from litemapy import Schematic
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)


class MetadataGenerator:
    """元数据生成器"""
    
    def __init__(self, litematic_dir: str = "litematic_files",
                 output_file: str = "data/metadata.json"):
        self.litematic_dir = Path(litematic_dir)
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(exist_ok=True)
        
    def generate_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """生成单个文件的元数据"""
        try:
            schematic = Schematic.load(str(file_path))
            
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
            
            if hasattr(schematic, 'regions'):
                for region_name, region in schematic.regions.items():
                    region_info = {
                        "name": region_name,
                        "position": {
                            "x": getattr(region.position, 'x', 0),
                            "y": getattr(region.position, 'y', 0),
                            "z": getattr(region.position, 'z', 0)
                        },
                        "size": {
                            "x": getattr(region.size, 'x', 0),
                            "y": getattr(region.size, 'y', 0),
                            "z": getattr(region.size, 'z', 0)
                        },
                        "volume": getattr(region.size, 'x', 0) * getattr(region.size, 'y', 0) * getattr(region.size, 'z', 0)
                    }
                    metadata["regions"].append(region_info)
            
            total_volume = sum(r["volume"] for r in metadata["regions"])
            metadata["total_volume"] = total_volume
            
            metadata["estimated_block_count"] = int(total_volume * 0.7)
            
            category = file_path.parent.name
            preview_2d = Path(f"previews/{category}/{file_path.stem}_2d.png")
            preview_3d = Path(f"previews/{category}/{file_path.stem}_3d.gif")
            
            metadata["previews"] = {
                "2d": str(preview_2d) if preview_2d.exists() else None,
                "3d": str(preview_3d) if preview_3d.exists() else None
            }
            
            return metadata
            
        except Exception as e:
            print(f"Error generating metadata for {file_path}: {e}")
            return None
    
    def generate_all_metadata(self) -> Dict[str, Any]:
        """生成所有文件的元数据"""
        files = list(self.litematic_dir.glob("**/*.litematic"))
        print(f"Found {len(files)} litematic files")
        
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "total_files": len(files),
            "files": {}
        }
        
        categories = {}
        for file_path in files:
            category = file_path.parent.name
            if category not in categories:
                categories[category] = []
            categories[category].append(file_path)
        
        for category, files_in_category in categories.items():
            print(f"\nProcessing category: {category}")
            
            category_data = {
                "name": category,
                "file_count": len(files_in_category),
                "files": []
            }
            
            for file_path in files_in_category:
                file_metadata = self.generate_file_metadata(file_path)
                if file_metadata:
                    category_data["files"].append(file_metadata)
                    metadata["files"][str(file_path.relative_to(self.litematic_dir))] = file_metadata
            
            metadata.setdefault("categories", {})[category] = category_data
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"\nMetadata saved to {self.output_file}")
        return metadata


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="生成litematic文件元数据")
    parser.add_argument("--litematic-dir", default="litematic_files",
                       help="litematic文件目录")
    parser.add_argument("--output-file", default="data/metadata.json",
                       help="输出文件")
    
    args = parser.parse_args()
    
    generator = MetadataGenerator(
        litematic_dir=args.litematic_dir,
        output_file=args.output_file
    )
    
    generator.generate_all_metadata()


if __name__ == "__main__":
    main()
