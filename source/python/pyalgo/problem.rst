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
