from __future__ import division 
import numpy as np
from matplotlib import pyplot as plt
import scipy.signal as signal
import csv
import os
import string
from matplotlib import style
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def search(path=".", name="0"):#���ض�Ŀ¼�������ؼ����ļ���  
    """
��������·���͹ؼ���
���������ļ�·��
    """
    for item in os.listdir(path):  
        item_path = os.path.join(path, item)  
        if os.path.isdir(item_path):  
            search(item_path, name)  
        elif os.path.isfile(item_path):  
            if name in item:  
                return item_path          

def read_wavecsv(name_key,search_path="C:\Users\Ludwig\Desktop\pythonworkspace",ch = 2):#��ȡָ��·���µ�ָ���ؼ����ļ��ĵ�ѹ��ʱ������
    """
����csv�ļ��ؼ��ֺ�����·��
���(ʱ������,��ѹ����)
    """
    data1 = csv.reader(open(search(search_path,name_key)))
    second_temp = np.array([x[0] for x in data1])
    data2 = csv.reader(open(search(search_path,name_key)))
    volt_temp = np.array([y[ch] for y in data2])
    second = []
    for index1 in second_temp:
        try:
            second.append(string.atof(index1))
        except ValueError:
            continue
    volt = []
    for index2 in volt_temp:
        try:
            volt.append(string.atof(index2))
        except ValueError:
            continue
    if volt[0] == 1:
        del volt[0]
    elif len(volt) == 1999:
        volt.append(volt[len(volt)-1])
    else:
        pass
    return (second,volt)

#
#          max.
#            . .
#           .   .
#          .     .
#        1.       .1
#        .         .
#       .           .
#*******    argmax   *************
#������λ������
def cal_wavepara(array):
    """        
�����������У�������λ�����кͷ���
((��������),(Դ�źű���״̬��1Ϊ�����أ�2Ϊ�½���))
    """
    out = []
    signal = []
    index1 = 0
    for index in range(0, len(array)):
        if index < index1:#�����ѱ�[index:index1+1]��Ƭ��������ֵ
            continue
        else:
           if abs(array[index]) > 1:#������������Χ��ֵ
            for index1 in range(index, len(array)):
                if abs(array[index1]) < 1:
                    out.append(np.argmax(array[index:index1+1])+index)
                    if array[index] > 0:
                        signal.append(1)
                    elif array[index] < 0:
                        signal.append(-1)
                    break
    return (out,signal)


def measure(edge=[],second=[],volt=[]):
    """
��������
�������������У�ʱ�����У���ѹ����
���((�ߵ�ƽʱ��,�͵�ƽʱ��),(�ߵ�ƽ��ѹ,�͵�ƽ��ѹ))
    """
    if edge[1][0] == 1:
        high_period = ((edge[0][1]-edge[0][0])/2000)*(second.max()-second[0])
        low_period = ((edge[0][2]-edge[0][1])/2000)*(second.max()-second[0])
        high_volt = volt[int((edge[0][1]-edge[0][0])/2)+edge[0][0]]
        low_volt = volt[int((edge[0][2]-edge[0][1])/2)+edge[0][1]]
    else:
        low_period = ((edge[0][1]-edge[0][0])/2000)*(second.max()-second[0])
        high_period = ((edge[0][2]-edge[0][1])/2000)*(second.max()-second[0])
        low_volt = volt[int((edge[0][1]-edge[0][0])/2)+edge[0][0]]
        high_volt = volt[int((edge[0][2]-edge[0][1])/2)+edge[0][1]]
    return (high_period,low_period),(high_volt,low_volt)



