哈希
======

Hash 的定义
-------------

　　Hash，就是把任意长度的输入，通过哈希算法，变换成固定长度的输出，该输出就是哈希值。不同的输入可能会哈希成相同的输出，所以不可能从哈希值来唯一的确定输入值。

　　链式存储

　　原理图如下，其实就是将发生有冲突的元素放到同一位置，然后通过“指针“来串联起来

   .. image:: images/hash.png

.. code:: python

    class HashTable:
        def __init__(self):
            self.size = 11
            self.slots = [list()] * self.size
            self.data = [list()] * self.size

        def hash_function(self, key, size):
            return key % size

        def __getitem__(self, key):
            return self.get(key)

        def __setitem__(self, key, data):
            self.put(key, data)

        def put(self, key, data):
            hash_value = self.hash_function(key,len(self.slots))
            self.slots[hash_value].append(key)
            self.data[hash_value].append(data)

        def get(self, key):
            hash_value = self.hash_function(key, len(self.slots))
            for i, ikey in enumerate(self.slots[hash_value]):
                if ikey == key:
                    return self.data[hash_value][i]

