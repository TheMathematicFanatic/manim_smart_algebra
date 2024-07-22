from setuptools import setup, find_packages

setup(
    name='manim_smart_algebra',
    version='0.3.1',
    description='Manim plugin which subclasses MathTex to make it much easier to animate algebra.',
    author='John Connell - The Mathematic Fanatic',
    author_email='johnconnelltutor@gmail.com',
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'manim>=0.18.0'  # Specify dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
    include_package_data=True,
    package_data={ # I don't think I need this
        '': ['*.py'],  # Include all Python files
    },
)
