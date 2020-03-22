import setuptools

with open('README.md', 'r') as fh:
	readme = fh.read()

setuptools.setup(
	name='crono',
	version='0.1.0',
	author='Georges Duverger',
	author_email='georges.duverger@gmail.com',
	description='Programmatic time-based job scheduler',
	long_description=readme,
	long_description_content_type='text/markdown',
	url='https://github.com/gduverger/crono',
	license='MIT',
	packages=['crono'],
	# install_requires=[],
	python_requires='>=3',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
		'Natural Language :: English'
	],
)