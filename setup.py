from setuptools import setup, find_packages

# create setup.py file
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='tweeter_analyser',
    version='0.2.0',
    python_requires='>3.5.2',
    author ='Scm',
    author_email ='tisalon@outlook.com',
    description ='Simple package for analysing a tweeter list and produce a quick report.',
    long_description_content_type ="text/markdown",
    license ='MIT',
    include_package_data=True,
    packages = find_packages(),
    entry_points ={
            'console_scripts': [
                'tweet_analyser = app.main:command_args'
            ]
        },
    classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
    keywords ='Twitter spacy NLP python analysis',
    install_requires = requirements,
    zip_safe = False)