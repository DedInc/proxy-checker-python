import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='proxy_checker_httpx',
    version='0.6.0',
    packages=['proxy_checker_httpx'],
    install_requires=['httpx'],
    author='Maehdakvan',
    description='Proxy checker in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='proxy checker',
    project_urls={
        'Source Code': 'https://github.com/DedInc/proxy-checker-python'
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)
