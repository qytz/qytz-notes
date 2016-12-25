二分法
=======
二分搜索每次把搜索区域减少一半，时间复杂度为 O(logn) （n代表集合中元素的个数）
在计算机科学中，二分搜索（英语：binary search），也称折半搜索（英语：half-interval search）、对数搜索（英语：logarithmic search），是一种在有序数组中查找某一特定元素的搜索算法。搜索过程从数组的中间元素开始，如果中间元素正好是要查找的元素，则搜索过程结束；如果某一特定元素大于或者小于中间元素，则在数组大于或小于中间元素的那一半中查找，而且跟开始一样从中间元素开始比较。如果在某一步骤数组为空，则代表找不到。这种搜索算法每一次比较都使搜索范围缩小一半。

步骤如下：

    #. 确定该期间的中间位置K
    #. 将查找的值T与array[k]比较。若相等，查找成功返回此位置；否则确定新的查找区域，继续二分查找。

猜数游戏。

::

    def BinarySearch(array,t):
        low = 0
        height = len(array)-1
        while low < height:
            mid = (low+height)/2
            if array[mid] < t:
                low = mid + 1
            elif array[mid] > t:
                height = mid - 1
            else:
                return array[mid]
        return -1
