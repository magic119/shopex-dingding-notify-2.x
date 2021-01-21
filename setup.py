# -*- coding: UTF-8 -*-

import sys
reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

from setuptools import setup, find_packages

# requires = ["amqp==1.4.9", "amqplib==1.0.2", "aniso8601==8.1.0", "anyjson==0.3.3",
#             "attrs==20.3.0", "gevent==1.1.1", "greenlet==0.4.15", "httplib2==0.9",
#             "kombu==3.0.30", "requests==2.21.0", "urllib3==1.24.3"]  # 需要安装的第三方依赖

setup(
    name="shopex-dingding-notify-2.x.x",
    version=1.0,
    description="ShopEx dingding notify for python",
    long_description_content_type=open("README.md").read(),
    packages=find_packages(),
    author="ShopEx",
    author_email="xuhongtao@shopex.cn",
    license="LGPL",
    url="https://github.com/magic119/shopex-dingding-notify-2.x.git",
    platforms=["README.md"],
    python_requires=">=2.7.0, <2.7.18",
    # install_requires=requires
)