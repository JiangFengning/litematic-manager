#!/usr/bin/env python3
"""
生成静态网站
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader


class SiteGenerator:
    """静态网站生成器"""
    
    def __init__(self, template_dir: str = "templates",
                 output_dir: str = "site",
                 data_dir: str = "data"):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.data_dir = Path(data_dir)
        
        self.output_dir.mkdir(exist_ok=True)
        
        self._copy_previews()
        
        self.metadata = self._load_json("metadata.json", default={})
        self.materials = self._load_json("materials.json", default={})
        self.categories = self._load_json("categories.json", default={})
        
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )
    
    def _load_json(self, filename: str, default: Any = None) -> Any:
        """加载JSON文件"""
        file_path = self.data_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _copy_previews(self):
        """复制预览图到输出目录"""
        previews_dir = Path("previews")
        if previews_dir.exists():
            output_previews = self.output_dir / "previews"
            if output_previews.exists():
                shutil.rmtree(output_previews)
            shutil.copytree(previews_dir, output_previews)
            print(f"Copied previews to {output_previews}")
    
    def generate_index(self):
        """生成首页"""
        template = self.env.get_template("index.html")
        
        html = template.render(
            title="Litematic文件管理",
            metadata=self.metadata,
            categories=self.metadata.get("categories", {}),
            current_category=None
        )
        
        output_path = self.output_dir / "index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated {output_path}")
    
    def generate_category_pages(self):
        """生成分类页面"""
        template = self.env.get_template("category.html")
        
        for category_name, category_data in self.metadata.get("categories", {}).items():
            html = template.render(
                title=f"{category_name} - Litematic文件管理",
                metadata=self.metadata,
                categories=self.metadata.get("categories", {}),
                current_category=category_name,
                category_data=category_data
            )
            
            output_path = self.output_dir / "category" / f"{category_name}.html"
            output_path.parent.mkdir(exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"Generated {output_path}")
    
    def generate_detail_pages(self):
        """生成详情页面"""
        template = self.env.get_template("detail.html")
        
        for file_path, file_metadata in self.metadata.get("files", {}).items():
            html = template.render(
                title=f"{file_metadata['name']} - Litematic文件管理",
                metadata=self.metadata,
                categories=self.metadata.get("categories", {}),
                current_category=file_metadata["category"],
                file=file_metadata,
                materials=self.materials.get(file_path, {})
            )
            
            safe_filename = file_path.replace("/", "_").replace("\\", "_")
            output_path = self.output_dir / "detail" / f"{safe_filename}.html"
            output_path.parent.mkdir(exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"Generated {output_path}")
    
    def generate_all(self):
        """生成所有页面"""
        print("Generating static site...")
        
        self.generate_index()
        self.generate_category_pages()
        self.generate_detail_pages()
        self._copy_assets()
        
        print("\nSite generation complete!")
    
    def _copy_assets(self):
        """复制静态资源"""
        assets_dir = self.template_dir / "assets"
        if assets_dir.exists():
            output_assets = self.output_dir / "assets"
            if output_assets.exists():
                shutil.rmtree(output_assets)
            shutil.copytree(assets_dir, output_assets)
            print(f"Copied assets to {output_assets}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="生成静态网站")
    parser.add_argument("--template-dir", default="templates",
                       help="模板目录")
    parser.add_argument("--output-dir", default="site",
                       help="输出目录")
    parser.add_argument("--data-dir", default="data",
                       help="数据目录")
    
    args = parser.parse_args()
    
    generator = SiteGenerator(
        template_dir=args.template_dir,
        output_dir=args.output_dir,
        data_dir=args.data_dir
    )
    
    generator.generate_all()


if __name__ == "__main__":
    main()
