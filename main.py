import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as spi
import math 


def sep():

    plt.figure(figsize=(8, 8))
    goes.plot()
    plt.ylabel('FPDO')
    plt.yscale('log')
    plt.show()

    energy = [10, 20, 30, 50, 70, 80]

    plt.figure(figsize=(8, 8))
    plt.plot(np.log(energy),goes.max(),'o-')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid()
    plt.ylabel('FPDO')
    plt.xlabel('Energy')
    plt.title('SPE differential proton flux spectrum (max)')
    plt.yscale('log')
    plt.show()

    slope_intercept = np.polyfit(np.log(energy),goes.max(),1)
    print("\ndifferential proton flux spectrum (max):  ")
    print(slope_intercept[0])

    
    plt.figure(figsize=(8, 8))
    plt.plot(np.log(energy),goes_all_m,'o-')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid()
    plt.ylabel('FPDO')
    plt.xlabel('Energy')
    plt.title('SPE differential proton flux spectrum (mean)')
    plt.yscale('log')
    plt.show()

    slope_intercept1 = np.polyfit(np.log(energy),goes_all_m[:,0],1)
    print("\ndifferential proton flux spectrum (mean):  ")
    print(slope_intercept1[0])

    int1 = np.trapz(np.log(energy),goes.max())
    print("\nFPDO max integral : ")
    print(int1)


    energy_int1 = np.arange(10,80, 2)
    xnew1 = np.array(np.log(energy_int1))
    int12 = np.array(math.exp(slope_intercept[1]) * (xnew1 ** slope_intercept[0]))      #power law 

    x0= xnew1[0]
    xn = xnew1[-1]
    n = 17

    h = (xn-x0)/n      
    
    inter1 = int12[0]  + int12[-1]
    for i in range(1,n):
        k = x0+ i*h
        k = int(k)
        inter1 = inter1 + 2* int12[k]
    inter1 = inter1 *h/2 
    print("\nFPDO max integral (power law): ")
    print(inter1)


    int2 = np.trapz(np.log(energy),goes_all_m[:,0])
    print("\nFPDO mean integral : ")
    print(int2)


    energy_int = np.arange(10,80, 2)
    xnew = np.array(np.log(energy_int))
    int22 = np.array(math.exp(slope_intercept1[1]) * (xnew ** slope_intercept1[0]))      #power law 

    x0= xnew[0]
    xn = xnew[-1]
    n = 17

    h = (xn-x0)/n      
    
    inter = int22[0]  + int22[-1]
    for i in range(1,n):
        k = x0+ i*h
        k = int(k)
        inter = inter + 2* int22[k]
    inter = inter *h/2 
    print("\nFPDO mean integral (power law): ")
    print(inter)


    print('\nDatetime of the max values:')
    l = goes.idxmax()
    print(l)

    max= goes.max()
    ar = np.array(max ** 10)
    
    out =[]
    print("\nS NOASS's scale for the max values")
    for i in ar:

        if ( i >= 10^5):
            out.append ("S5")
        elif (( i>= 10^4) &(i < 10^5) ):
            out.append ("S4")
        elif (( i>= 10^3) & (i < 10^4) ):
            out.append ("S3")
        elif ((i < 10^3) &( i>= 10^2)):
            out.append ("S2")
        elif (i <= 10):
            out.append ("S1")
        
    print(out)

    mean= goes_all_m[:,0]
    arr = np.array(mean ** 10)
    
    out2 =[]
    print("\nS NOASS's scale for the mean values")
    for i in arr:

        if ( i >= 10^5):
            out2.append ("S5")
        elif (( i>= 10^4) &(i < 10^5) ):
            out2.append ("S4")
        elif (( i>= 10^3) & (i < 10^4) ):
            out2.append ("S3")
        elif ((i < 10^3) &( i>= 10^2)):
            out2.append ("S2")
        elif (i <= 10):
            out2.append ("S1")
        
    print(out2)
    
ask = input("Please choose a SEP\n1. 2011-06-03:2011-06-21\n2. 2006-12-06:2006-12-18\n")

