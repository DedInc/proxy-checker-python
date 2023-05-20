import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='proxy_checker_requests',
    version='0.6.1',
    packages=['proxy_checker_requests'],
    install_requires=['requests'],
    author='ricerati',
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
