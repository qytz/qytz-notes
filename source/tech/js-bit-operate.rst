JavaScript 的移位运算与 IP 地址处理
=====================================

JS 左移运算符号位的问题
-------------------------
最近在做项目时有一个需求，将用户输入的 *地址 / 掩码* 对解析出来，并将数字掩码转换成点分的格式。

想到在 C 代码里面应该还算容易实现，通过最大 32 位整数位移就可完成，但是在 JavaScript 中如何实现还是很不清楚的。

因为考虑到 JavaScript 是弱类型的语言，首先就会遇到数字和字符串的转换等问题，接着还有按位操作的问题也不知道在 JavaScript 中如何实现。
然后开始查询资料尝试解决这些问题。数字和字符串类型的转换是不需要的，写代码尝试了下应该 JavaScript 自动做了类型转换。

首先想到的思路是根据最大 32 位整数位移获取掩码对应的整数值，然后将结果转换成点分格式的字符串。在网上找到了如下的代码。

.. code-block:: javascript

    function ip2long(ip) {
        var ipl=0;
        ip.split('.').forEach(function( octet ) {
            ipl<<=8;
            ipl+=parseInt(octet);
        });
        return(ipl >>>0);
    }

    function long2ip (ipl) {
        return ( (ipl>>>24) +'.' +
            (ipl>>16 & 255) +'.' +
            (ipl>>8 & 255) +'.' +
            (ipl & 255) );
    }

有了这两个方法就可以将计算得到的掩码整数值转换成点分格式了。
但是在做位运算的时候发现了一个坑，在一边查资料一边尝试实现的第一个版本中，掩码为 0 和掩码为 32 产生的结果一样，都是 255.255.255.255。

.. note
    JavaScript 的左移运算保留数字的符号位。例如，如果把 -2 左移 5 位，得到的是 -64，而不是 64。符号仍然存储在第 32 位中。 即使输出二进制字符串形式的负数，显示的也是负号形式（例如，-2 将显示 -10。）

看来此方案不可行，接着查资料发现了一个新的思路，根据掩码生成四个小于等于 255 的值，将这四个值拼成点分格式。这样实现避免了对符号位的操作，甚好。

.. code-block:: javascript

    function createNetmaskAddr(bitCount) {
      var mask=[];
      for(i=0;i<4;i++) {
        var n = Math.min(bitCount, 8);
        mask.push(256 - Math.pow(2, 8-n));
        bitCount -= n;
      }
      return mask.join('.');
    }

参考资料
----------
* `Unsigned Integer in Javascript <http://stackoverflow.com/questions/1908492/unsigned-integer-in-javascript>`_
* `ECMAScript 位运算符 <http://www.w3school.com.cn/js/pro_js_operators_bitwise.asp>`_
* `CIDR to netmask converion in javascript <http://stackoverflow.com/questions/21903482/cidr-to-netmask-converion-in-javascript>`_
