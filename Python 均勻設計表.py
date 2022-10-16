import numpy as np
import math
import itertools
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from sklearn.linear_model import LinearRegression

#普通註解
##普通註解
###測資範圍(必定有三個作間隔)，同號間的兩區域(手動輸入 / 測試資料)的程式碼擇一註解掉

def value(i, j, q):
    #按均勻表規則產生值
    
    ans = i* j% q
    
    if ans == 0:
        return q
    else:
        return ans

def tableprint(table, width, height):
    #一般輸出表
    
    w1 = len(str(width))
    h1 = len(str(height-1))
    
    if h1 >= 1:
        print(" "* (w1+ 1) + "* " + " "* h1, end='')
    else:
        print(" "* (w1+ 1) + "* ", end='')
        
#顯示一般行號
    for i in range(width):
        print(str(i+ 1) + " "*(w1+ 2 - len(str(i + 1))) , end='')
    print()
    
#顯示所實際餐與計算的行號
    '''
    for i in range(width):
        print(str(table[0][i]) + " "*(w1+ 2 - len(str(i + 1))) , end='')
    print()
    '''
    
    print("*"*int(width* 5))
    
    for i in range(height):
        print(str(i+ 1) + " "*(w1-len(str(i+ 1))+ 1) + "*" + " " * (w1 + 1), end='')
        for j in range(width):
            v = str(table[i][j])
            print(v + " "*(w1+ 2- len(v)), end='')
        print()
    
def tableprint_sq(table, width, height, square):
    #指定欄號(存於square)的輸出表
    
    w1 = len(str(width))
    h1 = len(str(height- 1))
    
    if h1 >= 1:
        print(" "*(w1+ 1) + "* " + " "* h1, end='')
    else:
        print(" "*(w1+ 1) + "* ", end='')
        
#顯示一般行號
    for i in range(width):
        print(str(square[i]) + " "*(w1+ 2- len(str(square[i]))), end='')
    print()
    
#顯示所實際餐與計算的行號
    '''
    for i in range(width):
        print(str(table[0][i]) + " "*(w1+ 2- len(str(i+ 1))) , end='')
    print()
    '''
    
    print("*"*int(width* 5))
    
    for i in range(height):
        print(str(i+1) + " "*(w1- len(str(i+ 1))+ 1) + "*" + " "*(w1+ 1), end='')
        for j in range(width):
            v = str(table[i][j])
            print(v + " "*(w1+ 2- len(v)), end='')
        print()
        
def gcd(m, n):
    #找出兩數最大公因數
    
    return m if n == 0 else gcd(n, m % n)
   
def table(n):
    #依試驗數 n 產生均勻表
    #表高(試驗數)
    
    colsum = 0
    colset = set()

    #表寬為偶數時，表的產生是試驗數+1去掉末行(反正本來就會被去掉)
    nAdjust = n
    
    if n%2 == 0:
        nAdjust +=1
    
    for i in range(1,nAdjust):
        if gcd(nAdjust, i) == 1:
            colsum+=1
            colset.add(i)
            
    
    tab = [[0]* colsum for i in range(n)]
    colsetList = list(colset)
    
    for i in range(n):
        for j in range(len(colset)):
            tab[i][j] = value(i+1, colsetList[j], nAdjust)

    #依序是表、表寬、表高
    tableprint(tab, colsum, n)
    print()
    print('最大水平數為 ' + str(colsum))
    print()

    return tab 
    
def CDproTwo(tab, n, s):   
    #求表的 CD 值，普通計算，未考慮 The Perils of Floating Point
    
    for i in range(n):
        for j in range(s):
            tab[i][j] = (2*tab[i][j]-1)/(2*n)   
    
    #pi是連乘
    #之後才是連加
    
    sum2 = 0
    sum4 = 0
    
    for i in range(n):
        sum1 = 1
        for j in range(s):
            sum1 *= (1 + 0.5* abs(tab[i][j]- 0.5) - 0.5* ((tab[i][j]- 0.5)**2))
        sum2 += sum1.real
        
            
    for i in range(n):
        for k in range(n):
            sum3 = 1
            for j in range(s):
                sum3 *= (1 + 0.5* abs(tab[i][j]- 0.5) + 0.5* abs(tab[k][j]- 0.5) - 0.5* abs(tab[i][j]- tab[k][j]))
            sum4 += sum3.real
                
    ans = ((13/12)** s - (2/n)* sum2.real + (1/(n** 2))* sum4.real)** 0.5

    #在未考慮 The Perils of Floating Point下，欲符合講義答案，僅能算到點後第14位
    return format(calChange(ans, 1, '*', 14), '.14f')

