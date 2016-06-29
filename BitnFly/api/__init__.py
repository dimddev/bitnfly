"""
A module BitNFly
"""

from collections import OrderedDict
from math import log


class BitnFly(object):

    """
    A BitNFly - the main object
    """

    def __init__(self, options, **kwargs):

        """
        The constructor will configure all needed variables

        :param options: list of strings, each value will be represented as pow(index, 2) from left to right
        :type options: list
        :param kwargs: a possible key is an 'output` with callable value eg. hex, bin; default is int
        :type kwargs: dict
        """

        assert isinstance(options, list), 'an options attribute must be a list'

        self.__output = kwargs.get('output', int)

        self.__options = self._create_options([opt.upper() for opt in options])

        self.__opt_flags = 0x0
        self.__flags_swap_mask = 0x0

        self.__repr_swap_mask = kwargs.get('mask', None)

        self.__switch_state = True
        self.__operation = '__xor__'

        self._init()

    def __and__(self, other):

        """
        A bitwise operator &

        :param other: can be an int or a str
        :type other: int or str
        :return: True if other is set in self otherwise False
        :rtype: bool
        """

        if isinstance(other, int) and self.get(output=int) & other:
            return True

        elif isinstance(other, str) and self._is_set(other):
            return True

        else:
            return False

    def __or__(self, other):

        """
        A bitwise operator |

        :param other: can be an int, a str, a list of int or a list of str
        :type other: int, str, list
        :return: self
        :rtype: self
        """

        self.__operation = '__or__'

        self._args_callback(other, callback_int=self._bitnfly_bits, callback_str=self._bitnfly_str)
        return self

    def __xor__(self, other):

        """
        A bitwise operator ^. Will turn on or off all bits in self with mask other

        :param other: can be an int, a str, a list of int or a list of str
        :type other: int, str, list
        :return: object it self
        :rtype: object
        """

        self.__operation = '__xor__'
        self.flip(other)

        return self

    def __str__(self):
        return str(self.get())

    def __repr__(self):

        return '{}({}, mask={})'.format(
            self.__class__.__name__,
            [flags.lower() for flags in self.__options.keys()],
            self.get(),
            self.__flags_swap_mask
        )

    def __getattr__(self, item):

        if item.upper() in self.__options:
            return self.__options.get(item.upper())

        return self.__getattribute__(item)

    @staticmethod
    def _create_options(options):

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

    def _bitnfly_bits_xor(self, bit):
        """
        Flip bits - xor
        :param bit:
        :type bit:
        :return:
        :rtype:
        """
        self.__opt_flags ^= (1 << bit)
        self.__flags_swap_mask ^= (1 << bit)

    def _bitnfly_bits_or(self, bit):
        """
        Or bit
        :param bit:
        :type bit:
        :return:
        :rtype:
        """
        self.__opt_flags |= (1 << bit)
        self.__flags_swap_mask |= (1 << bit)

    def _bitnfly_bits_helper(self, bit):
        """
        A helper bit method

        :param bit:
        :type bit:
        :return:
        :rtype:
        """
        if bit in self.__options.values():

            bit = int(log(bit, 2))

            if self.__operation == '__xor__':
                self._bitnfly_bits_xor(bit)

            else:
                self._bitnfly_bits_or(bit)

    def _bitnfly_bits_int(self, bit):
        """
        A function that care about bits
        :param bit: a bit
        :type bit: int
        :return: void
        :rtype: void
        """
        self._bitnfly_bits_helper(bit)

    def _bitnfly_bits_list(self, bit_num):
        """
        When we got a list ot bits
        :param bit_num:
        :type bit_num:
        :return:
        :rtype:
        """
        for bit in bit_num:
            self._bitnfly_bits_helper(bit)

    def _bitnfly_bits(self, bit_num):

        """
        A helper protected method for a internal usage
        Will flip a bit or bits to opposite values

        :param bit_num: can be a int or a list
        :type bit_num: int, list
        """

        if isinstance(bit_num, int):
            self._bitnfly_bits_int(bit_num)

        if isinstance(bit_num, list):
            self._bitnfly_bits_list(bit_num)

    def _bitnfly_str_xor(self, bit):

        """
        flip str xor

        :param bit:
        :type bit:
        :return:
        :rtype:
        """

        self.__opt_flags ^= (1 << list(self.__options.keys()).index(bit))
        self.__flags_swap_mask ^= (1 << list(self.__options.keys()).index(bit))

    def _bitnfly_str_or(self, bit):

        """
        flip str or

        :param bit:
        :type bit:
        :return:
        :rtype:
        """

        self.__opt_flags |= (1 << list(self.__options.keys()).index(bit))
        self.__flags_swap_mask |= (1 << list(self.__options.keys()).index(bit))

    def _bitnfly_str_list(self, bit_name):
        """
        When we got a list of strings
        :param bit_name:
        :type bit_name:
        :return:
        :rtype:
        """

        for bit in bit_name:

            bit = bit.upper()

            if self.__operation == '__xor__':
                self._bitnfly_str_xor(bit)

            else:
                self._bitnfly_str_or(bit)

    def _bitnfly_str_str(self, bit_name):
        """
        Case with a string bit
        :param bit_name:
        :type bit_name:
        :return:
        :rtype:
        """

        bit_name = bit_name.upper()

        if self.__operation == '__xor__':
            self._bitnfly_str_xor(bit_name)

        else:
            self._bitnfly_str_or(bit_name)

    def _bitnfly_str(self, bit_name):

        """
        A helper protected method for a internal usage
        Will flip a bit or bits to opposite values

        :param bit_name:
        :type bit_name:
        :return:
        :rtype:
        """

        if isinstance(bit_name, str):
            self._bitnfly_str_str(bit_name)

        elif isinstance(bit_name, list):
            self._bitnfly_str_list(bit_name)

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

    @staticmethod
    def _is_type_list(bits, itype):

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
        flag, swap_mask = 0x0, 0x0

        for _, val in self.__options.items():

            swap_mask |= val

            if self.__repr_swap_mask is None:
                flag |= val

        self.__opt_flags, self.__flags_swap_mask = flag or self.__repr_swap_mask, swap_mask

        return self.__opt_flags, self.__flags_swap_mask

    def _args_callback(self, bits, **kwargs):

        """
        A helper method, which care about all input arguments

        :param bits: a user query ca be a str an int, or a list of str or list or ints
        :type bits:
        :param kwargs: contains to required keys callback_int and callback_str, they must be callable
        :type kwargs: dict
        :return: void
        :rtype: void
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

        :param bits: can be an int, a str, a list of int or a list of str
        :type bits: int, str, list
        :return: object it self
        :rtype: object
        """

        self.__operation = '__xor__'

        self._args_callback(
            bits,
            callback_int=self._bitnfly_bits,
            callback_str=self._bitnfly_str,
        )
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
        :type bit: str or int
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

            else:
                return 0

        elif isinstance(bit, str):
            return self.__output(self._is_set(bit, 'int'))

        else:
            raise TypeError('A bit argument can be int or a str')

    def flags(self):
        """
        Will return all flags in ordered dict
        :return:
        :rtype:
        """
        return self.__options

    def mask(self):
        """
        Will return the current swap mask
        :return:
        :rtype:
        """
        return self.__flags_swap_mask

__all__ = [
    'BitnFly',
]