if ask in ['1']:

    fname='./SEP_H_GOES13.txt'
    colnames=['epoch', 'FPDO_1', 'FPDO_2','FPDO_3','FPDO_4','FPDO_5','FPDO_6'] 

    goes=pd.read_csv(fname,sep=',',skiprows=1,names=colnames,header=None)
    goes['epoch']=pd.to_datetime(goes['epoch'])
    goes  = goes.set_index('epoch')   

    goes = goes['2011-06-03':'2011-06-21']

    mask1 = goes['2011-06-03':'2011-06-04'].rolling(3).mean()
    mask12 = goes['2011-06-21':'2011-06-21'].rolling(3).mean()
    mask13 = goes['2011-06-04':'2011-06-21']

    mask = pd.concat ([mask1,mask12,mask13])
    tmask = pd.DataFrame(mask, columns=['FPDO_1'])

    mask2 = goes['2011-06-03':'2011-06-04'].rolling(3).mean()
    mask22 = goes['2011-06-19':'2011-06-21'].rolling(3).mean()
    mask23 = goes['2011-06-04':'2011-06-19']

    mask2 = pd.concat ([mask2,mask22,mask23])
    tmask2 = pd.DataFrame(mask2, columns=['FPDO_2'])

    mask3 = goes['2011-06-03':'2011-06-04'].rolling(3).mean()
    mask32 = goes['2011-06-18':'2011-06-21'].rolling(3).mean()
    mask33 = goes['2011-06-04':'2011-06-18']

    mask3 = pd.concat ([mask3,mask32,mask33])
    tmask3 = pd.DataFrame(mask3, columns=['FPDO_3'])

    mask4 = goes['2011-06-03':'2011-06-05'].rolling(3).mean()
    mask42 = goes['2011-06-11':'2011-06-21'].rolling(3).mean()
    mask43 = goes['2011-06-05':'2011-06-11']

    mask4 = pd.concat ([mask4,mask42,mask43])
    tmask4 = pd.DataFrame(mask4, columns=['FPDO_4'])

    mask5 = goes['2011-06-03':'2011-06-07'].rolling(3).mean()
    mask52 = goes['2011-06-09':'2011-06-21'].rolling(3).mean()
    mask53 = goes['2011-06-07':'2011-06-09']

    mask5 = pd.concat ([mask5,mask52,mask53])
    tmask5 = pd.DataFrame(mask5, columns=['FPDO_5'])

    mask6 = goes['2011-06-03':'2011-06-07'].rolling(3).mean()
    mask62 = goes['2011-06-09':'2011-06-21'].rolling(3).mean()
    mask63 = goes['2011-06-07':'2011-06-09']

    mask6= pd.concat ([mask6,mask62,mask63])
    tmask6 = pd.DataFrame(mask6, columns=['FPDO_6'])

    
    goes_all = [tmask.mean(),tmask2.mean(),tmask3.mean(),tmask4.mean(),tmask5.mean(),tmask6.mean()]
    goes_all_m = np.array(goes_all)

    sep()
elif ask in ['2']:

    fname='./SEP_H_GOES11.txt'
    colnames=['epoch', 'FPDO_1', 'FPDO_2','FPDO_3','FPDO_4','FPDO_5','FPDO_6'] 

    goes=pd.read_csv(fname,sep=',',skiprows=1,names=colnames,header=None)
    goes['epoch']=pd.to_datetime(goes['epoch'])
    goes  = goes.set_index('epoch')   

    goes = goes['2006-12-06':'2006-12-18']

    mask1 = goes['2006-12-06':'2006-12-06'].rolling(3).mean()
    mask12 = goes['2006-12-17':'2006-12-18'].rolling(3).mean()
    mask13 = goes['2006-12-06':'2006-12-17']

    mask = pd.concat ([mask1,mask12,mask13])
    tmask = pd.DataFrame(mask, columns=['FPDO_1'])

    mask2 = goes['2006-12-06':'2006-12-06'].rolling(3).mean()
    mask22 = goes['2006-12-16':'2006-12-18'].rolling(3).mean()
    mask23 = goes['2006-12-06':'2011-06-16']

    mask2 = pd.concat ([mask2,mask22,mask23])
    tmask2 = pd.DataFrame(mask2, columns=['FPDO_2'])

    mask3 = goes['2006-12-06':'2006-12-06'].rolling(3).mean()
    mask32 = goes['2006-12-16':'2006-12-18'].rolling(3).mean()
    mask33 = goes['2006-12-06':'2006-12-16']

    mask3 = pd.concat ([mask3,mask32,mask33])
    tmask3 = pd.DataFrame(mask3, columns=['FPDO_3'])

    mask4 = goes['2006-12-06':'2006-12-06'].rolling(3).mean()
    mask42 = goes['2006-12-16':'2006-12-18'].rolling(3).mean()
    mask43 = goes['2006-12-06':'2006-12-16']

    mask4 = pd.concat ([mask4,mask42,mask43])
    tmask4 = pd.DataFrame(mask4, columns=['FPDO_4'])

    mask5 = goes['2006-12-06':'2006-12-07'].rolling(3).mean()
    mask52 = goes['2006-12-16':'2006-12-18'].rolling(3).mean()
    mask53 = goes['2006-12-07':'2006-12-16']

    mask5 = pd.concat ([mask5,mask52,mask53])
    tmask5 = pd.DataFrame(mask5, columns=['FPDO_5'])

    mask6 = goes['2006-12-06':'2006-12-07'].rolling(3).mean()
    mask62 = goes['2006-12-16':'2006-12-18'].rolling(3).mean()
    mask63 = goes['2006-12-07':'2006-06-16']

    mask6= pd.concat ([mask6,mask62,mask63])
    tmask6 = pd.DataFrame(mask6, columns=['FPDO_6'])

    
    goes_all = [tmask.mean(),tmask2.mean(),tmask3.mean(),tmask4.mean(),tmask5.mean(),tmask6.mean()]
    goes_all_m = np.array(goes_all)


    sep()

else:
    print("error")