def deMul(num, degree, offset):
    #求次方的值
    
    if degree == 1:
        return num
    else:
        return calChange(deMul(num, degree-1, offset), num, '*', offset)

def deCDproTwo(tab, n, s):
    #求表的 CD 值，以 Decimal 計算，有考慮 The Perils of Floating Point
    
    #目前最大位數在 n = 5 時，可以算到點後 26 位
    # n = 13 時，可以到點後 6 位
    # n 越大，點後位數也要跟著縮小，不然會在函數 calChange() 發生問題(各種計算問題)
    offset = 6
    
    for i in range(n):
        for j in range(s):
            #tab[i][j] = (2*tab[i][j]-1)/(2*n)
            tab[i][j] = calChange(calChange(calChange(2, tab[i][j], '*', offset), 1, '-', offset), calChange(2, n, '*', offset), '/', offset)
    
    #pi是連乘
    #之後才是連加   
    sum2 = 0
    sum4 = 0
    
    for i in range(n):
        sum1 = 1
        for j in range(s):
            #sum1 *= (1 + 0.5* abs(tab[i][j]- 0.5) - 0.5* ((tab[i][j]- 0.5)**2))

            a = abs(calChange(tab[i][j], 0.5, '-', offset))
            ah = calChange(0.5, a, '*', offset)

            aa = calChange(a, a,'*', offset)
            aah = calChange(0.5, aa, '*', offset)

            sum1 = calChange(sum1, calChange(calChange(1, ah, '+', offset), aah, '-', offset), '*', offset)
            
        sum2 = calChange(sum2, sum1, '+', offset)
        
            
    for i in range(n):
        for k in range(n):
            sum3 = 1
            for j in range(s):
                #sum3 *= (1 + 0.5* abs(tab[i][j]- 0.5) + 0.5* abs(tab[k][j]- 0.5) - 0.5* abs(tab[i][j]- tab[k][j]))

                a = abs(calChange(tab[i][j], 0.5, '-', offset))
                abh = calChange(0.5, a, '*', offset)

                b = abs(calChange(tab[k][j], 0.5, '-', offset))
                bbh = calChange(0.5, b, '*', offset)

                c = abs(calChange(tab[i][j], tab[k][j], '-', offset))
                ch = calChange(0.5, c, '*', offset)

                sum3 = calChange(calChange(calChange(calChange(1, abh, '+', offset), bbh, '+', offset), ch, '-', offset), sum3, '*', offset)
                
            sum4 = calChange(sum4, sum3, '+', offset)
                
    #ans = ((13/12)** s - (2/n)* sum2.real + (1/(n** 2))* sum4.real)** 0.5

    p1 = deMul(calChange(13, 12, '/', offset), s, offset)
    
    p2 = calChange(2, n, '/', offset)
    p2m = calChange(p2, sum2, '*', offset)
    
    p3 = calChange(1, calChange(n, n, '*', offset), '/', offset)
    p3m = calChange(p3, sum4, '*', offset)

    ans = calChange(calChange(calChange(p1, p2m, '-', offset), p3m, '+', offset),1, 'sq', offset)

    lenth = '.' + str(offset) + 'f'
    
    return format(calChange(ans, 1, '*', offset), lenth)

def c(m, n):
    #求組合數
    
    if m-n == 1:
        return m
    elif m == n:
        return 1
    else:
        return math.factorial(m)/(math.factorial(n)* math.factorial(m-n))
    
def findUpperPrime(a):
    #求大於該數的質數
    
    while Primecheck(a) == False:
        a+=1
    return a
            
def Primecheck(a):
    #質數檢查
    
    r = int(a** 0.5)
    
    for i in range(2, r+1):
        if a % i == 0:
            return False
    return True

def catchTableColum(tab1, height, width, n, tab2):
    #提取表 1 特定欄 n 至表 2
    
    for i in range(height):
        tab2[i][width] = tab1[i][n]

def rowResult(number, many):
    #列出各欄的組合結果
    
    all = list(itertools.combinations(list(range(1, number+ 1)),many))
    
    for i in range(len(all)):
        all[i] = list(all[i])
    
    return all

def produceTables(result, tab, height, weight, pointSeq):
    #產生指定因素水平的均勻表，需指定序數

    print('指定組合: ', end='')
    print(result[pointSeq])
    print()
    
    tab2 = [[0]* weight for i in range(height)]
    
    for j in range(weight):
        catchTableColum(tab, height, j, result[pointSeq][j]-1, tab2)
        
    tableprint_sq(tab2, weight, height, result[pointSeq])
    
    return tab2

