import numpy as np
import pandas as pd
import cdm_bindings
from pycdm import PyCDM
import time
import scipy
import queue
import signal

cdm = PyCDM("172.16.17.25")
dq = cdm.reg_msg("DATA.FRAME")

def empty_queue(dq,buffer, chanels = range(20)):
    while (True):
            try:
                data = dq.get(block=False, timeout=0.01)[1]
                print(1)
            except queue.Empty:
                #print("Empty message")
                break
            decoder = cdm_bindings.FrameDecoder(data)
            header = decoder.get_header()
            for i in range(header.count):
                f = decoder.read_sumsq_frame()
                buffer[20].append(f.timestamp)
                for i in chanels:
                    buffer[i].append(f.data[i].sum/f.count)
                    buffer[i] = buffer[i][-2048:]       
    return buffer

def computefft(buffer, freq, result, chanels=range(20)):
    for i in chanels:
        y = np.fft.rfft(buffer[i])
        tempdf = pd.DataFrame(columns = freq, data =[y])
        tempdf['timestamp'] = time.time()
        tempdf.insert(0, 'timestamp', tempdf.pop('timestamp'))
        result[i] = pd.concat([result[i],tempdf])
    return result

def save_file(result, chanels=range(20)):
    for i in chanels:
        result[i].to_csv(time.strftime('%Y%m%d%H%M%S',time.gmtime())+f'-fft-{i}')
    

x = np.fft.rfftfreq(2048)
buffer = [[] for i in range(21)]
result = [pd.DataFrame() for i in range(20)]
first = True


while True:
    try:
        buffer = empty_queue(dq,buffer)#, chanels = [0,1])
        if first and len(buffer[0])== 2048:
            diff = np.diff(buffer[20])
            timestep = np.mean(diff)
            freq = np.fft.rfftfreq(2048,timestep/1.e6)
            refactor_time = time.time() - buffer[20][-1]/1.e6
            result = computefft(buffer, freq, result)#, chanels = [0,1])
            first= False
            #print(result)
            print('Computed fft')
        elif not first and time.time()-result[0]['timestamp'].iloc[-1] > 5 :
            ts = refactor_time + buffer[20]/1.e6
            if time.time() - ts[-1] > 0.1: raise Exception("Old data") 
            result = computefft(buffer, freq, result)#, chanels = [0,1])
            print('Computed fft')
            #print(result)
    except KeyboardInterrupt:
        print("Captured Ctrl+C")
        save_file(result)#,chanels=[0,1])
        break

cdm.close()