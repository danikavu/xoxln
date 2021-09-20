""" This code make random presets for XO XLN vst """

import os
import re
import random
import sqlite3
import numpy as np
import pandas as pd


SECURE_RANDOM = random.SystemRandom()

DEFAULT_XO_PATH = os.path.expanduser('~') + '\Documents\XO'
DEFAULT_XO_PATH = os.path.join(DEFAULT_XO_PATH, '00100','Data','sample.db')

CLASSIC = [16,8,4,2]
INNER_CLASSIC = [3,5,7,9,10,11,12,13,14,15]

class XO:
    
    samples_db = None 
    
    choke = False
    sample_len = 44000
    global_swing = True
    string_contains = False
    
    chosen_hashes = None
    chosen_samples_db = None
    
    pattern = None
    chosen_samples = None
    
    def __init__(self):
        """
            Search for XO database path.
        """
        if not os.path.exists(DEFAULT_XO_PATH):
            self.xo_db_path = None
        else:
            self.xo_db_path = DEFAULT_XO_PATH
    
    
    def xo_connect(self):
        """
            Create a connection for the XO database.
        """
        if not self.xo_db_path: 
            raise ValueError('Please provide XO database path')
        else:
            connection = sqlite3.connect(self.xo_db_path)
            _sample_data = pd.read_sql_query("SELECT * FROM samples", connection)
            _sample_data = _sample_data[8746:]
            _sample_data = _sample_data.loc[_sample_data['unsupported'] == '']
            self.samples_db = _sample_data

    
    def get_samples_set(self, df):
        """
            Create a new database from the filtered search.
        """
        if self.string_contains:
            _samples = df.loc[(df['length'] < self.sample_len) &
                             (df['filename'].str.contains("{}".format(self.string_contains)))].reset_index(drop=True)
        else:
            _samples = df.loc[df['length'] < self.sample_len].reset_index(drop=True)
        
        _hashes = [x for x in _samples['file_hash']]
        
        self.chosen_samples_db = _samples
        self.chosen_hashes = _hashes
    
    
    def choose_samples(self, 
                       db=chosen_samples_db, 
                       hashes=chosen_hashes):
        """
            Choose 8 samples from the new samples set.
        """
        _samples = []
        for x in range(8):
            h = SECURE_RANDOM.choice(hashes)
            hashes.remove(h)
            sample = db.loc[db['file_hash'] == h].reset_index(drop=True)
            _samples.append(sample['path'][0])
            _samples.append(sample['file_hash'][0])
            _samples.append(sample['coord_x'][0])
            _samples.append(sample['coord_y'][0])

        self.chosen_samples = _samples
        
    
    def samples_set(self):
        """
            Call to get samples.
        """
        self.get_samples_set(self.samples_db)
        self.choose_samples(self.chosen_samples_db, self.chosen_hashes)
        
        
    def make_pattern(self):
        """
            This can be greatly improved.
            Beta mode for making random patterns.
        """
        probability = random.SystemRandom().random()
        if probability < 0.1:
            _pattern = [0 for x in range(32)]
        elif probability > 0.5:
            pattern_num = SECURE_RANDOM.choice(CLASSIC)
            _probability = random.SystemRandom().random()
            if _probability > 0.80:
                _pattern = [1 if random.SystemRandom().random() < pattern_num/32 else 0 for x in range(1,33)]
            elif _probability < 0.40:
                _offset = random.SystemRandom().randint(2, 16)
                _pattern = [1 if (x == _offset) or (x % pattern_num == _offset) else 0 for x in range(1,33)]
            else:
                _pattern = [1 if (x == 1) or (x % pattern_num == 1) else 0 for x in range(1,33)]
        else:
            pattern_num = SECURE_RANDOM.choice(INNER_CLASSIC)
            _probability = random.SystemRandom().random()
            if _probability > 0.50:
                _pattern = [1 if (x == 1) or (x % pattern_num == 1) else 0 for x in range(1,33)]
            else:
                _pattern = [1 if random.SystemRandom().random() < pattern_num/32 else 0 for x in range(1,33)]

        if not self.global_swing:
            _probability = random.SystemRandom().random()
            if _probability > 0.3:
                _pattern.extend([random.SystemRandom().uniform(0.01, 0.5), random.SystemRandom().randint(1, 14), 0])
            else:
                 _pattern.extend([0,1,0])
        else: 
            _pattern.extend([0,1,1])    

        return _pattern
    
    
    def make_pattern_set(self):
        """
            Make patterns for all 8 slots.
        """
    
        _pattern = []
        for x in range(1,9):
            _pattern.append(self.make_pattern())
            
        self.pattern = _pattern
    
    
    def slot_choke(self):
        """
            Set if samples will choke or be random.
        """
        if self.choke:
            _choke = [1 for x in range(8)]
        else:
            _choke = [random.randint(0,4) for x in range(8)]
            
        return _choke
    
    
    def make_preset(self, filename=False, filepath=False):
        """
            Make the preset and save.
        """
        
        if not isinstance(self.samples_db, pd.DataFrame):
            raise ValueError('You must initiate a connection to the XO database first.')
            
        self.samples_set()
        self.make_pattern_set()
        
        default_preset_path = os.path.dirname(__file__) + '{s}default{s}xo_db_preset.txt'.format(s=os.sep)
        
        with open(default_preset_path, 'r') as xo:
            xo_read = xo.read()
        
        if self.global_swing:
            _swing = [0, 1]
        else:
            _swing = [random.SystemRandom().uniform(0.01, 0.5), random.SystemRandom().randint(1, 14)]

        xo_preset = xo_read.format(*_swing,
                                   *self.pattern[0],
                                   *self.pattern[1],
                                   *self.pattern[2],
                                   *self.pattern[3],
                                   *self.pattern[4],
                                   *self.pattern[5],
                                   *self.pattern[6],
                                   *self.pattern[7],
                                   *self.chosen_samples, 
                                   *self.slot_choke())
        
        if not filename:
            preset_name = 'xoxlnDefault.XOPreset'
        else:
            preset_name = filename + '.XOPreset'
        
        if not filepath:
            filepath = preset_name
        else:
            filepath = os.path.join(filepath, preset_name)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xo_preset)