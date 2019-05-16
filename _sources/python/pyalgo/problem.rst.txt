算法问题
================
水仙花数
-----------
一个N位的十进制正整数，如果它的每个位上的数字的N次方的和等于这个数本身，则称其为水仙花数。

例如：

  当N=3时，153就满足条件，因为 1^3 + 5^3 + 3^3 = 153，这样的数字也被称为水仙花数（其中，“^”表示乘方，5^3表示5的3次方，也就是立方）。

  当N=4时，1634满足条件，因为 1^4 + 6^4 + 3^4 + 4^4 = 1634。

  当N=5时，92727满足条件。

实际上，对N的每个取值，可能有多个数字满足条件。

.. code:: python

    # 直接循环遍历所有N位的数进行判断，效率低
    def get_flower(n):
        start, end = pow(10, n-1), pow(10, n) - 1
        for i in range(start, end):
            index1 = i // 100;
            index2 = (i % 100) // 10;
            index3 = i % 10;
            if pow(index1, 3) + pow(index2, 3) + pow(index3, 3) == i:
                print(i)

    # 另外一个思路，找出N位数所包含所有数字的组合，遍历这些组合，检查所有数字的N次方之和的数字组成是否匹配这些数组。
    # N位数所包含的数字组合是数学组合问题，其组合数目大大小于N位数的数目，因此算法效率高很多
    # https://oeis.org/A005188
    from itertools import combinations_with_replacement
    A005188_list = []
    for k in range(1, 10):
        a = [i**k for i in range(10)]
        for b in combinations_with_replacement(range(10), k):
            x = sum(map(lambda y:a[y], b))
            if x > 0 and tuple(int(d) for d in sorted(str(x))) == b:
                A005188_list.append(x)
    A005188_list = sorted(A005188_list) # Chai Wah Wu, Aug 25 2015

    # 优化效率后的方法，少做了很多次循环
    # 找出N个数字的的N次方之和落在N位数范围内的所有组合
    # 遍历这些组合判断组合组成的数字能否符合水仙花数的规则
    # （即不管这个组合中数字是在哪一位，只需判断N次方和数字的组成与该组合的数字组成一样就可以）
    def get_flower(n):
        D_pow = [pow(i,n) for i in range(0,10)]
        V_min = pow(10,n-1)
        # V_max=sum((9*pow(10,x) for x in range(0,n)))
        V_max = pow(10, n) - 1
        T_count = 0
        print(D_pow, V_max, V_min)
        nums = [1] + [0] * (n-1)
        print('Start:', nums)
        tests = []

        idx = n - 1
        tmp_l = [0]*10
        while True:
            nums[idx] += 1
            if nums[idx] < 10:
                j = idx+1
                while j < n:
                    nums[j] = nums[idx] # reset
                    j += 1
                v = sum((D_pow[x] for x in nums))
                if v <= V_max and v >= V_min:
                    T_count+=1
                    # test if is flower
                    # print('do test:', ''.join(map(str,nums)))
                    N = n
                    tmp_l = [0]*10
                    for k in nums:
                        tmp_l[k] += 1
                    while N > 0:
                        p = v % 10
                        if tmp_l[p] > 0:
                            tmp_l[p] -= 1
                            N -= 1
                        else:
                            break
                        v //= 10
                    if N == 0:
                        print('hit', sum((D_pow[x] for x in nums)))
                idx = n-1
            elif idx == 0:
                print('done')
                break
            else:
                idx -= 1
        print('t_count', T_count)
        # print('tests: ', str(tests))


终极解决方法是，十进制的水仙花数总共有89个::

    # https://zh.wikipedia.org/wiki/%E6%B0%B4%E4%BB%99%E8%8A%B1%E6%95%B0
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    153
    370
    371
    407
    1634
    8208
    9474
    54748
    92727
    93084
    548834
    1741725
    4210818
    9800817
    9926315
    24678050
    24678051
    88593477
    146511208
    472335975
    534494836
    912985153
    4679307774
    32164049650
    32164049651
    40028394225
    42678290603
    44708635679
    49388550606
    82693916578
    94204591914
    28116440335967
    4338281769391370
    4338281769391371
    21897142587612075
    35641594208964132
    35875699062250035
    1517841543307505039
    3289582984443187032
    4498128791164624869
    4929273885928088826
    63105425988599693916
    128468643043731391252
    449177399146038697307
    21887696841122916288858
    27879694893054074471405
    27907865009977052567814
    28361281321319229463398
    35452590104031691935943
    174088005938065293023722
    188451485447897896036875
    239313664430041569350093
    1550475334214501539088894
    1553242162893771850669378
    3706907995955475988644380
    3706907995955475988644381
    4422095118095899619457938
    121204998563613372405438066
    121270696006801314328439376
    128851796696487777842012787
    174650464499531377631639254
    177265453171792792366489765
    14607640612971980372614873089
    19008174136254279995012734740
    19008174136254279995012734741
    23866716435523975980390369295
    1145037275765491025924292050346
    1927890457142960697580636236639
    2309092682616190307509695338915
    17333509997782249308725103962772
    186709961001538790100634132976990
    186709961001538790100634132976991
    1122763285329372541592822900204593
    12639369517103790328947807201478392
    12679937780272278566303885594196922
    1219167219625434121569735803609966019
    12815792078366059955099770545296129367
    115132219018763992565095597973971522400
    115132219018763992565095597973971522401

我们把这些数存到数组，直接取出来就可以了。


回文算法
------------
回文（Palindrome），就是一个序列（如字符串）正着读反着读是一样的。

.. code:: python

    def isPlidromNonRecursive(inputStr):
        strLen = len(inputStr)
        currentStart = 0
        currentEnd = strLen - 1
        while currentStart <= currentEnd:
            if inputStr[currentStart] != inputStr[currentEnd]:
                return False
            else:
                currentStart += 1
                currentEnd -= 1
        return True

    def isPlidromRecursive(inputStr, start, end):
        if len(inputStr) <= 1:
            return True
        if start >= end:
            return True
        if inputStr[start] != inputStr[end]:
            return False
        else:
            return isPlidromRecursive(inputStr, start+1, end-1)
    isPlidromRecursive('abc', 0, len('abc')-1)

    # 复杂度O(n)的，不过是python内部用C语言实现的，猜测会比前2个方法快。
    def isPalindrome(s):
        return s == s[::-1]
