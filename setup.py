import setuptools

setuptools.setup(
    packages=[
        "mashcima",
        "mashcima.canvas_items",
        "mashcima.default_symbols",
        "mashcima.inspections"
    ],
    package_data={
        "mashcima.default_symbols": ["*.png", "*.txt"]
    },
    include_package_data=True,
    install_requires=[
        # mashcima dependencies
        'numpy>=1.11.1',
        'opencv-python>=3.4.8.29',
        'muscima>=0.10.0',
        'appdirs>=1.4.4',
        'tqdm>=4.40.0',
        'requests>=2.15.1'

        # missing dependencies for the 'muscima' package
        'scipy>=1.5.4',
        'scikit-image>=0.18.0'
    ]
)