def main_process(name_key,search_path="C:\Users\Ludwig\Desktop\pythonworkspace",ch = 2):
    data = read_wavecsv(name_key,search_path,ch)
    second = np.array(data[0])#������ʱ������
    volt = np.array(data[1])#�����ĵ�ѹ����
   
    if ch == 2:
        name = raw_input("file number:%s the singal is:"%name_key)
        volt_medfilt = signal.medfilt(volt,kernel_size=3)#��ֵ�˲�
        volt_medfilt_diff = np.diff(volt_medfilt)#�������
        edge = cal_wavepara(volt_medfilt_diff)#�������     
        measurement  = measure(edge,second,volt)
        high_period = measurement[0][0]
        low_period = measurement[0][1]
        high_volt = measurement[1][0]
        low_volt = measurement[1][1]
        
        print "Ƶ��=%d����"%(1/(high_period+low_period))
        print "�ߵ�ƽʱ��:%.2f΢��"%np.round(high_period*1000000,2)
        print "�͵�ƽʱ��:%.2f΢��"%np.round(low_period*1000000,2)
        print "�ߵ�ƽ��ѹ:%.2f����"%np.round(high_volt)
        print "�͵�ƽ��ѹ:%.2f����"%np.round(low_volt)
        plt.plot(np.arange(0,len(volt))*(second.max()-second[0])/2,volt+string.atoi(name_key)*30,label=name,linewidth=0.5)
        plt.plot(np.arange(0,len(volt))*(second.max()-second[0])/2,
                 string.atoi(name_key)*30+np.ones_like(np.arange(0,len(volt))*(second.max()-second[0]))*0,'--',linewidth=0.3)
        #plt.yticks(volt+string.atoi(name_key)*30,name,rotation=30)
        return measurement
    elif ch == 1:
        name = raw_input("the name of reference signal")
        plt.plot(np.arange(0,len(volt))*(second.max()-second[0])/2,volt+(string.atoi(name_key)-1)*30,label=name,linewidth=0.5)
        plt.plot(np.arange(0,len(volt))*(second.max()-second[0])/2,
                 (string.atoi(name_key)-1)*30+np.ones_like(np.arange(0,len(volt))*(second.max()-second[0]))*0,'--',linewidth=0.3)



###############################################################
#                                                             #
#                     ��������ִ�к���                         #
#                                                            #
#############################################################
 
name_key = raw_input("Please input the <start number> of wave_date:")
date_count = input("Please intput the amount of wave_data:")
main_process("0",ch=1)#��׼�����ź�
for index in xrange(string.atoi(name_key),date_count):
    try:
        main_process("%d"%index)
    except TypeError:
        continue
#��ȡCSV���ݺ������� 

ax=plt.gca() 
xmajorLocator   = MultipleLocator(0.01)#��x���̶ȱ�ǩ����Ϊ20�ı���  
#xmajorFormatter = FormatStrFormatter('%1.1f') #����x���ǩ�ı��ĸ�ʽ 
xminorLocator   = MultipleLocator(0.001) #��x��ο̶ȱ�ǩ����Ϊ5�ı���  

ymajorLocator   = MultipleLocator(10) #��y�����̶ȱ�ǩ����Ϊ0.5�ı���  
#ymajorFormatter = FormatStrFormatter('%1.1f') #����y���ǩ�ı��ĸ�ʽ  
yminorLocator   = MultipleLocator(1) #����y��ο̶ȱ�ǩ����Ϊ0.1�ı���  




#�������̶ȱ�ǩ��λ��,��ǩ�ı��ĸ�ʽ  
ax.xaxis.set_major_locator(xmajorLocator)  
#ax.xaxis.set_major_formatter(xmajorFormatter)  
  
ax.yaxis.set_major_locator(ymajorLocator)  
#ax.yaxis.set_major_formatter(ymajorFormatter)  
  
#��ʾ�ο̶ȱ�ǩ��λ��,û�б�ǩ�ı�  
ax.xaxis.set_minor_locator(xminorLocator)  
ax.yaxis.set_minor_locator(yminorLocator)  

ax.grid(True, color = "#054E9F",linewidth=0.1) 
plt.xlabel("time/ms")
plt.ylabel("voltage/V")
plt.legend()
style.use("ggplot")
plt.show()
