#!/usr/bin/python3
#author:jisenquan
import operator
import copy

'''
设置属性及其值
'''
class Attribute(object):
    def __init__(self,attribute):
        self.attribute = attribute
        self.attributeNum = len(attribute)
        self.attributeValue = {}
        #for i in attribute:
        #    self.attributeValue[i] = []
    '''
    添加属性的值
    '''
    def addValue(self,attr,value):
        self.attributeValue[attr] = value

'''
定义候选消除算法类
'''
class Candidate(object):
    '''
    输入测试数据，属性，并初始化S,S0,G0,G
    '''
    def __init__(self,testNum,testInstance,attrInit):
        self.testNum = testNum
        self.attributeValue = attrInit.attributeValue
        self.attribute = attInit.attribute
        self.attributeNum = attrInit.attributeNum
        self.S0 = []
        for i in range(self.attributeNum):
            self.S0.append('0')
        self.S = []
        self.S.append(self.S0)
        self.G0 = []
        for i in range(self.attributeNum):
            self.G0.append('?')
        self.G = []
        self.G.append(self.G0)
        self.testInstance = testInstance

    '''
    候选消除算法实现
    '''
    def runAlgorithm(self):
        for i in range(self.testNum):
            if self.testInstance[i][-1] == 'Yes':
                self.removeInconsistentG(i)
                S_New = []
                for s in self.S:
                    #print('s',s)
                    if not self.consistant(s,i):
                        self.S.remove(s)
                        S_Temp = self.generalizeAllInconsistant_s(s, i)
                        S_Temp2 = self.getGeneral(S_Temp)
                        S_New = self.removemoregeneral(S_Temp2)
                self.S = S_New
            else:
                self.removeInconsistantS(i)
                G_new = []
                for g in self.G:
                    if self.consistant(g,i):
                        self.G.remove(g)
                        G_Temp = self.specializeInconstant_g(g,i)
                        #print('G_temp',G_Temp)
                        G_Temp2 = self.getspeciclize(G_Temp)
                        #print('G_temp2',G_Temp2)
                        G_Temp3 = self.removemorespecific(G_Temp2)
                        #print(G_Temp3)
                        G_new += G_Temp3
                self.G = copy.deepcopy(G_new)
    '''
    从G中移除所有与d不一致的假设
    '''
    def removeInconsistentG(self,InstanceIndex):
        G_Temp = copy.deepcopy(self.G)
        #print(id(G_Temp))
        #print(id(self.G))
        for g in self.G:
            g_temp = copy.deepcopy(g)
            for attr in range(self.attributeNum):
                if self.testInstance[InstanceIndex][attr] != g[attr] and g[attr] != '?':
                    #print('G:',self.G)
                    #print('jiG',G_Temp)
                    #print('ji',g_temp)
                    break
                    G_Temp.remove(g_temp)

        self.G = copy.deepcopy(G_Temp)

    '''
    判断d与s是否一致
    '''
    def consistant(self,s,InstanceIndex):
        for attr in range(self.attributeNum):
            if s[attr] != self.testInstance[InstanceIndex][attr] and s[attr] != '?':
                return False

        return True
    '''
    将s更特殊化
    '''
    def generalizeAllInconsistant_s(self, s, InstanceIndex):
        S_Temp = copy.deepcopy(s)
        #print('Temp',S_Temp)
        for attr in range(self.attributeNum):
            if S_Temp[attr] == '0':
                S_Temp[attr] = self.testInstance[InstanceIndex][attr]
            elif not S_Temp[attr] == self.testInstance[InstanceIndex][attr]:
                S_Temp[attr] = '?'
        S_Temp2 = []
        S_Temp2.append(S_Temp)
        return S_Temp2
    '''
    判断G的某个成员是否比s更一般
    '''
    def getGeneral(self,S_Temp):
        S_Temp2 = []
        for s in S_Temp:
            flag = False
            for g in self.G:
                '''
                for attr in range(self.attributeNum):
                    if s[attr] == '0':
                        flag = True
                        break
                    if s[attr] != '?' and g[attr] == '?':
                        flag = True
                        break'''
                flag = self.more_general(g,s)
                if flag:
                    S_Temp2.append(s)
                    break
        if S_Temp2 == []:
            self.G = []
        return S_Temp2
    '''
    移除与d不一致的s
    '''
    def removeInconsistantS(self,InstanceIndex):
        for s in self.S:
            if operator.eq(s,self.testInstance[InstanceIndex][:-1]):
                self.S.remove(s)
    '''
    将g一般化
    
    '''
    def specializeInconstant_g(self,g,InstanceIndex):
        G_Temp = []

        for index,attr in enumerate(self.attribute):
            if g[index] == '?':
                for value in self.attributeValue[attr]:
                    #print('jisenquan')
                    if value != self.testInstance[InstanceIndex][index]:
                        gtemp = copy.deepcopy(g)
                        gtemp[index] = value
                        #print('gtemp:',gtemp)
                        G_Temp.append(gtemp)
                        gtemp = []
        return G_Temp
    '''
    检验h是否比s更一般
    '''
    def getspeciclize(self,G_Temp):
        G_Temp2 = []
        for g in G_Temp:
            for s in self.S:
                if self.more_general(s,g) or s == self.S0:
                    G_Temp2.append(g)
        if G_Temp2 == []:
            self.S = []
        return G_Temp2
    '''
    移除更一般的假设
    '''
    def removemoregeneral(self, S_Temp):
        #print('Stemp',S_Temp)
        S_new = copy.deepcopy((S_Temp))
        for old in S_Temp:
            for new in S_new:
                if old != new and self.more_general(new, old):
                    S_new.remove(new)
        return S_new
    '''
    移除更特殊的假设
    '''
    def removemorespecific(self, G_Temp2):
        G_new = G_Temp2[:]
        for old in G_Temp2:
            for new in G_new:
                if old != new and self.more_specific(new, old):
                    G_new.remove[new]
        return G_new
    '''
    获得更特殊的假设
    '''
    def more_specific(self, hyp1, hyp2):
        return self.more_general(hyp2, hyp1)
    '''
    获得更一般的假设
    '''
    def more_general(self, hyp1, hyp2):
        hyp = zip(hyp1, hyp2)
        for i, j in hyp:
            if i == '?':
                continue
            elif j == '?':
                if i != '?':
                    return False
            elif i != j:
                return False
            else:
                continue
        return True

    '''
    输出得到的边界
    '''
    def show(self):
        #for s in self.S:
        print('S:',self.S)
        #for g in self.G:
        print('G:',self.G)

