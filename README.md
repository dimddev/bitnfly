# BitnFly
### is a simple API for working with bit flags

#### usage:

```sh
ipython
```
```python
In [1]: from BitnFly.api import BitnFly

In [2]: b = BitnFly(['read', 'delete', 'write', 'execute'], output=bin)

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

In [20]: b.off()
Out[20]: <BitnFly(0b0)>

In [21]: b.on()
Out[21]: <BitnFly(0b110)>

In [22]: b.flip(b.WRITE)
Out[22]: <BitnFly(0b10)>

In [23]: b.off()
Out[23]: <BitnFly(0b0)>

In [24]: b.on()
Out[24]: <BitnFly(0b10)>

In [25]: b.reset()
Out[25]: <BitnFly(0b1111)>
```
