from setuptools import setup, find_packages

# Reads the requirements.txt file and extracts dependencies
def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    # Filters out comment lines and empty lines
    requirements = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return requirements

setup(
    name='social-media-opinion-analysis',  # Name of the package
    version='1.0.0',  # Version number
    author='Uğur Ortaç',  # Author's name
    author_email='info@ugurortac.com',  # Author's email address
    description='Social Media Opinion Analysis with GPU Support',  # Short description
    long_description=open('README.md').read(),  # Long description (README file)
    long_description_content_type='text/markdown',  # Format of the README file
    url='https://github.com/H4ck3rZ0n3/social-media-opinion-analysis',  # Project URL
    packages=find_packages(where='src'),  # Directory where packages are located
    package_dir={'': 'src'},  # Root directory of the packages
    install_requires=parse_requirements('requirements.txt'),  # Dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU License 3.0',  # Type of license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Minimum required Python version
    entry_points={
        'console_scripts': [
            'social-media-opinion-analysis=main:main',  # Command-line command (optional)
        ],
    },
)