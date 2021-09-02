import setuptools

setuptools.setup(
    packages=["mashcima"],
    install_requires=[
        # mashcima dependencies
        'numpy>=1.11.1',
        'opencv-python>=3.4.8.29',
        'muscima>=0.10.0',

        # missing dependencies for the 'muscima' package
        'scipy>=1.5.4',
        'scikit-image>=0.18.0'
    ]
)
