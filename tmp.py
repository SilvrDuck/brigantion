


from tqdm import tqdm
import os
import time

rows, columns = os.popen('stty size', 'r').read().split()
print(rows, columns)
columns = int(columns)
rows = int(rows)

for i in range(8):
        print(i, end='\r')
        #time.sleep(1)



with open('test.txt', 'r', encoding='latin-1') as f:
        line_cnt = 1
        for l in f:
                sublen = len(l) // columns + 1
                for i in range(sublen):
                        print(l[i*columns:min((i+1)*columns, len(l)-1)])
                        time.sleep(0.1)
                        line_cnt += 1
                        if line_cnt % (rows - 3) == 0:
                                #print(, end='\r')
                                input('<< Press enter to continue... >>')
                                print("\033[A                                          \033[A")
                                print('>> --------')
