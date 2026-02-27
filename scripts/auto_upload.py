#!/usr/bin/env python3
"""
自动上传脚本 - 渲染完成后自动上传到GitHub
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class AutoUploader:
    """自动上传器"""
    
    def __init__(self, repo_url: str = None,
                 repo_path: str = ".",
                 branch: str = "main"):
        self.repo_path = Path(repo_path)
        self.branch = branch
        self.repo_url = repo_url
        
    def git_add(self, files: List[str]):
        """添加文件到Git"""
        for file in files:
            subprocess.run(
                ["git", "add", file],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
    
    def git_commit(self, message: str):
        """提交更改"""
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.repo_path,
            check=True,
            capture_output=True
            )
    
    def git_push(self):
        """推送到GitHub"""
        subprocess.run(
            ["git", "push", "origin", self.branch],
            cwd=self.repo_path,
            check=True,
            capture_output=True
            )
    
    def upload_file(self, file_path: Path, 
                   category: str = None) -> bool:
        """上传单个文件"""
        try:
            # 确定目标路径
            if category:
                target_dir = self.repo_path / "litematic_files" / category
            else:
                target_dir = self.repo_path / "litematic_files"
            
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            target_path = target_dir / file_path.name
            import shutil
            shutil.copy2(file_path, target_path)
            
            print(f"✓ 文件已复制: {file_path.name}")
            return True
            
        except Exception as e:
            print(f"✗ 文件复制失败: {e}")
            return False
    
    def upload_previews(self, preview_files: List[Path]):
        """上传预览图"""
        for preview_file in preview_files:
            try:
                # 确定目标路径
                relative_path = preview_file.relative_to("previews")
                target_path = self.repo_path / "previews" / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制预览图
                import shutil
                shutil.copy2(preview_file, target_path)
                
                print(f"✓ 预览图已复制: {preview_file.name}")
                
            except Exception as e:
                print(f"✗ 预览图复制失败: {preview_file.name} - {e}")
    
    def upload_metadata(self, metadata: Dict[str, Any]):
        """上传元数据"""
        metadata_file = self.repo_path / "data" / "metadata.json"
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 元数据已更新")
    
    def upload_site(self, site_dir: str = "site"):
        """上传静态网站"""
        site_path = Path(site_dir)
        if not site_path.exists():
            print("✗ 静态网站不存在")
            return False
        
        # 复制网站文件到仓库根目录
        for item in site_path.iterdir():
            target_path = self.repo_path / item.name
            if target_path.exists():
                if target_path.is_dir():
                    shutil.rmtree(target_path)
                else:
                    target_path.unlink()
            
            if item.is_dir():
                shutil.copytree(item, target_path)
            else:
                shutil.copy2(item, target_path)
        
        print(f"✓ 静态网站已更新")
        return True
    
    def commit_and_push(self, message: str):
        """提交并推送"""
        try:
            # 添加所有更改
            self.git_add(["litematic_files/", "previews/", "data/", "index.html", "detail/", "category/", "assets/"])
            
            # 检查是否有更改
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                print("没有需要提交的更改")
                return False
            
            # 提交
            self.git_commit(message)
            print(f"✓ 已提交: {message}")
            
            # 推送
            print("正在推送到GitHub...")
            self.git_push()
            print("✓ 已推送到GitHub")
            
            return True
            
        except Exception as e:
            print(f"✗ 推送失败: {e}")
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="自动上传到GitHub")
    parser.add_argument("--file", help="上传单个文件")
    parser.add_argument("--category", help="文件分类")
    parser.add_argument("--repo-path", default=".",
                       help="仓库路径")
    parser.add_argument("--branch", default="main",
                       help="分支名称")
    parser.add_argument("--commit-message",
                       help="提交消息")
    
    args = parser.parse_args()
    
    # 创建上传器
    uploader = AutoUploader(
        repo_path=args.repo_path,
        branch=args.branch
    )
    
    # 上传文件
    if args.file:
        file_path = Path(args.file)
        uploader.upload_file(file_path, args.category)
        
        # 提交并推送
        message = args.commit_message or f"添加文件: {file_path.name}"
        uploader.commit_and_push(message)


if __name__ == "__main__":
    main()
