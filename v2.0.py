# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:28:18 2022

@author: DELL
"""

# 求解数独
# copyright 物理学院 2100011461 陈贝宁

# v1.0 debug on Thur Mar 10 13:44 2022
# 需要回退mark，否则会造成老鼠屎坏粥

# success on Thur Mar 10 13:55 2022

# v1.1 join time on Thur Mar 10 15:46 2022

# v2.0 join find_must on Wed Mar 16 14:54 2022

import time

def readin():
    # 读入原始数据
    # 分行读入，以空格为界，0表示无数字
    # 返回9*9列表puzzle
    puzzle = []
    for i in range(9):
        p = [int(x) for x in input().split()]
        puzzle.append(p)
        
    return puzzle

def possible(i,j,puzzle,mark):
    # 对于给定数据表，找出（i，j）可能的数字
    # （i，j）位于第（m，n）个宫内
    m = i//3 ; n = j//3
    s = set()
    # mark表的使用
    for x in mark[i][j]:
        s.add(x)
    # 宫内
    for pi in range(3*m,3*m+3):
        for pj in range(3*n,3*n+3):
            s.add(puzzle[pi][pj])
    # 行内
    for pj in range(9):
        s.add(puzzle[i][pj])
    # 列内
    for pi in range(9):
        s.add(puzzle[pi][j])
    # 挨个排除
    p = [x for x in range(10)]
    for x in s:
        p.remove(x)
    return p

def get_numtable(puzzle,mark):
    # 获得一张记录可能数字的表
    numtable = [[[]for _ in range(9)]for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                numtable[i][j] = possible(i, j, puzzle, mark)
    return numtable

def find_least(puzzle,numtable):
    # 寻找给定数据表中可能数字最少的一格
    mini = 9 ; p = None
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0 and len(numtable[i][j]) < mini:
                mini = len(numtable[i][j])
                p = [i,j]
    return p

def find_must(numtable):
    # 寻找必须填的数字
    l = [None] ; pk = None
    for k in range(1,10):
        # 宫内
        for m in range(3):
            for n in range(3):
                # 第（m，n）宫
                f = True
                for a in range(9):
                    i = a//3 + 3*m ; j = a%3 + 3*n
                    if k in numtable[i][j]:
                        # 找到了
                        if f:
                            # 只有一个
                            pk = (i,j,k) ; f = False
                        else:
                            # 不止一个
                            pk = None          
                if pk not in l:
                    l.append(pk)
        # 行内
        for i in range(9):
            # 第i行
            f = True
            for j in range(9):
                if k in numtable[i][j]:
                    # 找到了
                    if f:
                        # 只有一个
                        pk = (i,j,k) ; f = False
                    else:
                        # 不止一个
                        pk = None          
            if pk not in l:
                l.append(pk)
        # 列内
        for j in range(9):
            # 第j列
            f = True
            for i in range(9):
                if k in numtable[i][j]:
                    # 找到了
                    if f:
                        # 只有一个
                        pk = (i,j,k) ; f = False
                    else:
                        # 不止一个
                        pk = None          
            if pk not in l:
                l.append(pk)
    return l[1:]

def print_puzzle(puzzle):
    # 打印
    print('='*9 + ' 答案 ' + '='*9)
    for i in range(9):
        print(' '.join([str(x) for x in puzzle[i]]))

def main():
    # 主程序
    # 用来记录操作的栈，元素（i，j，填入的数字k）
    stack = []
    # 用来记录被排除的数字
    mark = [[[0]for _ in range(9)]for _ in range(9)]
    # 读入数独
    puzzle = readin()
    # 计时模组
    s = time.time()
    
    # 先找必须填的
    numtable = get_numtable(puzzle, mark)
    l = find_must(numtable)
    print(l)
    while l:
        p = l.pop()
        # 存在，填入，进栈（其实无所谓）
        i,j,k = p
        puzzle[i][j] = k
        stack.append(p)
    print_puzzle(puzzle)
    # 再暴力列举
    while True:
        numtable = get_numtable(puzzle, mark)
        p = find_least(puzzle, numtable)
        if p:
            # 还没填完
            i,j = p
            if numtable[i][j]:
                # 存在可用数字，填入，进栈
                k = numtable[i][j][0]
                mark[i][j].append(k) # 标记填过的数字
                puzzle[i][j] = k
                stack.append((i,j,k))
            else:
                # 走入歧途，退栈
                mark[i][j] = [0] # 回退mark
                i,j,k = stack.pop()
                puzzle[i][j] = 0
        else:
            # 填完了，打印
            print_puzzle(puzzle)
            break
    
    e = time.time()
    print('用时：' + str(e-s) + '秒')

if __name__ == '__main__':
    main()
