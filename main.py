import numpy as np
from itertools import product


# Вспомог. ф-ия: формирование матрицы Х для H и G
def matX(r):
    U = []
    for it in product('01', repeat=r):  # все двоичные комбинации длины r
        if it.count('1') >= 2:  # оставляем те, где количество единиц >=2
            U.insert(0, it)
        # print(U)
    return U

# Формирование проверочной матрицы
def matH(n, r):
    I = np.eye(r, dtype=int)  # единичная матрица размера r
    # print(I)
    X = matX(r)  # матрица X
    # print(X)
    H = (np.concatenate((X, I), axis=0))  # H = (X)
    #    (I)
    H = H.astype('int32')
    return H


# Формирование порождающей матрицы
def matG(n, r):
    I = np.eye(n - r, dtype=int)  # единичная матрица n-r
    X = matX(r)  # Матрица X
    # print(X)
    G = (np.concatenate((I, X), axis=1))  # G=(I|X)
    G = G.astype('int32')
    return G

#ормирование таблицы синдромов (как для КХ. так для и РКХ)
def Syndromes(n, H):
    I = np.mat(np.eye(n, dtype=int))
    # print(I)
    syndromes = (I @ H) % 2
    return syndromes

# Формирование проверочной матрицы РКХ
def matHR(H):
    H_c = H.copy()
    n =  len(H_c[0, :])
    ZeroStr = np.zeros((n), dtype=int)
    HH = np.vstack([H_c, ZeroStr])#добавляем в конец матрицы нулевую строку
    m = len(HH[:, 0])
    OnesColumn = np.ones((m, 1), dtype=int)#добавляем столбец из 1
    HH = np.c_[HH, OnesColumn]
    return HH

# Формирование порождающей матрицы РКХ
def matGR(G):
    G_c = G.copy()
    m = len(G_c[:, 0])
    ZeroStr = np.zeros((m), dtype=int)
    GG = np.c_[G_c, ZeroStr] #добавляем к матрице G стоблец из нуле
    m = len(GG[:, 0])
    n = len(GG[0, :])
    sum = 0#для подсчета веса
    for i in range(m):
        for j in range(n-1):
            if GG[i][j]==1:
                sum+=1#считаем вес строки без учета добавленного столбца
            j+=1
        if sum %2!=0:#вес нечетный - меняем добавленный эл-т строки на 1
            GG[i][n-1]=1
            sum=0
        i+=1
    return GG

# Задаем r в диапазоне[2, 4]
while True:
    r = int(input("Введите r от 2 до 4: "))
    if not 2 <= (r) <= 4:
        print("Попробуйте снова")
    else:
        print("r =", r)
        break

n = pow(2, r) - 1  # расчет n
print("n=", n)
k = pow(2, r) - r - 1  # расчет k
print("k=", k)
H = matH(n, r)
print("H\n", H)
G = matG(n, r)
print("G\n", G)

syndromes = Syndromes(n,H)
print("syndromes=\n", syndromes)#вывод таблицы синдромов

mas = []
print("Введите", k, "символов")
mas = [int(input()) for i in range(k)]#ввод сообщения
print("Исходное сообщение:", mas)
cmas = (mas @ G) % 2
print("Закодированное сообщение", cmas)
ercmas=cmas
Ishod = cmas.copy()
#кол-во ошибок от 1 до 3
while True:
    count_er = int(input("Количество ошибок?: "))
    if not 1 <= (count_er) <= 3:
        print("Попробуйте снова")
    else:
        print(count_er)
        break
mas_er=[]
z=0
#последовательно вносим ошибки
while z < count_er:
    i = int(input("В какой бит внести ошибку?: "))
    if not 0 <= (i) < n: #не выходим за границы сообщения
        print("Число не в диапазоне, попробуйте снова")
        i = int(input("В какой бит внести ошибку?: "))
    elif i in mas_er:
        print("Число ранее было задано,попробуйте снова")#е меняем один и тот же бит несколько раз
        i = int(input("В какой бит внести ошибку?: "))
    else:
        print("i =", i)
        mas_er.append(i)#запоминаем номер бита для проверки
        ercmas[i] = not ercmas[i]#еняем бит
        print("Cлово с ошибкой в бите",i,":", ercmas)
    z+=1

