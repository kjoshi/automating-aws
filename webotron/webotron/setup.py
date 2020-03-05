from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author='Kiran Joshi',
    author_email='kiran.j88@gmail.com',
    description='A tool to deploy static websites to AWS S3',
    license='GPLv3+',
    packages=['webotron'],
    url='',
    install_requires=[
        'boto3',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'webotron = webotron.webotron:cli'
        ]
    }
)