[![Build Status](https://travis-ci.org/dimddev/bitnfly.svg?branch=master)](https://travis-ci.org/dimddev/bitnfly) [![Coverage Status](https://coveralls.io/repos/github/dimddev/bitnfly/badge.svg?branch=master)](https://coveralls.io/github/dimddev/bitnfly?branch=master) [![PyPI](https://img.shields.io/badge/python-2.6%2C%202.7%2C%203.3%2C%203.4%2C%20PyPy%20-blue.svg)](https://travis-ci.org/dimddev/bitnfly) 
# BitnFly
### is a simple API for working with bit flags

#### install
```sh
$ git clone https://github.com/dimddev/bitnfly
$ cd bitnfly 
$ python setup.py install
```

#### usage:
##### ipython example

```sh
$ ipython
```
```python
In [1]: from BitnFly.api import BitnFly
```
BitnFly constructor accept a list of stings. Each value will be transformed into bit flag, from left to right: pow(2, 0), pow(2, 1), pow(2, 2) etc. So that meaning "read" is 0x1, "delete" is 0x2, "write" is 0x4 and "exeute" will be 0x8, all together 0xf or 1111 in binary

```python
In [2]: b = BitnFly(['read', 'delete', 'write', 'execute'], output=bin)
```
We can easily check for some bit state with a `get` method. A `get` method accept for an arguments: str; int; [int, int...]; ( list of integers) and [str, str, ...]; ( list of strings )

example usage:

```python

In [3]: b.get()
Out[3]: '0b1111'

In [4]: b.get(1)
Out[4]: '0b1'

In [5]: b.get(8)
Out[5]: '0b1000'

In [6]: b.get('read')
Out[6]: '0b1'

In [7]: b.get('execute')
Out[7]: '0b1000'

In [8]: b.get(b.READ)
Out[8]: '0b1'

In [9]: b.get(b.WRITE)
Out[9]: '0b100'

In [10]: b.get(b.WRITE, output=hex)
Out[10]: '0x4'
```

We can flip one or more bits to its inverse value with a `flip` method. As `get` flip accept the same arguments eg:
str; int; [int, int...]; ( list of integers) and [str, str, ...]; ( list of strings )

```python
In [11]: b.flip(b.READ)
Out[11]: <BitnFly(0b1110)>

In [12]: b.flip(b.WRITE)
Out[12]: <BitnFly(0b1010)>

In [13]: b.flip([b.WRITE, b.READ])
Out[13]: <BitnFly(0b1111)>

In [14]: b.flip(1)
Out[14]: <BitnFly(0b1110)>

In [15]: b.flip(1)
Out[15]: <BitnFly(0b1111)>

In [16]: b.flip('read')
Out[16]: <BitnFly(0b1110)>

In [17]: b.flip('delete')
Out[17]: <BitnFly(0b1100)>

In [18]: b.flip(['delete', 'read'])
Out[18]: <BitnFly(0b1111)>

In [19]: b.flip([b.READ, b.EXECUTE])
Out[19]: <BitnFly(0b110)>
```

If you want to turn off all bits we should use a `off` method. It will turn off all remaining bits to zero

```python
In [20]: b.off()
Out[20]: <BitnFly(0b0)>
```
then if we want to restore all bit states to point to it's state before of calling a method `off` we can use a `on` method, in short it's work as undo of our `off` method

```python
In [21]: b.on()
Out[21]: <BitnFly(0b110)>
```
All bits are restored,

let's do some bit `flip`, `off` and `on` executions

```python
In [22]: b.flip(b.WRITE)
Out[22]: <BitnFly(0b10)>

In [23]: b.off()
Out[23]: <BitnFly(0b0)>

In [24]: b.on()
Out[24]: <BitnFly(0b10)>
```
If you want to reset all bit states to its initial values use a `reset` method

```python
In [25]: b.reset()
Out[25]: <BitnFly(0b1111)>
```
An BitbFly API also supports a simple bitwise operations on object level

Bitwise `and`

```python
In [26]: b & b.READ
Out[26]: True

In [27]: b & b.READ and b & b.WRITE
Out[27]: True

In [28]: b & 'read'
Out[28]: True

In [29]: b & 'read' and b & b.WRITE
Out[29]: True

In [30]: b
Out[31]: <BitnFly(0b1111)>
```

Bitwise `xor`

```python
In [32]: b ^= b.READ

In [33]: b
Out[33]: <BitnFly(0b1110)>

In [34]: b ^= b.WRITE

In [35]: b
Out[35]: <BitnFly(0b1010)>

In [36]: b ^= b.WRITE

In [37]: b
Out[37]: <BitnFly(0b1110)>

In [38]: b.reset()
Out[38]: <BitnFly(0b1111)>
```

Bitwise `or`

```python

In [39]: b.off()
Out[39]: <BitnFly(0b0)>

In [40]: b |= b.READ

In [41]: b
Out[41]: <BitnFly(0b1)>

In [42]: b |= [b.WRITE, b.DELETE]

In [43]: b
Out[43]: <BitnFly(0b111)>

In [44]: b |= b.EXECUTE

In [45]: b
Out[45]: <BitnFly(0b1111)>

In [46]: b.off()
Out[46]: <BitnFly(0b0)>

In [47]: b |= 'read'

In [48]: b
Out[48]: <BitnFly(0b1)>

In [49]: b |= ['write', 'delete', 'execute']

In [50]: b
Out[50]: <BitnFly(0b1111)>


```