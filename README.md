## xoxln (beta version)

This module creates random presets for the XO vst. [XO by XLN AUDIO](https://www.xlnaudio.com/products/xo)

Only uses the samples you have added to XO. Default sounds excluded.

Pattern creation is currently a bit sloppy. -Working on it-

### Requirements

The XO vst.

Python 3.7 or higher.

### Installation

1 - Clone this repo.

2 - Inside repo folder run commands below

	python setup.py bdist_wheel
	
3 - Inside generated dist folder run 

	pip install xoxln-1.0.0-py3-none-any.whl
	

### Usage

	import xoxln
	
	# Set the XO instance.
	xo = xoxln.XO()  
	
	# Create the database connection.
	xo.xo_connect()
		
	# Create a preset
	xo.make_preset()
	
	# You can provide a filename and a path for the export
	xo.make_preset(filename='xoxlnpython', filepath='C:/somefilepath')
	
	
### Additional info/parameters	

If the XO database sample path is not found by the instance you will have to provide it yourself.
	
	# Default Windows path is 'C:\Users\USERNAME\Documents\XO\00100\Data'
	xo.xo_db_path = 'PATH_TO/sample.db'

Currently there are a few parameters you can modify in the XO instance.

	# Choke parameter which specifies if samples will overlap or choke between each other, default False
	xo.choke = True 
	
	# The sample length max duration in samples, default 44000
	xo.sample_len = 20000
	
	# The global swing controls overall swing of preset, default True. Global swing currently chooses a random swing type.
	xo.global_swing = False 
	
	# String contains search, searches a string within the filename, default False
	xo.string_contains = 'G#' # Search for samples containing G# inside path
	

### TODO

- Add all parameters
- Make sample search options flexible
- Add pattern making from MIDI input
- Add sample swapping between presets
- Add proper documentation 

# Generated loops with xoxln

With Global Swing disabled

https://user-images.githubusercontent.com/51134703/133932735-6aedf50b-5b84-4a42-953f-375dbbc5e710.mov

https://user-images.githubusercontent.com/51134703/133932750-da2c379b-9ecb-4c91-a2ab-5ea77b313e9d.mov

https://user-images.githubusercontent.com/51134703/133932759-0b550b8d-4fff-4756-b79c-d10b960248ed.mov


With Global Swing enabled

https://user-images.githubusercontent.com/51134703/133932844-eff614a5-2aad-43e1-9653-743439d84915.mov

https://user-images.githubusercontent.com/51134703/133932851-721da498-9b7b-43ab-a8b7-ad2d851f19d1.mov

https://user-images.githubusercontent.com/51134703/133932854-da775a6e-1ea0-433b-a2a2-04312eeeff27.mov



