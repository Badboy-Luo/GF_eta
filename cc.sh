# This shell script is to launch cross-correlation jobs between every 

rm -rf STACKS MWCS DTT db.ini msnoise.sqlite

msnoise db init --tech 1

msnoise config set startdate=2019-08-01
msnoise config set enddate=2021-08-31
msnoise config set components_to_compute=ZZ   # NN, EE or ZZ depending on which component you use
# msnoise config set remove_response='Y'
# msnoise config set response_format=inventory
# msnoise config set response_path='./station'
# msnoise config set response_prefilt=0.01,0.05,99,99.5

msnoise config set preprocess_lowpass=99
msnoise config set preprocess_highpass=0.1
msnoise config set cc_sampling_rate=200
msnoise config set preprocess_max_gap=86400

msnoise config set mov_stack=1,5,10
msnoise config set stack_method='linear'

msnoise config set data_structure=custom.py
msnoise config set data_folder=station
msnoise populate


msnoise config set maxlag=3
msnoise config set overlap=0.5
msnoise config set keep_days=Y
msnoise config set analysis_duration=86400  # 1 day
msnoise config set corr_duration=1800  # seconds
msnoise config set hpc='Y'

msnoise db execute 'insert into filters (ref, low, mwcs_low, high, mwcs_high, rms_threshold, mwcs_wlen, mwcs_step, used) values (1, 1, 1, 99, 99, 0.0, 12.0, 4.0, 1)'



msnoise scan_archive --path ../../Iceland_data/HHZ/ --recursively --init
msnoise new_jobs

msnoise -t 4 compute_cc

msnoise reset -a STACK
msnoise new_jobs --hpc CC:STACK
msnoise stack -r
msnoise reset STACK
msnoise stack -m


