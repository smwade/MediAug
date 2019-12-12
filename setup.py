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
            'scikit-image',
            'click',
            'ipython'
      ],
      entry_points={
            'console_scripts': [
                'mediaug=mediaug.command_line:cli'
            ],
      },
      include_package_data=True,
      zip_safe=False
     )