'''
主函数
'''
if __name__ == '__main__':

    attribute = ['outlook','temperature','humidity','wind']

    attInit = Attribute(attribute)
    #print(attInit.attribute,attInit.attributeNum)
    attInit.addValue('outlook',['sunny','overcast','rain'])
    attInit.addValue('temperature',['hot','mild','cool'])
    attInit.addValue('humidity',['high','normal'])
    attInit.addValue('wind',['week','strong'])
    #print(attInit.attributeValue)
    testInstance = [['sunny','hot','high','weak','No'],
                    ['sunny','hot','high','strong','No'],
                    ['overcast','hot','high','weak','Yes'],
                    ['rain','mild','high','weak','Yes'],
                    ['rain','cool','normal','weak','Yes'],
                    ['overcast','cool','normal','strong','Yes'],
                    ['sunny','mild','high','weak','No'],
                    ['sunny','mild','high','weak','Yes'],
                    ['rain','mild','normal','weak','Yes'],
                    ['sunny','mild','normal','strong','Yes'],
                    ['overcast','mild','high','strong','Yes'],
                    ['overcast','Hot','Normal','Weak','Yes'],
                    ['rain','mild','high','strong','No']]
    test = Candidate(4,testInstance,attInit)
    test.runAlgorithm()
    test.show()