# Them cac thu vien neu can
import math
from math import sqrt
import random
import numpy as np
import time

def assign(file_input, file_output):
    class Status:
        def __init__(self, locStore, numOrder, numShipper, listOrder):
            self.locateStore = locStore         # vị trí kho hàng
            self.order = numOrder               # tổng số lượng đơn hàng
            self.shipper = numShipper           # tổng shipper
            self.listOrder = listOrder          # List thành phần đơn hàng
        """
        input : lst [id_đơn_hàng, location_đơn_hàng, thể_tích, trọng_lượng]
        output: Tổng công f(i)
        """
        def LoiNhuan(self, lstDonHang):
            doanhThu = 0
            tongKhoangCach = 0
            for i in range(len(lstDonHang)):
                doanhThu += (5 + float(lstDonHang[i][2]) + (float(lstDonHang[i][3])*2))
                if i == 0:
                    tongKhoangCach += sqrt(pow(float(self.locateStore[0]) - float(lstDonHang[i][1][0]), 2) + pow(float(self.locateStore[1]) - float(lstDonHang[i][1][1]), 2))
                    if len(lstDonHang) != 1:
                        tongKhoangCach += sqrt(pow(float(lstDonHang[i][1][0]) - float(lstDonHang[i+1][1][0]), 2) + pow(float(lstDonHang[i][1][1]) - float(lstDonHang[i+1][1][1]), 2))
                elif i < len(lstDonHang) - 1:
                    tongKhoangCach += sqrt(pow(float(lstDonHang[i][1][0]) - float(lstDonHang[i+1][1][0]), 2) + pow(float(lstDonHang[i][1][1]) - float(lstDonHang[i+1][1][1]), 2))
            chiPhi = (tongKhoangCach/40)*20 + 10
            return doanhThu - chiPhi

    def readFile(file):
        with open(file) as file:
            str = file.readline()
            pos = tuple(map(lambda x: eval(x), str.split(' ')))
            str = file.readline().split(' ')
            mSaleman = eval(str[0])
            nCity = eval(str[1])
            orders = []
            count = 0
            a = 0
            while a < nCity:
                str = file.readline()
                str = list(map(lambda x: eval(x), str.split(' ')))
                orders.append([count, (str[0], str[1]), str[2],str[3]])
                count += 1
                a += 1
        return pos, nCity, mSaleman, orders

    def minimize(lst):
        tong = 0
        a = []
        b = []
        temp = 0
        for i in range(len(lst)):
            for j in range(i, len(lst)):
                if i != j:
                    tong += abs(lst[i] - lst[j])
                    a.append(abs(lst[i] - lst[j]))
                    if i == 0 and j == 1:
                        temp = abs(lst[i] - lst[j])
                        b = (i, j)
                    else:
                        if temp < abs(lst[i] - lst[j]):
                            temp = abs(lst[i] - lst[j])
                            b= (i,j)
        return tong

    def distance(a, b):
        result = 0
        result = sqrt(pow(float(a[0]) - float(b[0]), 2) + pow(float(a[1])- float(b[1]), 2))
        return result

    def takeThird(elem):
        return elem[2]

    def takeSecond(elem):
        return elem[1]

    # return f cua tung cai
    def aStar(begin, end, lst, nOrder):
        openSet = []
        lenList = len(lst)
        # Tap khoi dau tu diem xuat phat
        for i in range(lenList):
            # duong di | total g | f
            if lst[i] != end :
                duongdi = lst[i]
                totalG = distance(begin, lst[i][1])
                h = distance(lst[i][1], end[1])
                openSet.append([[duongdi], totalG, h+totalG])     
        while openSet:
            openSet.sort(key=takeThird)
            if len(openSet[0][0]) == len(lst) - 1:
                minF = openSet[0]
                minF[0].append(end)
                Sol = Status(lStore, nOrder, nShipper, minF[0])          
                return minF[0], Sol.LoiNhuan(minF[0])
            for i in range(lenList):           
                minF = openSet[0]
                minG = minF[1]
                if lst[i] not in minF[0] and lst[i] != end:
                    duongdi = lst[i]
                    totalG = minG + distance(minF[0][-1][1], lst[i][1])
                    h = distance(lst[i][1], end[1])
                    minF[0].append(duongdi)
                    minF[1] = totalG
                    minF[2] = h + totalG
                    openSet.append(minF)
            openSet.remove(openSet[0])
        return None

    def sum(nShipper, lStore, nOrder, lOrder):
        nShipper = int(nShipper)
        nOrder = int(nOrder)
        lstOut = []
        listF = np.empty(nShipper, dtype=list)
        random.shuffle(lOrder)
        random.shuffle(lOrder)
        #create init
        t = 0
        for i in lOrder:
            if t < nShipper:    
                listF[t] = [i]
                t += 1
            else:
                a = random.randint(0,nShipper-1)
                listF[a].append(i)
        begin = lStore
        for i in listF:
            numO = len(i)
            if numO == 1:
                Sol = Status(lStore, nOrder, nShipper, lOrder)
                newFofI = Sol.LoiNhuan(i)
                lstOut.append([i, newFofI]) 
            else:
                newFofI = []
                for j in range(numO):
                    end = i[j]
                    out1, out2 = aStar(begin, end, i, nOrder)
                    if out1 != []: #and out2 > 0:
                        newFofI.append([out1, out2])
                lstOut.append(newFofI)
        return lstOut


    """
    lOrder: id || locate || the tich | trong luong
    """
    # read data
    f = open("input.txt", "r")
    lStore, nOrder, nShipper, lOrder = readFile("input.txt")
    if nShipper > nOrder:
        print("Error: shipper quantity larger than order")
        file = open("output.txt", "w")
        file.write("")
        return
    time_train = float(input("Enter the time to receive the results (s): "))
    yes = int(input("Do you want to see minimize each training\n1. yes\n2. no\nYour choice: "))
    Sol = Status(lStore, nOrder, nShipper, lOrder)
    min_main = 0
    duongDi_main = []
    count_main = 1
    timee = 0
    b = 10
    a = 0
    time_begin = time.time()
    time_end = 0
    while (time_end - time_begin) < time_train:
        if yes == 1 and min_main != 0:
            print("Minimize %s: %s"%(str(timee) ,str(min_main)))
        timee+=1
        a = count_main
        count = 0
        hopLe = 1
        exist = []
        while count < a:
            listF = sum(nShipper, lStore, nOrder, lOrder)
            count += 1
            if len(listF) == int(nShipper):
                if listF not in exist:
                    exist.append(listF)
                    hopLe += 1
                    for i in range(len(listF)):
                        if len(listF[i]) != 1:
                            try:
                                listF[i].sort(key=takeSecond)
                            except:
                                continue
        duongDi = []
        totalF = []
        for no in range(len(exist)):
            minF = []
            duong = []
            for i in range(len(exist[no])):
                tempF = []
                tempDuongDi = []
                for j in range(len(exist[no][i])):
                    try:
                        tempF.append(exist[no][i][j][1])
                        tempDuongDi.append(exist[no][i][j][0])
                    except:
                        tempF.append(exist[no][i][1])
                        tempDuongDi.append(exist[no][i][0])
                        break
                minF.append(tempF)
                duong.append(tempDuongDi)
            totalF.append(minF)
            duongDi.append(duong)
        minResult = 0
        temp = []
        duongdiResult = []
        limit = 0
        while 1:
            for no in range(len(totalF)):
                total = []
                total2 = []
                for i in range(len(totalF[no])):
                    s = random.randint(0, len(totalF[no][i])-1)
                    total.append(totalF[no][i][s])
                    total2.append([duongDi[no][i][s], totalF[no][i][s]])
                total = minimize(total)
                if minResult == 0:
                    minResult = total
                    duongdiResult = total2
                if minResult > total:
                    minResult = total
                    duongdiResult = total2
                    limit = 0
                else:
                    limit += 1
            if limit > 5000:
                break
        if count_main == 1:
            min_main = minResult
            duongDi_main = duongdiResult
            file = open("output.txt", "w")
            for no in range(len(duongDi_main)):
                for j in range(len(duongDi_main[no][0])):
                    if j != len(duongDi_main[no][0]) - 1:
                        file.write(str(duongDi_main[no][0][j][0]) + " ")
                    else:
                        file.write(str(duongDi_main[no][0][j][0]))
                if no != len(duongDi_main) - 1:
                    file.write("\n")
            file.close()
        else:
            if min_main > minResult:
                min_main = minResult
                duongDi_main = duongdiResult
                file = open("output.txt", "w")
                for no in range(len(duongDi_main)):
                    for j in range(len(duongDi_main[no][0])):
                        if j != len(duongDi_main[no][0]) - 1:
                            file.write(str(duongDi_main[no][0][j][0]) + " ")
                        else:
                            file.write(str(duongDi_main[no][0][j][0]))
                    if no != len(duongDi_main) - 1:
                        file.write("\n")
                file.close()
        count_main += 10
        time_end = time.time()

    #write output
    file = open("output.txt", "w")
    for no in range(len(duongDi_main)):
        for j in range(len(duongDi_main[no][0])):
            if j != len(duongDi_main[no][0]) - 1:
                file.write(str(duongDi_main[no][0][j][0]) + " ")
            else:
                file.write(str(duongDi_main[no][0][j][0]))
        if no != len(duongDi_main) - 1:
            file.write("\n")
    return


assign('input.txt', 'output.txt')
print("The result is in output.txt")