def produceUseTable(result, tab, height, width, Mintab, look = False, delta = False):
    #產生使用表
    
    tab2 = [[0]* width for i in range(height)]
    Minlines = []#儲存行號
    checklineCD = []#儲存CD值
    tabs = []#儲存陣列內容

    #print('result :' + str(result))
    for i in range(len(result)):#對於各個的組合結果
        tab3 = [[0]* width for item in range(height)]
        for j in range(width):#擷取出對應的表
            
            ##或許會問，為啥 tab3 不用複製的就好?
            ##因為不知為何，當時無論用何寫法(大概沒放綠乖乖中邪了吧...)
            ##都僅抄了一堆指標，經過 CDproTwo 計算後就變質了
            catchTableColum(tab, height, j, result[i][j]-1, tab2)
            #catchTableColum(tab, height, j, result[i][j]-1, tab3)
            
            ##用deepcopy()解決惹，感動~
            tab3 = deepcopy(tab2)        

        #求該表的CD值
        ##有兩種函數(CDproTwo() / deCDproTwo())可以選擇
        ##差別在是否有考慮 The Perils of Floating Point
        tab3CD = deCDproTwo(tab3, height, width)
 
        checklineCD.append(tab3CD)
        Minlines.append(deepcopy(tab2[0]))
        tabs.append(deepcopy(tab2))

    # CD 取最小
    MinCD = checklineCD.index(min(checklineCD))        
    Mintab.append(tabs[MinCD])
    
    w1 = len(str(width))

    #印出選取結果
    print(str(width) + " "*(w1-len(str(height))+1) + "#" + " "*(w1+1) + str(Minlines[MinCD]))

    if look == True:
        print()
        #顯示所有 CD 值
        for i in range(len(checklineCD)):
            print(str(i) + '  ' + str(Minlines[i]), end='')
            
            if delta == True:
                print('  CD: ' + str(checklineCD[i]), end='' )
                d = float(checklineCD[i]) - float(checklineCD[MinCD])
                print('  delta: ' + str(d))
            else:
                print('  CD: ' + str(checklineCD[i]))
        print()

    return Minlines[MinCD]

def calChange(number1, number2, op, offset):
    #將數字進行轉換
    
    #offset 最少為 1
    ##指定位數並非小數點後的位數，包含了小數點前的位數，待修正
    
    numberAfter1 = Decimal(str(number1))
    numberAfter2 = Decimal(str(number2))   

    if op == '+':
        return numberAfter1 + numberAfter2.quantize(Decimal('.'+ '0'* offset), ROUND_HALF_UP)
    elif op == '-':
        return numberAfter1 - numberAfter2.quantize(Decimal('.'+ '0'* offset), ROUND_HALF_UP)
    elif op == '*':
        return numberAfter1 * numberAfter2.quantize(Decimal('.'+ '0'* offset), ROUND_HALF_UP)
    elif op == '/':
        return numberAfter1 / numberAfter2.quantize(Decimal('.'+ '0'* offset), ROUND_HALF_UP)
    elif op == 'sq':
        if numberAfter1 < 0:
            print('error value = ' + str(numberAfter1))
            return numberAfter1
        else:
            return (numberAfter1.sqrt()).quantize(Decimal('.'+ '0'* offset), ROUND_HALF_UP)

def addcol(table, addlist):
    #延伸追加一欄

    tableh = len(table)
    
    print('\nAfterTable: ')
    print("="* int(tableh* 3) + '>')
    #需先轉換型態回 list 
    table = np.array(table).tolist()
    for i in range(tableh):
        table[i].append(addlist[i])

    #調整完再轉換型態回 array     
    table = np.array(table)
    print(table)
    
    return table

def testdata(tab, n, s):
    valueS = [1,5,1,15]
    valueE = [5.4,60,6.5,70]
    
    pointOffset = 2

    for i in range(s):
        ##是否預先將分割出來的值進行轉換處理(是為上，反之為下)
        #valueDelta = calChange(calChange(valueE, valueS, '-', pointOffset), (s- 1), '/', pointOffset)
        valueDelta = (valueE[i]- valueS[i])/ (n- 1)

        #print(valueDelta)
        #print()
        for j in range(n):
            if j == n-1:
                tab[i][j] = calChange(valueE[i], 1, '*', pointOffset)
            else:
                tab[i][j] = calChange(valueS[i], calChange(valueDelta, j, '*', pointOffset), '+', pointOffset)
    return tab 

def prodeceCaseTable(refTable, oriTable, n, s, offset):
    #試驗方案表
    
    oriTable = np.array(oriTable)
    casetable = deepcopy(oriTable)
    casetable = np.array(casetable, dtype = 'float')
    #print('\n case:')
    #print(casetable)

    for i in range(n):
        for j in range(s):
            casetable[i][j] = refTable[j][oriTable[i][j]-1]
    print()
    
    #print('case2:')

    lenth = '{0:0.' + str(offset) + 'f}'
    np.set_printoptions(formatter={'float': lambda x: lenth.format(x)})
    
    print('\nBeforeTable: ')
    print("="* int(n* 3) + '>')
    print(casetable)
    return casetable

