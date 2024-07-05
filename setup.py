from setuptools import setup, find_packages

setup(
    name='LLMeta',
    version='1.0.0',
    description='A tool for systematic reviews using large language models with RAG and HyDE',
    long_description= '''LLMeta is a Python package designed for conducting systematic reviews using large language models in conjunction with Retrieval Augmented Generation (RAG) and Hypothetical Document Embeddings (HyDE) techniques.''',
    author='Jinquan Ye',
    author_email='jinquan.ye@duke.edu',
    url='https://github.com/yebarryallen/LLMeta',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'openai',
        'langchain',
        'langchain_openai',
        # Add any other dependencies here
    ],
    keywords=['survey', 'carbon footprint', 'emissions'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
