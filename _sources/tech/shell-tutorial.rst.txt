=========================
shell 脚本常用操作入门
=========================

shell 字符串操作
=================

判断读取字符串值

    ===============     =======================================================
    表达式               含义
    ===============     =======================================================
    ${var} 	            变量 var 的值，与 $var 相同
    ${var-DEFAULT} 	    如果 var 没有被声明，那么就以 $DEFAULT 作为其值 *
    ${var:-DEFAULT} 	如果 var 没有被声明，或者其值为空，那么就以 $DEFAULT 作为其值 *
    ${var=DEFAULT} 	    如果 var 没有被声明，那么就以 $DEFAULT 作为其值 *
    ${var:=DEFAULT} 	如果 var 没有被声明，或者其值为空，那么就以 $DEFAULT 作为其值 *
    ${var+OTHER} 	    如果 var 声明了，那么其值就是 $OTHER, 否则就为 null 字符串
    ${var:+OTHER}   	如果 var 被设置了，那么其值就是 $OTHER, 否则就为 null 字符串
    ${var?ERR_MSG} 	    如果 var 没被声明，那么就打印 $ERR_MSG *
    ${var:?ERR_MSG} 	如果 var 没被设置，那么就打印 $ERR_MSG *
    ${!varprefix*} 	    匹配之前所有以 varprefix 开头进行声明的变量
    ${!varprefix@}  	匹配之前所有以 varprefix 开头进行声明的变量
    ===============     =======================================================

