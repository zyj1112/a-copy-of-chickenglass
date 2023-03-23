import yaml
import argparse
import os
import pandoc
from pandoc.types import *
import shutil
import json

# 关于argparse库的相关语法学习参考：https://zhuanlan.zhihu.com/p/395173906
# parser = argparse.ArgumentParser() 创建一个叫做parser的参数获取对象
# parser.add_argument 添加命令行参数
# args = parser.parse_args() 从命令行解析参数

# 关于os库的相关语法学习参考https://zhuanlan.zhihu.com/p/82029511
#os.path系列语法
# os.walk(top, topdown=True, οnerrοr=None, followlinks=False)
# dirpath 是一个string，代表目录的路径， dirnames 是一个list，包含了dirpath下所有子目录的名字。 filenames 是一个list，包含了非目录文件的名字。
# os.sep系统文件分隔符

# 关于yaml学习参考https://www.runoob.com/w3cnote/yaml-intro.html

def main():
    parser = argparse.ArgumentParser(description='Huh.') # 创建一个参数对象parser
    parser.add_argument('project_dir', metavar='D', type=str,
                        help='the input project directory')
    parser.add_argument('output_dir', metavar='O', type=str,
                        help='the output project directory') # 添加两个字符串类型参数：'project_dir' 'ouput_dir'
    args = parser.parse_args() # 从命令行获取参数
    project_dir = args.project_dir
    output_dir = args.output_dir
    config_file = os.path.join(project_dir, '_chickenglass.yaml') # 配置文件
    with open(config_file, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        # read configs
        filter_path = os.path.dirname(os.path.realpath(__file__)) + "/filters/"
        read_lua_filters = ["--lua-filter=" + filter_path + x + ".lua" for x in config['read-lua-filters']]
        css = config['format']['html']['css']
        read_options = read_lua_filters + ["--bibliography=" + project_dir + "/" + config['bib'],
                                           "--csl=" + project_dir + "/" + config['csl'],
                                           "--citeproc",
                                           "--metadata=reference-section-title:References"] # 读filters里的.lua文件
                                                                                            # 似乎在使用pandoc的filters 但还没太搞懂这些.lua文件的具体原理

        # handle latex math macros
        latex_macros = {} # 处理python中数学宏的问题
        if config['latex-math-macros']:
            if math_render == 'katex':
                latex_macros = {('\\' + a): b for (a, b) in config['latex-math-macros'].items()} # 用latex数学宏
        latex_macros_json = json.dumps(latex_macros)

        # find all files with *.md
        md_files = []
        out_files = {}
        n = len(project_dir.split(os.sep))# os.sep是系统路径的分隔符
        for root, dirs, files in os.walk(project_dir): # 目录路径，子目录，第一个文件
            path = root.split(os.sep)
            path = [output_dir] + path[n:]
            for file in files: # 读取每一个文件 如果文件是.md格式，则把他变成output的html并添加到md_files
                name, ext = os.path.splitext(file)
                if ext == '.md':
                    filename = os.path.join(root, file)
                    md_files.append(filename)
                    out_files[filename] = os.path.join(*path, name + ".html")

        # pandoc_contents
        # read
        pandoc_contents = {}
        for file in md_files: #读取md_files的每一个文件，利用pandoc完成格式转化
            with open(file, "r") as stream:
                content = stream.read()
                pandoc_contents[file] = pandoc.read(content,
                                                    format="markdown+tex_math_single_backslash+east_asian_line_breaks",
                                                    options=read_options)
                # add latex macros into the meta dict
                pandoc_contents[file][0][0]["latex-macros-json"] = MetaInlines(
                    [RawInline(Format("html"), latex_macros_json)])

        # TODO: need to create a navigations page?

        # write
        for file in md_files: #将md_files中的文件写入
            html_content = pandoc.write(pandoc_contents[file], format="html", options=write_options)
            os.makedirs(os.path.dirname(out_files[file]), exist_ok=True)
            with open(out_files[file], "w", encoding='utf-8') as f:
                f.write(html_content)

        # copy
        for file in config['copy']:
            in_file = os.path.join(project_dir, file)
            out_file = os.path.join(output_dir, file)
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            shutil.copy(in_file, out_file)

    main()