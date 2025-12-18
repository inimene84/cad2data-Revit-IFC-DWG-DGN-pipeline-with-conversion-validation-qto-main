#!/usr/bin/env python3
"""
Cleanup script for construction-platform
Removes unnecessary files and directories for VPS deployment
"""

import os
import shutil
from pathlib import Path

class ProjectCleanup:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.files_removed = []
        self.dirs_removed = []
        self.size_freed = 0
        
    def get_size(self, path):
        """Get size of file or directory"""
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            total = 0
            try:
                for entry in path.rglob('*'):
                    if entry.is_file():
                        total += entry.stat().st_size
            except (PermissionError, OSError):
                pass
            return total
        return 0
    
    def remove_file(self, file_path, reason=""):
        """Remove a file"""
        if file_path.exists():
            size = self.get_size(file_path)
            try:
                file_path.unlink()
                self.files_removed.append(str(file_path))
                self.size_freed += size
                print(f"Removed file: {file_path} ({reason})")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
    
    def remove_dir(self, dir_path, reason=""):
        """Remove a directory"""
        if dir_path.exists() and dir_path.is_dir():
            size = self.get_size(dir_path)
            try:
                shutil.rmtree(dir_path)
                self.dirs_removed.append(str(dir_path))
                self.size_freed += size
                print(f"Removed directory: {dir_path} ({reason})")
            except Exception as e:
                print(f"Error removing {dir_path}: {e}")
    
    def cleanup_test_files(self):
        """Remove test files"""
        print("\nCleaning up test files...")
        
        test_patterns = [
            "**/test_*.py",
            "**/*_test.py",
            "**/tests/**",
            "**/test/**",
            "**/*.test.js",
            "**/*.test.ts",
            "**/*.test.tsx",
            "**/*.spec.js",
            "**/*.spec.ts",
            "**/*.spec.tsx",
        ]
        
        for pattern in test_patterns:
            for file_path in self.project_path.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "test file")
                elif file_path.is_dir():
                    self.remove_dir(file_path, "test directory")
    
    def cleanup_build_artifacts(self):
        """Remove build artifacts"""
        print("\nCleaning up build artifacts...")
        
        build_patterns = [
            "**/__pycache__/**",
            "**/*.pyc",
            "**/*.pyo",
            "**/*.pyd",
            "**/.pytest_cache/**",
            "**/.mypy_cache/**",
            "**/.coverage",
            "**/htmlcov/**",
            "**/.nyc_output/**",
            "**/coverage/**",
        ]
        
        for pattern in build_patterns:
            for file_path in self.project_path.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "build artifact")
                elif file_path.is_dir():
                    self.remove_dir(file_path, "build directory")
    
    def cleanup_node_modules(self):
        """Remove node_modules directories"""
        print("\nCleaning up node_modules...")
        
        node_modules_dirs = list(self.project_path.rglob("node_modules"))
        for node_modules_dir in node_modules_dirs:
            # Keep node_modules in web-react for build, but remove after build
            if "web-react" in str(node_modules_dir):
                # Check if build directory exists
                build_dir = node_modules_dir.parent / "build"
                if build_dir.exists():
                    self.remove_dir(node_modules_dir, "node_modules (build exists)")
            else:
                self.remove_dir(node_modules_dir, "node_modules")
    
    def cleanup_log_files(self):
        """Remove log files"""
        print("\nCleaning up log files...")
        
        log_patterns = [
            "**/*.log",
            "**/*.logs",
            "**/logs/**",
            "**/nginx/logs/**",  # Keep nginx config, remove logs
        ]
        
        for pattern in log_patterns:
            for file_path in self.project_path.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "log file")
                elif file_path.is_dir() and "nginx/logs" in str(file_path):
                    # Clean nginx logs directory but keep it
                    for log_file in file_path.glob("*.log"):
                        self.remove_file(log_file, "nginx log")
    
    def cleanup_temporary_files(self):
        """Remove temporary files"""
        print("\nCleaning up temporary files...")
        
        temp_patterns = [
            "**/*.tmp",
            "**/*.temp",
            "**/*.swp",
            "**/*.swo",
            "**/*~",
            "**/.DS_Store",
            "**/Thumbs.db",
            "**/.idea/**",
            "**/.vscode/**",
            "**/.vs/**",
        ]
        
        for pattern in temp_patterns:
            for file_path in self.project_path.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "temporary file")
                elif file_path.is_dir():
                    self.remove_dir(file_path, "temporary directory")
    
    def cleanup_backup_files(self):
        """Remove backup files"""
        print("\nCleaning up backup files...")
        
        backup_patterns = [
            "**/*.bak",
            "**/*.backup",
            "**/*.old",
            "**/*.orig",
            "**/backups/**",
        ]
        
        for pattern in backup_patterns:
            for file_path in self.project_path.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "backup file")
                elif file_path.is_dir():
                    self.remove_dir(file_path, "backup directory")
    
    def cleanup_duplicate_files(self):
        """Remove duplicate files"""
        print("\nCleaning up duplicate files...")
        
        # Remove docker-compose.yml (keep docker-compose.prod.yml)
        docker_compose = self.project_path / "docker-compose.yml"
        if docker_compose.exists():
            docker_compose_prod = self.project_path / "docker-compose.prod.yml"
            if docker_compose_prod.exists():
                self.remove_file(docker_compose, "duplicate (keeping docker-compose.prod.yml)")
        
        # Remove build.log if build directory exists
        build_log = self.project_path / "web-react" / "build.log"
        if build_log.exists():
            build_dir = self.project_path / "web-react" / "build"
            if build_dir.exists():
                self.remove_file(build_log, "build log (build directory exists)")
    
    def cleanup_empty_directories(self):
        """Remove empty directories"""
        print("\nCleaning up empty directories...")
        
        # Find all directories
        all_dirs = []
        for root, dirs, files in os.walk(self.project_path):
            for dir_name in dirs:
                all_dirs.append(Path(root) / dir_name)
        
        # Sort by depth (deepest first)
        all_dirs.sort(key=lambda p: len(p.parts), reverse=True)
        
        # Remove empty directories (except important ones)
        important_dirs = {
            "cad-converters",
            "n8n-workflows",
            "python-services",
            "web-react",
            "deployment",
            "monitoring",
            "nginx",
            "sql",
            "config",
            "secrets",
            "uploads",
            "output",
        }
        
        for dir_path in all_dirs:
            # Skip important directories
            if any(important in str(dir_path) for important in important_dirs):
                continue
            
            # Skip if directory is in an important path
            if any(important in str(dir_path.parent) for important in important_dirs):
                continue
            
            try:
                # Check if directory is empty
                if dir_path.exists() and dir_path.is_dir():
                    if not any(dir_path.iterdir()):
                        self.remove_dir(dir_path, "empty directory")
            except (PermissionError, OSError):
                pass
    
    def cleanup_unnecessary_documentation(self):
        """Remove unnecessary documentation files"""
        print("\nCleaning up unnecessary documentation...")
        
        # Keep only essential documentation
        essential_docs = {
            "README.md",
            ".env.production.example",
            "docker-compose.prod.yml",
            "requirements.txt",  # Keep requirements.txt files
            "package.json",      # Keep package.json files
        }
        
        doc_patterns = [
            "**/*.md",
            "**/*.txt",
            "**/*.pdf",
        ]
        
        for pattern in doc_patterns:
            for file_path in self.project_path.rglob(pattern):
                # Skip essential files
                if file_path.name in essential_docs:
                    continue
                
                # Skip requirements.txt files
                if file_path.name == "requirements.txt":
                    continue
                
                # Skip package.json files
                if file_path.name == "package.json":
                    continue
                
                # Skip if in root directory (keep README.md)
                if file_path.parent == self.project_path:
                    if file_path.name == "README.md":
                        continue
                
                # Remove other documentation
                self.remove_file(file_path, "unnecessary documentation")
    
    def cleanup_development_files(self):
        """Remove development-only files"""
        print("\nCleaning up development files...")
        
        dev_patterns = [
            "**/.git/**",
            "**/.gitignore",
            "**/.gitattributes",
            "**/.env.local",
            "**/.env.development",
            "**/.env.test",
            "**/package-lock.json",  # Keep package.json, remove lock file
            "**/yarn.lock",
            "**/pnpm-lock.yaml",
        ]
        
        for pattern in dev_patterns:
            for file_path in self.project_path.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "development file")
                elif file_path.is_dir():
                    self.remove_dir(file_path, "development directory")
    
    def cleanup_large_files(self):
        """Remove unnecessarily large files"""
        print("\nCleaning up large files...")
        
        # Files larger than 100MB that might not be needed
        large_file_patterns = [
            "**/*.zip",
            "**/*.tar",
            "**/*.tar.gz",
            "**/*.rar",
            "**/*.7z",
        ]
        
        for pattern in large_file_patterns:
            for file_path in self.project_path.rglob(pattern):
                if file_path.is_file():
                    size = file_path.stat().st_size
                    # Remove archives larger than 50MB
                    if size > 50 * 1024 * 1024:
                        self.remove_file(file_path, f"large archive ({size / 1024 / 1024:.2f} MB)")
    
    def create_gitignore(self):
        """Create .gitignore file"""
        print("\nCreating .gitignore...")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
