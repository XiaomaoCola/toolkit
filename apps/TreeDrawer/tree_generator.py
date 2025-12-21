import os
from pathlib import Path
from typing import List, Tuple


class TreeGenerator:
    """目录树生成器"""

    def __init__(self):
        self.tree_chars = {
            'branch': '├── ',
            'last_branch': '└── ',
            'vertical': '│   ',
            'space': '    '
        }

    def generate_tree(self, root_path: str, show_files: bool = True,
                     ignore_hidden: bool = True, max_depth: int = None) -> str:
        """
        生成目录树字符串

        Args:
            root_path: 根目录路径
            show_files: 是否显示文件
            ignore_hidden: 是否忽略隐藏文件/文件夹
            max_depth: 最大深度限制

        Returns:
            格式化的目录树字符串
        """
        if not os.path.exists(root_path):
            return f"错误：路径 '{root_path}' 不存在"

        if not os.path.isdir(root_path):
            return f"错误：'{root_path}' 不是一个目录"

        root = Path(root_path)
        tree_lines = [root.name + '/']

        try:
            self._build_tree(root, tree_lines, '', show_files,
                           ignore_hidden, max_depth, 0)
        except PermissionError:
            tree_lines.append("权限错误：无法访问某些文件夹")

        return '\n'.join(tree_lines)

    def _build_tree(self, path: Path, tree_lines: List[str], prefix: str,
                   show_files: bool, ignore_hidden: bool, max_depth: int,
                   current_depth: int):
        """递归构建目录树"""
        if max_depth is not None and current_depth >= max_depth:
            return

        try:
            # 获取目录内容
            items = list(path.iterdir())

            # 过滤隐藏文件
            if ignore_hidden:
                items = [item for item in items if not item.name.startswith('.')]

            # 分离文件夹和文件
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()] if show_files else []

            # 排序
            dirs.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())

            all_items = dirs + files

            for i, item in enumerate(all_items):
                is_last = (i == len(all_items) - 1)

                # 选择分支字符
                branch_char = self.tree_chars['last_branch'] if is_last else self.tree_chars['branch']

                # 添加项目到树
                if item.is_dir():
                    tree_lines.append(f"{prefix}{branch_char}{item.name}/")

                    # 递归处理子目录
                    extension = self.tree_chars['space'] if is_last else self.tree_chars['vertical']
                    self._build_tree(item, tree_lines, prefix + extension,
                                   show_files, ignore_hidden, max_depth,
                                   current_depth + 1)
                else:
                    tree_lines.append(f"{prefix}{branch_char}{item.name}")

        except PermissionError:
            tree_lines.append(f"{prefix}├── [权限拒绝]")
        except Exception as e:
            tree_lines.append(f"{prefix}├── [错误: {str(e)}]")

    def get_stats(self, root_path: str, ignore_hidden: bool = True) -> Tuple[int, int]:
        """
        获取目录统计信息

        Returns:
            (文件夹数量, 文件数量)
        """
        if not os.path.exists(root_path) or not os.path.isdir(root_path):
            return 0, 0

        dir_count = 0
        file_count = 0

        try:
            for root, dirs, files in os.walk(root_path):
                if ignore_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]

                dir_count += len(dirs)
                file_count += len(files)

        except PermissionError:
            pass

        return dir_count, file_count


if __name__ == "__main__":
    # 测试代码
    import sys

    # 在Windows上设置UTF-8编码
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    generator = TreeGenerator()
    current_dir = os.getcwd()
    tree = generator.generate_tree(current_dir, show_files=True, max_depth=2)
    print(tree)