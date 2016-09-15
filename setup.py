__version__ = 0.01

kwargs = dict(
    name='immutable_evolver',
    description=(
        'A little Python helper to make building immutable objects and '
        'changing them a piece of cake!'),
    author='Paul Weaver',
    author_email='paul@ruthorn.co.uk',
    version=__version__,
    packages=['immutable_evolver'],
    install_requires=[
        'pyrsistent',
    ],
    extras_require={
        'dev': [
            'pytest',
        ]
    },
)

if __name__ == '__main__':
    from setuptools import setup
    setup(**kwargs)
