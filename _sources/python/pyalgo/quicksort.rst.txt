快排
====
通过一趟排序将要排序的数据分割成独立的两部分，其中一部分的所有数据都比另外一部分的所有数据都要小，然后再按此方法对这两部分数据分别进行快速排序，整个排序过程可以递归进行，以此达到整个数据变成有序序列。

.. code:: python

    #方法1
    def quickSort(arr):
        less = []
        pivotList = []
        more = []
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]      #将第一个值做为基准
            for i in arr:
                if i < pivot:
                    less.append(i)
                elif i > pivot:
                    more.append(i)
                else:
                    pivotList.append(i)

            less = quickSort(less)      #得到第一轮分组之后，继续将分组进行下去。
            more = quickSort(more)

            return less + pivotList + more

    #方法2
    # 分为<, >, = 三种情况，如果分为两种情况的话函数调用次数会增加许多，以后几个好像都有相似的问题
    # 如果测试1000个100以内的整数，如果分为<, >=两种情况共调用函数1801次，分为<, >, = 三种情况，共调用函数201次
    def qsort(L):
        return (qsort([y for y in L[1:] if y <  L[0]]) + L[:1] + [y for y in L[1:] if y == L[0] + qsort([y for y in L[1:] if y > L[0]])) if len(L) > 1 else L

    #方法3
    #基本思想同上，只是写法上又有所变化
    def qsort(list):
        if not list:
            return []
        else:
            pivot = list[0]
            less = [x for x in list     if x <  pivot]
            more = [x for x in list[1:] if x >= pivot]
            return qsort(less) + [pivot] + qsort(more)

    #方法4
    from random import choice
    def qSort(a):
        if len(a) <= 1:
            return a
        else:
            q = choice(a)       #基准的选择不同于前，是从数组中任意选择一个值做为基准
            return qSort([elem for elem in a if elem < q]) + [q] * a.count(q) + qSort([elem for elem in a if elem > q])


    #方法5
    #这个最狠了，一句话搞定快速排序，瞠目结舌吧。
    qs = lambda xs : ( (len(xs) <= 1 and [xs]) or [ qs( [x for x in xs[1:] if x < xs[0]] ) + [xs[0]] + qs( [x for x in xs[1:] if x >= xs[0]] ) ] )[0]

