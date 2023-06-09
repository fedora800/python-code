

amer_list, apac_list, emea_list = [], [], []

for proc_name in ['IndicationManager_Asia_0-4', 'IndicationManager_Europe_A-C',
                  'IndicationManager_USA_D-E', 'IndicationManager_Asia_N-Z',
                  'IndicationManager_Canada_0-K', 'IndicationManager_Canada_L-Z',
                  'IndicationManager_Europe_M-O', 'IndicationManager_Asia_5-9',
                  'IndicationManager_Europe_S-T', 'IndicationManager_Europe_U-Z']:
    print('\Procname= ' + proc_name)
    if ('USA' in proc_name or 'Canada' in proc_name):
        print('---11--- ' + proc_name)
        amer_list.append(proc_name)
        print('==NOW AMER LIST==')
        print(amer_list)
    elif 'Asia' in proc_name:
        apac_list.append(proc_name)
        print('==NOW APAC LIST==')
        print(apac_list)
    elif 'Europe' in proc_name:
        emea_list.append(proc_name)
        print('==NOW EMEA LIST==')
        print(emea_list)
    print('End of Loop')
