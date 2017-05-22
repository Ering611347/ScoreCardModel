
import os
import sys
import copy
import platform
import distutils
import subprocess
from os import path
from codecs import open
from setuptools import setup, find_packages, Command

if sys.version_info[0] != 3:
    raise OSError("only for python 3.5+")
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    raise OSError("only for python 3.5+")

from pathlib import Path

REQUIREMETS_DEV_FILE = 'requirements_dev.txt'
REQUIREMETS_TEST_FILE = 'requirements_test.txt'
REQUIREMETS_FILE = 'requirements.txt'
PROJECTNAME = 'score_card_model'
VERSION = '0.0.1'
DESCRIPTION = 'A sample Python project for score card model'
URL = 'https://github.com/data-science-tools/ScoreCardModel'
AUTHOR = 'hsz'
AUTHOR_EMAIL = 'hsz1273327@gmail.com'
LICENSE = 'MIT'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Math model',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
]
KEYWORDS = 'math finance model statistics machine_learning'
PACKAGES = find_packages(exclude=['contrib', 'docs', 'test'])
ZIP_SAFE = False
# 用同文件夹下的README.rst文件定义长介绍
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# 用同文件夹下的requirements.txt文件定义运行依赖
with open(path.join(HERE, REQUIREMETS_FILE), encoding='utf-8') as f:
    REQUIREMETS = f.readlines()

with open(path.join(HERE, REQUIREMETS_DEV_FILE), encoding='utf-8') as f:
    REQUIREMETS_DEV = f.readlines()

with open(path.join(HERE, REQUIREMETS_TEST_FILE), encoding='utf-8') as f:
    REQUIREMETS_TEST = f.readlines()


def get_command():
    if platform.system() == 'Windows':
        PYTHON = 'python'
        p = Path(".\env")
        if p.exists():
            COMMAND = ['env\Scripts\python']
        else:
            COMMAND = [PYTHON]
    else:
        PYTHON = 'python3'
        p = Path("./env")
        if p.exists():
            COMMAND = ['env/bin/python']
        else:
            COMMAND = [PYTHON]
    return PYTHON, COMMAND


class DocCommand(Command):
    description = "文档工具"
    user_options = [
        ("runcommand=", "r", "文档操作")
    ]

    def initialize_options(self):
        self.cwd = None
        self.runcommand = "serve"

    def finalize_options(self):
        self.cwd = os.getcwd()
        if self.runcommand == None:
            self.runcommand = "serve"
        else:
            if self.runcommand not in ('serve','build','gitpage'):
                raise AttributeError("runcommand 的参数必须在 'serve','build','gitpage' 之中")


    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: {self.cwd}'.format(self=self)
        _, COMMAND = get_command()

        if self.runcommand == 'build':
            command = copy.copy(COMMAND)
            command += ['-m', 'mkdocs', 'build']
            self.announce('Running command: {command}'.format(command=str(command)),
                          level=distutils.log.INFO)
            subprocess.check_call(command)
            return 0

        elif self.runcommand == 'gitpage':
            command = copy.copy(COMMAND)
            command += ['-m', 'mkdocs', 'gh-deploy']
            self.announce('Running command: {command}'.format(command=str(command)),
                          level=distutils.log.INFO)
            subprocess.check_call(command)
            return 0
        else:
            command = copy.copy(COMMAND)
            command += ['-m', 'mkdocs', 'serve']
            self.announce('Running command: {command}'.format(command=str(command)),
                          level=distutils.log.INFO)
            subprocess.check_call(command)
            return 0



        ("serve=", "s", "启动文档的静态服务器"),
        ('gh_deploy=',"g","放到gitpage")


class InitCommand(Command):
    description = "初始化项目"
    user_options = [('globa=', 'g', "使用全局环境")]

    def initialize_options(self):
        self.globa = None
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: {self.cwd}'.format(self=self)
        if not self.globa:
            PYTHON, _ = get_command()
            command = [PYTHON, '-m', 'venv', 'env']
            self.announce('Running command: {command}'.format(command=str(command)),
                          level=distutils.log.INFO)
            subprocess.check_call(command)
        _, COMMAND = get_command()
        command = copy.copy(COMMAND)
        command += ['-m', 'pip', 'install', '-r', REQUIREMETS_FILE]
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=distutils.log.INFO)
        subprocess.check_call(command)

        command = copy.copy(COMMAND)
        command += ['-m', 'pip', 'install', '-r', REQUIREMETS_TEST_FILE]
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=distutils.log.INFO)
        subprocess.check_call(command)

        command = copy.copy(COMMAND)
        command += ['-m', 'pip', 'install', '-r', REQUIREMETS_DEV_FILE]
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=distutils.log.INFO)
        subprocess.check_call(command)

        command = copy.copy(COMMAND)
        command += ['-m', 'mkdocs', 'new', '.']
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=distutils.log.INFO)
        subprocess.check_call(command)
#         with open(path.join(HERE, 'docs/mathjaxhelper.js'), 'w', encoding='utf-8') as f:
#             f.write('''MathJax.Hub.Config({
# "tex2jax": { inlineMath: [ [ '$', '$' ] ] }
# });
# MathJax.Hub.Config({
# config: ["MMLorHTML.js"],
# jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
# extensions: ["MathMenu.js", "MathZoom.js"]
# });''')
        with open(path.join(HERE, 'mkdocs.yml'), 'w' ,encoding='utf-8') as f:
            f.write("""site_name: My Docs
markdown_extensions: ['extra', 'mdx_math']
extra_javascript: ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML']
pages:
  - Home: index.md
  - API: api.autodoc
theme: readthedocs
""")
        with open(path.join(HERE, 'docs/api.autodoc'), "w", encoding='utf-8') as f:
            for i in PACKAGES:
                f.write(i)
                f.write("\n")



class CoverageCommand(Command):
    description = "覆盖率"
    user_options = [
        ("output=", "o", "选择报告的输出方式")
    ]

    def initialize_options(self):
        self.cwd = None
        self.output = ''

    def finalize_options(self):
        self.cwd = os.getcwd()
        if self.output and self.output not in ("report", "html"):
            raise Exception("Parameter --output is missing")

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: {self.cwd}'.format(self=self)
        _, COMMAND = get_command()
        command = copy.copy(COMMAND)
        command += ['-m', 'coverage']
        if self.output:
            cm = '{self.output}'.format(self=self)
            command.append(cm)
        else:
            command.append('report')
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=distutils.log.INFO)
        subprocess.check_call(command)


class TestCommand(Command):
    description = "测试"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: {self.cwd}'.format(self=self)
        _, COMMAND = get_command()
        command = copy.copy(COMMAND)
        command += ['-m',
                   'coverage', 'run', '--source=score_card_model',
                   '-m', 'unittest', 'discover', '-v', '-s', 'test']
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=distutils.log.INFO)
        subprocess.check_call(command)


setup(
    name=PROJECTNAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=PACKAGES,
    install_requires=REQUIREMETS,
    extras_require={
        #'dev': REQUIREMETS_DEV,
        'test': REQUIREMETS_TEST
    },
    zip_safe=ZIP_SAFE,
    data_files=[('./', ['requirements.txt', 'requirements_dev.txt', 'requirements_test.txt'])],
    # 定义自定义命令
    cmdclass={
        'init': InitCommand,
        'doc': DocCommand,
        'coverage': CoverageCommand,
        'test': TestCommand
    }
)