if z ==1:
    print("Сообщение с внесённой ошибкой:", ercmas)
else:
    print("Сообщение с внесёнными ошибками:", ercmas)
syn1 = (ercmas@H)%2
print("синдром = ", syn1)
zero = np.zeros((r), dtype = int)
correct = ercmas.copy()
if (syn1==zero).all() and z==3:
    print("Ничего не обнаружено!\nКоличество ошибок: ", z, "\nЗакодированное сообщение: ", Ishod,"\nСлово с ошибками: ", ercmas)
else:
    b = 0
    for j in range(n):
        s=np.ravel(syndromes[j])
        if np.array_equal(syn1,s):
            b=j
            break
    print(b)
    correct[b] = not correct[b]
    print("Количество ошибок: ", z, "\nЗакодированное сообщение: ", Ishod,"\nСлово с ошибками: ", ercmas, "\nИсправленное слово: ",correct)

######### РАСШИРЕННЫЙ КОД ХЭММИНГА ####################

print("РАСШИРЕННЫЙ КОД ХЭММИНГА")
n2 = pow(2, r)  # расчет n
print("n=", n2)
k2 = pow(2, r) - r - 1  # расчет k
print("k=", k2)
HH = matHR(H)
print ("H\n",HH)
GG = matGR(G)
print ("G\n",GG)
syndromes2 = Syndromes(n2,HH)
print("syndromes2=\n", syndromes2)#вывод таблицы синдромов

mas2 = []
print("Введите", k2, "символов")
mas2 = [int(input()) for i in range(k2)]#ввод сообщения
print("Исходное сообщение:", mas2)
cmas2 = (mas2 @ GG) % 2
print("Закодированное сообщение", cmas2)
ercmas2=cmas2
Ishod2 = cmas2.copy()
#кол-во ошибок от 1 до 4
while True:
    count_er2 = int(input("Количество ошибок?: "))
    if not 1 <= (count_er2) <= 4:
        print("Попробуйте снова")
    else:
        print(count_er2)
        break
mas_er2=[]
z=0
#последовательно вносим ошибки
while z < count_er2:
    i = int(input("В какой бит внести ошибку?: "))
    if not 0 <= (i) < n2: #не выходим за границы сообщения
        print("Число не в диапазоне, попробуйте снова")
        i = int(input("В какой бит внести ошибку?: "))
    elif i in mas_er2:
        print("Число ранее было задано,попробуйте снова")#не меняем один и тот же бит несколько раз
        i = int(input("В какой бит внести ошибку?: "))
    else:
        print("i =", i)
        mas_er2.append(i)#запоминаем номер бита для проверки
        ercmas2[i] = not ercmas2[i]#меняем бит
        print("Cлово с ошибкой в бите",i,":", ercmas2)
    z+=1

if z ==1:
    print("Сообщение с внесённой ошибкой:", ercmas2)
else:
    print("Сообщение с внесёнными ошибками:", ercmas2)
syn2 = (ercmas2@HH)%2
print("синдром = ", syn2)
zero2 = np.zeros((r+1), dtype = int)
correct2 = ercmas2.copy()
a = (np.where((syndromes2==syn2).all(axis=1))[0])#сть ли синдром в таблице H
s = np.array_equal(syn2,zero2)#не нулевой ли синдром
#print(s)
if a.size==0 and s == False:#синдрома нет в таблице и он не нулевой
    print("Синдром не найден в таблице H, ошибки не могут быть исправлены"
          "\nКоличество ошибок: ", z, "\nЗакодированное сообщение: ", Ishod2,"\nСлово с ошибками: ", ercmas2)
elif a.size==0 and s == True:#синдрома нет в таблице и он нулевой
    print("Ошибок не обнаружено!\nКоличество ошибок: ", z, "\nЗакодированное сообщение: ", Ishod2,"\nСлово с ошибками: ", ercmas2)
else:
    b = 0
    for j in range(n2):
        s=np.ravel(syndromes2[j])
        if np.array_equal(syn2,s):
            b=j
            break
    print(b)
    correct2[b] = not correct2[b]
    print("Количество ошибок: ", z, "\nЗакодированное сообщение: ", Ishod2,"\nСлово с ошибками: ", ercmas2, "\nИсправленное слово: ",correct2)