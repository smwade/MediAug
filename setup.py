from setuptools import setup

def readme():
      with open('README.md') as f:
            return f.read()

setup(name='mediaug',
      version='0.1',
      description='Image augmentation tools for cell images',
      long_description=readme(),
      url='https://github.com/smwade/MediAug',
      author='Sean Wade',
      license='MIT',
      author_email='seanwademail@gmail.com',
      packages=['mediaug'],
      install_requires=[
            'Augmentor',
            'numpy',
            'Pillow',
            'opencv_python',
            'tqdm',
            'scikit-image'
      ],
      entry_points={
            'console_scripts': [
                  'mediaug-test=mediaug.command_line:main',
                  'mediaug-test2=mediaug.command_line:resize_image',
            ],
      },
      include_package_data=True,
      zip_safe=False
     )
