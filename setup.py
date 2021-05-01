from setuptools import setup
import setuptools


setup(
    name='weibo_crawler',     # 包名字
    version='0.1',   # 包版本
    description='weibo_crawler 最简单的wiebo爬虫，可以轻度的进行微博数据采集',
    author='大邓',  # 作者
    author_email='thunderhit@qq.com',  # 邮箱
    url='https://github.com/thunderhit/weibo_crawler',      # 包的主页
    packages=setuptools.find_packages(),
    install_requires=['requests', 'pyquery'],
    python_requires='>=3.5',
    license="MIT",
    keywords=['data collect', '数据采集', 'weibo', '微博'],
    long_description=open('README.md').read(), # 读取的Readme文档内容
    long_description_content_type="text/markdown")  # 指定包文档格式为markdown
    #py_modules = ['eventextraction.py']