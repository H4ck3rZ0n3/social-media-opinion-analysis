from setuptools import setup, find_packages

# requirements.txt dosyasını okuyup bağımlılıkları alır
def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    # Yorum satırlarını ve boş satırları filtreler
    requirements = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return requirements

setup(
    name='socialMediaNew',  # Paketinizin adı
    version='1.0.0',  # Sürüm numarası
    author='Uğur Ortaç',  # Yazar adı
    author_email='info@ugurortac.com',  # Yazarın e-posta adresi
    description='Social Media Analysis with GPU Support',  # Kısa açıklama
    long_description=open('README.md').read(),  # Uzun açıklama (README dosyası)
    long_description_content_type='text/markdown',  # README dosyasının formatı
    url='https://github.com/yourusername/socialMediaNew',  # Projenizin URL'si
    packages=find_packages(where='src'),  # Paketlerin bulunduğu dizin
    package_dir={'': 'src'},  # Paketlerin kök dizini
    install_requires=parse_requirements('requirements.txt'),  # Bağımlılıklar
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Lisans türü
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Python sürüm gereksinimi
    entry_points={
        'console_scripts': [
            'socialMediaNew=main:main',  # Komut satırı komutu (isteğe bağlı)
        ],
    },
)