*.egg

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Environment
.env
.env.local
.env.development
.env.test
.env.production
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Logs
*.log
logs/
*.logs

# Temporary
*.tmp
*.temp
*.bak
*.backup
*.old
*.orig

# Build
build/
dist/
*.build

# Test
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
.nyc_output/
coverage/

# Archives
*.zip
*.tar
*.tar.gz
*.rar
*.7z

# Docker
.dockerignore

# Secrets
secrets/
*.pem
*.key
*.crt

# Uploads and outputs
uploads/*
!uploads/.gitkeep
output/*
!output/.gitkeep
"""
        
        gitignore_path = self.project_path / ".gitignore"
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        print(f"Created .gitignore")
    
    def create_dockerignore(self):
        """Create .dockerignore file"""
        print("\nCreating .dockerignore...")
        
        dockerignore_content = """# Git
.git
.gitignore
.gitattributes

# Documentation
*.md
*.txt
*.pdf
README*

# Environment
.env
.env.local
.env.development
.env.test
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/
*.logs

# Temporary
*.tmp
*.temp
*.bak
*.backup
*.old
*.orig

# Test
test/
tests/
*_test.py
test_*.py
*.test.js
*.test.ts
*.test.tsx
*.spec.js
*.spec.ts
*.spec.tsx

# Build artifacts
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/
.nyc_output/
coverage/

# Node (keep package.json, remove node_modules)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Archives
*.zip
*.tar
*.tar.gz
*.rar
*.7z

# Secrets
secrets/
*.pem
*.key
*.crt

# Development files
.git/
.gitignore
.gitattributes
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
"""
        
        dockerignore_path = self.project_path / ".dockerignore"
        dockerignore_path.write_text(dockerignore_content, encoding='utf-8')
        print(f"Created .dockerignore")
    
    def print_summary(self):
        """Print cleanup summary"""
        print("\n" + "=" * 60)
        print("Cleanup Summary")
        print("=" * 60)
        print(f"Files removed: {len(self.files_removed)}")
        print(f"Directories removed: {len(self.dirs_removed)}")
        print(f"Size freed: {self.size_freed / 1024 / 1024:.2f} MB")
        print("\nFiles removed:")
        for file_path in self.files_removed[:20]:  # Show first 20
            print(f"  - {file_path}")
        if len(self.files_removed) > 20:
            print(f"  ... and {len(self.files_removed) - 20} more files")
        print("\nDirectories removed:")
        for dir_path in self.dirs_removed[:20]:  # Show first 20
            print(f"  - {dir_path}")
        if len(self.dirs_removed) > 20:
            print(f"  ... and {len(self.dirs_removed) - 20} more directories")
        print("=" * 60)
    
    def run(self):
        """Run cleanup process"""
        print("Cleaning up construction-platform...")
        print("=" * 60)
        
        # Run cleanup steps
        self.cleanup_test_files()
        self.cleanup_build_artifacts()
        self.cleanup_node_modules()
        self.cleanup_log_files()
        self.cleanup_temporary_files()
        self.cleanup_backup_files()
        self.cleanup_duplicate_files()
        self.cleanup_unnecessary_documentation()
        self.cleanup_development_files()
        self.cleanup_large_files()
        self.cleanup_empty_directories()
        
        # Create ignore files
        self.create_gitignore()
        self.create_dockerignore()
        
        # Print summary
        self.print_summary()
        
        print("\nCleanup complete!")
        print(f"Project size reduced by {self.size_freed / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    project_path = Path(__file__).parent / "construction-platform"
    
    if not project_path.exists():
        print(f"Error: {project_path} does not exist!")
        print("Run combine_projects.py first to create the project.")
        exit(1)
    
    cleanup = ProjectCleanup(project_path)
    cleanup.run()

