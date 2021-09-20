from setuptools import setup

setup(
	name='xoxln',
	version='1.0.0',
	author='Daniel Kavoulakos',
	author_email='dan_kavoulakos@hotmail.com',
	description='Creates random presets for XO XLN vst',
	license='MIT',
	packages=['.xoxln'],
    package_data={'.xoxln': ['default/*']},
	install_requires=['numpy',
					  'pandas',
					  ],
	python_requires='>=3.7',
)
					  