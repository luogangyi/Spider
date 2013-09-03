# -*- coding: gb2312 -*-
def getGBKCode(gbkFile='GBK1.1.txt',s=''):
    #gbkFile�ֵ��ļ� ��3755������
    #sΪҪת���ĺ��֣�����Ϊgb2312���룬����IDLE����ĺ��ֱ���

    #�����ֵ�
    with open(gbkFile) as f:
        gbk=f.read().split()

    #����A1-FE����������
    t=['A1']
    while True:
        if t[-1]=='FE':
            break
        if (ord(t[-1][1])>=48 and ord(t[-1][1])<57) or (ord(t[-1][1])>=65 and ord(t[-1][1])<70):
            t.append(t[-1][0]+chr(ord(t[-1][1])+1))
            continue
        if ord(t[-1][1])>=57 and ord(t[-1][1])<65:
            t.append(t[-1][0]+chr(65))
            continue
        if ord(t[-1][1])>=70:
            t.append(chr(ord(t[-1][0])+1)+chr(48))
            continue
    #��������ÿ������
    l=list()
    for st in s.decode('gb2312'):
        st=st.encode('utf-8')
        i=gbk.index(st)+1
    #С�ڱ����B0��ʼ����ȡ���ֵ�С�ڱ���
    t1='%'+t[t.index('B0'):][i/94]
    #�����ڽڵ��е�������
    i=i-(i/94)*94
    t2='%'+t[i-1]
    l.append(t1+t2)
    #����ÿո�ָ����
    return ' '.join(l) 
