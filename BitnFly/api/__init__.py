"""
A module BitNFly
"""
from collections import OrderedDict
from math import log


class _BitnFlyOperation(object):

    """
    This class providing a bitwise operation on object level
    """

    def __and__(self, other):

        """
        A bitwise operator &

        :param other: can be a int, a str or a object which inherit from
            BitnFly or it is a BitnFly
        :type other: int or str or object
        :return: True if other is set in self otherwise False
        :rtype: bool
        """

        if isinstance(other, int) and (getattr(self, 'get')(output=int) & other):
            return True

        elif isinstance(other, str) and getattr(self, '_is_set')(other):
            return True

        else:
            return False

    def __or__(self, other):

        """
        A bitwise operator | still not implemented

        :param other:
        :type other:
        :return:
        :rtype:
        """

        pass

    def __xor__(self, other):

        """
        A bitwise operator ^. Will turn on or off all bits in self with mask other

        :param other: can be a int, str or a list
        :type other: int, str, list
        :return: object it self
        :rtype: object
        """
        getattr(self, 'flip')(other)

        return self


class BitnFly(_BitnFlyOperation):

    """
    A BitNFly - the main object
    """

    def __init__(self, options, **kwargs):

        assert isinstance(options, list), 'an options attribute must be a list'

        self.__output = kwargs.get('output', int)

        self.__options = self._create_options([opt.upper() for opt in options])

        self.__opt_flags = 0x0
        self.__flags_swap_mask = 0x0

        self.__switch_state = True

        self._init()

    def __str__(self):
        return str(self.get())

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.get())

    def __getattr__(self, item):

        if item.upper() in self.__options:
            return self.__options.get(item.upper())

        return self.__getattribute__(item)

    def _create_options(self, options):

        """
        A helper protected method for a internal usage
        Will create a ordered dictionary

        :param options:
        :type options:
        :return:
        :rtype:
        """

        return OrderedDict(
            zip(options, [pow(2, x) for x in range(len(options))])
        )

    def _flip_bits(self, bit_num):

        """
        A helper protected method for a internal usage
        Will flip a bit or bits to opposite values

        :param bit_num: can be a int or a list
        :type bit_num: int, list
        """
        if isinstance(bit_num, int):

            bit_num = int(log(bit_num, 2))

            self.__opt_flags ^= (1 << bit_num)
            self.__flags_swap_mask ^= (1 << bit_num)

        if isinstance(bit_num, list):

            for bit in bit_num:

                bit = int(log(bit, 2))

                self.__opt_flags ^= (1 << bit)
                self.__flags_swap_mask ^= (1 << bit)

    def _flip_str(self, bit_name):

        """
        A helper protected method for a internal usage
        Will flip a bit or bits to opposite values

        :param bit_name:
        :type bit_name:
        :return:
        :rtype:
        """

        if isinstance(bit_name, str):

            bit_name = bit_name.upper()
            self.__opt_flags ^= (1 << list(self.__options.keys()).index(bit_name))
            self.__flags_swap_mask ^= (1 << list(self.__options.keys()).index(bit_name))

        elif isinstance(bit_name, list):

            for bit in bit_name:

                bit = bit.upper()
                self.__opt_flags ^= (1 << list(self.__options.keys()).index(bit))
                self.__flags_swap_mask ^= (1 << list(self.__options.keys()).index(bit))

    def _is_set(self, opt, result_as=None):

        """
        Check is some bit is set or not

        :param opt: string that represent some bit field
        :type opt: str
        :return: if opt bit is set True otherwise False
        :rtype: bool
        """

        opt = opt.upper()

        if result_as is None:
            return True if self.__options[opt] & self.__opt_flags else False

        elif result_as == 'int':
            return self.__options[opt] & self.__opt_flags

    def _is_type_list(self, bits, itype):

        """
        A factory helper method.
        Will test whether all elements in a list are from some type

        :param bits: a list of bits
        :type bits: list
        :param itype: a type for which we are looking for
        :type itype: str or int
        :return: if all elements are from itype type True otherwise False
        :rtype: bool
        """

        return len(bits) == len([x for x in bits if isinstance(x, itype)])

    def _is_digit_list(self, bits):

        """
        Test if all elements in list are int

        :param bits: a list of bits
        :type bits: list
        :return: True if all elements are int otherwise False
        :rtype: bool
        """

        return self._is_type_list(bits, int)

    def _is_alpha_list(self, bits):

        """
        Test if all elements in list are str

        :param bits: a list of bits
        :type bits: list
        :return: True if all elements are str otherwise False
        :rtype: bool
        """

        return self._is_type_list(bits, str)

    def _init(self):

        """
        Will initialize the bits and swap_mask

        :return: a tuple of current bits and swap mask
        :rtype: tuple
        """
        _flag, swap_mask = 0x0, 0x0

        for key, val in self.__options.items():

            if key in self.__options:
                swap_mask |= val

            _flag |= val

        self.__opt_flags, self.__flags_swap_mask = _flag, swap_mask

        return self.__opt_flags, self.__flags_swap_mask

    def _flip_conditions(self, bits, **kwargs):

        """
        Still not implemented

        :param bits:
        :type bits:
        :param callbacks:
        :type callbacks:
        :return:
        :rtype:
        """
        callback_int = kwargs.get('callback_int')
        callback_str = kwargs.get('callback_str')

        if isinstance(bits, int) or (isinstance(bits, list) and self._is_digit_list(bits)):
            callback_int(bits)

        if isinstance(bits, str) or (isinstance(bits, list) and self._is_alpha_list(bits)):
            callback_str(bits)

    def flip(self, bits):

        """
        Will flip bit or bits to opposite side

        :param bits: can be a int, a str, a list of int or a list of str
        :type bits: int, str, list
        :return: object it self
        :rtype: object
        """

        self._flip_conditions(bits, callback_int=self._flip_bits, callback_str=self._flip_str)
        return self

    def off(self):

        """
        Will turning off all bits, according to a swap mask

        :return: object it self
        :rtype: object
        """

        self.__opt_flags &= ~self.__flags_swap_mask
        self.__switch_state = False
        return self

    def on(self):

        """
        Will turn on all flags according to swap mask

        :return: object it self
        :rtype: object
        """

        if self.__switch_state is False:
            self.__opt_flags ^= self.__flags_swap_mask
            self.__switch_state = True

        return self

    def reset(self):

        """
        Reset all bits to initial values

        :return: object it's self
        :rtype: object
        """

        self._init()
        return self

    def get(self, bit=None, output=None):

        """
        Will return current bits mask, if arg bit is None, otherwise
        will try to extract it from the current bit mask

        :param bit:
        :type bit: str
        :param output:
        :type output:
        :return: a bit flag
        :rtype: int
        """

        call = output or self.__output

        if bit is None:
            return call(self.__opt_flags)

        elif isinstance(bit, int):

            if bit in self.__options.values():
                return call(self.__opt_flags & bit)

            elif bit not in self.__options.values() and bit <= sum(self.__options.values()):
                return call(self.__opt_flags & bit)

            else:
                return 0

        elif isinstance(bit, str):
            return self.__output(self._is_set(bit, 'int'))

        else:
            raise TypeError('A bit argument can be int or a str')

__all__ = [
    'BitnFly',
]