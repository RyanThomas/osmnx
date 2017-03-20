import matplotlib as mpl
mpl.use('Agg') #use agg backend so you don't need a display on travis-ci

import os, shutil
if os.path.exists('.temp'):
    shutil.rmtree('.temp')

from .. import osmnx
import logging as lg
ox.config(log_console=True, log_file=True, use_cache=True,
          data_folder='.temp/data', logs_folder='.temp/logs', imgs_folder='.temp/imgs', cache_folder='.temp/cache')

ox.log('test debug', level=lg.DEBUG)
ox.log('test info', level=lg.INFO)
ox.log('test warning', level=lg.WARNING)
ox.log('test error', level=lg.ERROR)