字符串操作（长度，读取，替换）

    ================================   ==========================================================
    表达式                              含义
    ================================   ==========================================================
    ${#string}              	       $string 的长度
    ${string:position} 	               在 $string 中，从位置 $position 开始提取子串
    ${string:position:length} 	       在 $string 中，从位置 $position 开始提取长度为 $length 的子串
    ${string#substring}                从变量 $string 的开头，删除最短匹配 $substring 的子串
    ${string##substring}               从变量 $string 的开头，删除最长匹配 $substring 的子串
    ${string%substring}                从变量 $string 的结尾，删除最短匹配 $substring 的子串
    ${string%%substring}               从变量 $string 的结尾，删除最长匹配 $substring 的子串
    ${string/substring/replacement}    使用 $replacement, 来代替第一个匹配的 $substring
    ${string//substring/replacement}   使用 $replacement, 代替所有匹配的 $substring
    ${string/#substring/replacement}   如果 $string 的前缀匹配 $substring,
                                       那么就用 $replacement 来代替匹配到的 $substring
    ${string/%substring/replacement}   如果 $string 的后缀匹配 $substring,
    ================================   ==========================================================

举例

.. code:: shell

    /// 取得字符串长度
    string=abc12342341          // 等号二边不要有空格
    echo ${#string}             // 结果 11
    expr length $string         // 结果 11
    expr "$string" : ".*"       // 结果 11 冒号二边要有空格，这里的：根 match 的用法差不多

    /// 字符串所在位置
    expr index $string '123'    // 结果 4 字符串对应的下标是从 1 开始的
    str="abc"
    expr index $str "b"  # 2
    expr index $str "x"  # 0
    expr index $str ""   # 0

    /// 字符串截取
    echo ${string:4}      //2342341  从第 4 位开始截取后面所有字符串
    echo ${string:3:6}    //123423   从第 3 位开始截取后面 6 位
    echo ${string: -4}    //2341  : 右边有空格   截取后 4 位
    echo ${string:(-4)}   //2341  同上
    expr substr $string 3 3   //123  从第 3 位开始截取后面 3 位
    str="abcdef"
    expr substr "$str" 4 5  # 从第四个位置开始取 5 个字符， def
    echo ${str:(-6):5}        # 从倒数第二个位置向左提取字符串，abcde
    echo ${str:(-4):3}      # 从倒数第二个位置向左提取 6 个字符，cde

    /// 匹配显示内容
    expr match $string '\([a-c]*[0-9]*\)'  //abc12342341
    expr $string : '\([a-c]*[0-9]\)'       //abc1
    expr $string : '.*[([0-9][0-9][0-9]\)' //341 显示括号中匹配的内容

    /// 截取不匹配的内容
    echo ${string#a*3}     //42341  从 $string 左边开始，去掉最短匹配子串
    echo ${string#c*3}     //abc12342341  这样什么也没有匹配到
    echo ${string#*c1*3}   //42341  从 $string 左边开始，去掉最短匹配子串
    echo ${string##a*3}    //41     从 $string 左边开始，去掉最长匹配子串
    echo ${string%3*1}     //abc12342  从 $string 右边开始，去掉最短匹配子串
    echo ${string%%3*1}    //abc12     从 $string 右边开始，去掉最长匹配子串
    str="abbc,def,ghi,abcjkl"
    echo ${str#a*c}     # 输出，def,ghi,abcjkl  一个井号 (#) 表示从左边截取掉最短的匹配 （这里把 abbc 字串去掉）
    echo ${str##a*c}    # 输出 jkl，             两个井号 (##) 表示从左边截取掉最长的匹配 （这里把 abbc,def,ghi,abc 字串去掉）
    echo ${str#"a*c"}   # 输出 abbc,def,ghi,abcjkl 因为 str 中没有"a*c"子串
    echo ${str##"a*c"}  # 输出 abbc,def,ghi,abcjkl 同理
    echo ${str#*a*c*}   # 空
    echo ${str##*a*c*}  # 空
    echo ${str#d*f)     # 输出 abbc,def,ghi,abcjkl,
    echo ${str#*d*f}    # 输出，ghi,abcjkl
    echo ${str%a*l}     # abbc,def,ghi  一个百分号 (%) 表示从右边截取最短的匹配
    echo ${str%%b*l}    # a             两个百分号表示 (%%) 表示从右边截取最长的匹配
    echo ${str%a*c}     # abbc,def,ghi,abcjkl

    /// 匹配并且替换
    echo ${string/23/bb}   //abc1bb42341  替换一次
    echo ${string//23/bb}  //abc1bb4bb41  双斜杠替换所有匹配
    echo ${string/#abc/bb} //bb12342341   #以什么开头来匹配，根 php 中的 ^ 有点像
    echo ${string/%41/bb}  //abc123423bb  % 以什么结尾来匹配，根 php 中的 $ 有点像
    str="apple, tree, apple tree"
    echo ${str/apple/APPLE}   # 替换第一次出现的 apple
    echo ${str//apple/APPLE}  # 替换所有 apple
    echo ${str/#apple/APPLE}  # 如果字符串 str 以 apple 开头，则用 APPLE 替换它
    echo ${str/%apple/APPLE}  # 如果字符串 str 以 apple 结尾，则用 APPLE 替换它

    /// 比较
    [[ "a.txt" == a* ]]        # 逻辑真 (pattern matching)
    [[ "a.txt" =~ .*\.txt ]]   # 逻辑真 (regex matching)
    [[ "abc" == "abc" ]]       # 逻辑真 (string comparision)
    [[ "11" < "2" ]]           # 逻辑真 (string comparision), 按 ascii 值比较

    /// 字符串删除
    $ test='c:/windows/boot.ini'
    $ echo ${test#/}
    c:/windows/boot.ini
    $ echo ${test#*/}
    windows/boot.ini
    $ echo ${test##*/}
    boot.ini
    $ echo ${test%/*}
    c:/windows
    $ echo ${test%%/*}
    #${变量名#substring 正则表达式}从字符串开头开始配备 substring, 删除匹配上的表达式。
    #${变量名 %substring 正则表达式}从字符串结尾开始配备 substring, 删除匹配上的表达式。
    #注意：${test##*/},${test%/*} 分别是得到文件名，或者目录地址最简单方法。

数组操作
==============
声明一个数组 ::

    declare -a array

数组赋值 ::

    A. array=(var1 var2 var3 ... varN)
    B. array=([0]=var1 [1]=var2 [2]=var3 ... [n]=varN)
    C. array[0]=var1
       arrya[1]=var2
       ...
       array[n]=varN
    D. ARRAY=()
       ARRAY+=('foo')
       ARRAY+=('bar')

计算数组元素个数 ::

    ${#array[@]}  或者  ${#array[*]}

引用数组 ::

    echo ${array[n]}

遍历数组 ::

    filename=(`ls`)
    for var in ${filename[@]};do
        echo $var
    done

参考资料
===========
#. `linux shell 字符串操作详解 （长度，读取，替换，截取，连接，对比，删除，位置 ） <http://justcoding.iteye.com/blog/1963463>`_
#. `BASH 数组用法小结 <http://snailwarrior.blog.51cto.com/680306/154704>`_

