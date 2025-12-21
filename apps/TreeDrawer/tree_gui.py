import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
from tree_generator import TreeGenerator


class TreeDrawerGUI:
    """目录树生成器GUI应用"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("目录树生成器 - TreeDrawer")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        # 初始化树生成器
        self.tree_generator = TreeGenerator()

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        """创建GUI界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # 路径选择区域
        path_label = ttk.Label(main_frame, text="目录路径:")
        path_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # 路径输入框和浏览按钮
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(0, weight=1)

        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, font=('Consolas', 9))
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        browse_btn = ttk.Button(path_frame, text="浏览", command=self.browse_directory)
        browse_btn.grid(row=0, column=1)

        # 选项区域
        options_frame = ttk.LabelFrame(main_frame, text="选项", padding="5")
        options_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(2, weight=1)

        # 显示文件选项
        self.show_files_var = tk.BooleanVar(value=True)
        show_files_cb = ttk.Checkbutton(options_frame, text="显示文件",
                                      variable=self.show_files_var)
        show_files_cb.grid(row=0, column=0, sticky=tk.W, padx=(0, 15))

        # 忽略隐藏文件选项
        self.ignore_hidden_var = tk.BooleanVar(value=True)
        ignore_hidden_cb = ttk.Checkbutton(options_frame, text="忽略隐藏文件",
                                         variable=self.ignore_hidden_var)
        ignore_hidden_cb.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))

        # 最大深度选项
        depth_label = ttk.Label(options_frame, text="最大深度:")
        depth_label.grid(row=0, column=2, sticky=tk.E, padx=(0, 5))

        self.depth_var = tk.StringVar(value="")
        depth_entry = ttk.Entry(options_frame, textvariable=self.depth_var, width=8)
        depth_entry.grid(row=0, column=3, sticky=tk.W)

        # 生成按钮
        generate_btn = ttk.Button(main_frame, text="生成目录树", command=self.generate_tree)
        generate_btn.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        # 统计信息标签
        self.stats_var = tk.StringVar(value="")
        stats_label = ttk.Label(main_frame, textvariable=self.stats_var, foreground="gray")
        stats_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="生成的目录树", padding="5")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        # 文本输出区域（使用等宽字体）
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.NONE,
            font=('Consolas', 9),
            background='#f8f8f8',
            relief='sunken',
            borderwidth=1
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))

        # 复制按钮
        copy_btn = ttk.Button(button_frame, text="复制到剪贴板", command=self.copy_to_clipboard)
        copy_btn.grid(row=0, column=0, padx=(0, 10))

        # 清空按钮
        clear_btn = ttk.Button(button_frame, text="清空输出", command=self.clear_output)
        clear_btn.grid(row=0, column=1)

        # 设置初始目录为当前工作目录
        self.path_var.set(os.getcwd())

    def browse_directory(self):
        """浏览选择目录"""
        directory = filedialog.askdirectory(
            title="选择要生成树状图的目录",
            initialdir=self.path_var.get() if os.path.exists(self.path_var.get()) else os.getcwd()
        )
        if directory:
            self.path_var.set(directory)

    def generate_tree(self):
        """生成目录树"""
        path = self.path_var.get().strip()
        if not path:
            messagebox.showerror("错误", "请选择一个目录路径")
            return

        if not os.path.exists(path):
            messagebox.showerror("错误", f"路径不存在: {path}")
            return

        if not os.path.isdir(path):
            messagebox.showerror("错误", f"选择的路径不是目录: {path}")
            return

        try:
            # 获取选项
            show_files = self.show_files_var.get()
            ignore_hidden = self.ignore_hidden_var.get()

            # 处理最大深度
            max_depth = None
            depth_str = self.depth_var.get().strip()
            if depth_str:
                try:
                    max_depth = int(depth_str)
                    if max_depth <= 0:
                        max_depth = None
                except ValueError:
                    messagebox.showerror("错误", "最大深度必须是正整数")
                    return

            # 生成目录树
            tree_text = self.tree_generator.generate_tree(
                path, show_files, ignore_hidden, max_depth
            )

            # 显示结果
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, tree_text)

            # 更新统计信息
            dir_count, file_count = self.tree_generator.get_stats(path, ignore_hidden)
            if show_files:
                stats_text = f"统计: {dir_count} 个文件夹, {file_count} 个文件"
            else:
                stats_text = f"统计: {dir_count} 个文件夹"
            self.stats_var.set(stats_text)

        except Exception as e:
            messagebox.showerror("错误", f"生成目录树时发生错误:\n{str(e)}")

    def copy_to_clipboard(self):
        """复制输出内容到剪贴板"""
        content = self.output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有可复制的内容")
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()  # 确保剪贴板更新
            messagebox.showinfo("成功", "目录树已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制到剪贴板失败:\n{str(e)}")

    def clear_output(self):
        """清空输出内容"""
        self.output_text.delete(1.0, tk.END)
        self.stats_var.set("")

    def run(self):
        """运行应用程序"""
        # 居中显示窗口
        self.center_window()
        self.root.mainloop()

    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")


def main():
    """主函数"""
    app = TreeDrawerGUI()
    app.run()


if __name__ == "__main__":
    main()