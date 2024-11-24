from setuptools import setup, find_packages

setup(
    name='MyAPIManager',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'cryptography',
    ],
    url='https://github.com/lupin-oomura/MyAPIManager.git',
    author='Shin Oomura',
    author_email='shin.oomura@gmail.com',
    description='APIを自作する際の便利クラス',
)