#### main

#顯示該因素數最大水平的表
###1
n = int(input('試驗數/(高(上標)、因素/) n：'))
###1
'''
###測資測試用
n = 12
'''
###1
print("="*int(n*3) + str(1))

##禁宣告一整數當參數傳進函式裡取得內容的任意數值，會取不到值，本語言不允許傳值，但傳遞容器類的例外
Utable = table(n)
#最大水平數
Maxs = len(Utable[0])


#列出該表指定列數的組合表
useN = int(n/ 2) + 1
#預設因素數若為奇數，則會無條件捨去
print("最大因素個數為 " + str(int(useN)))
print()
print("使用表：")
print("="*int(n* 3))

#紀錄各水平最高CD的組合 firstCDLine 和表 firstCDtab
firstCDLine = []#首列行號
firstCDtab = []#對應該行號的均勻表

for i in range(2, useN + 1):
    #末端可添加參數 1 設為 True，以查看各組合的 CD值
    #再添加參數 2 設為 True，以查看各組合與最小組合的 CD 差距
    #取值時要記得把索引值-2
    firstCDLine.append(produceUseTable(rowResult(Maxs, i), Utable, n, i, firstCDtab))

print("="* int(n* 3) + str(2))


'''
for i in range(0, useN - 1):
    print(firstCDLine[i])
    print(firstCDtab[i])
'''
'''
if s < n:
    print("共有 " + str(int(c(n- 1, s))) + " 種組合")
else:
    print("共有 " + str(1) + " 種組合")
    
print("="*int(n*3) + str(3))
'''
###2
s = int(input('指定列數/(寬(下標)、水平/) s：'))
###2
'''
#測資測試用
s = 4
'''
###2
print("="* int(n* 3) + str(4))

#print(produceTables(rowResult(Maxs, s), Utable, n, s, 136))


#因素水平表產生
#要留意和平常看的均勻表行列顛倒
nstable = [[0]* n for i in range(s)]

#暫時先銜接測試用資料的函數
nstable = testdata(nstable, n, s)

###3
'''
#測試用指定位數
pointOffset = 2
pointTable = produceTables(rowResult(Maxs, s), Utable, n, s, 136)
Case = deepcopy(prodeceCaseTable(nstable, pointTable, n, s, pointOffset))
'''
###3
for i in range(s):
    valueS = float(input('輸入第' + str(i+ 1) + '個因素的範圍起始值：'))
    valueE = float(input('輸入第' + str(i+ 1) + '個因素的範圍結束值：'))
    pointOffset = int(input('輸入該因素的小數點後指定位數：'))

    ##是否預先將分割出來的值進行轉換處理(是為上行，反之為下行)
    #valueDelta = calChange(calChange(valueE, valueS, '-', pointOffset), (s- 1), '/', pointOffset)
    valueDelta = (valueE- valueS)/ (n- 1)

    #print(valueDelta)
    #print()
    for j in range(n):
        if j == n-1:
            nstable[i][j] = calChange(valueE, 1, '*', pointOffset)
        else:
            nstable[i][j] = calChange(valueS, calChange(valueDelta, j, '*', pointOffset), '+', pointOffset)
        print(str(nstable[i][j]) + "  ",end='')
    print()

Case = deepcopy(prodeceCaseTable(nstable, firstCDtab[s - 2], n, s, pointOffset))
###3
#print(Case)


#產生試驗方案表
print('\n試驗方案表: \n')

#併入欲額外添加的欄位(要作為回歸的 Y 值)
addline = []
###4
'''
#手動輸入測試用資料
testY1 = [2.20, 2.83, 6.20, 10.49, 4.20, 9.87, 10.22, 24.24, 9.88, 13.27, 12.43, 27.77]
addline = testY1
'''
###4
for i in range(n):
    Yvalue = float(input('輸入第' + str(i+ 1) + '次試驗的應變數：'))
    addline.append(Yvalue)
###4

#兩表合併(似乎可以不用)
#Case2 = addcol(Case, addline)


#回歸分析
print('\n回歸分析: ')
print("="*int(n*3) + str(5))

X = Case
Y = addline
reg = LinearRegression().fit(X, Y)

print('Coefficient of determination R^2 of the prediction: ' + str(reg.score(X, Y)))
print('Cofficients: ' + str(reg.coef_))
print('常數: ' + str(reg.intercept_))

#逐步回歸分析，本語言尚未有穩定的支援套件，僅有向前選擇和向後刪除，但皆不穩定
