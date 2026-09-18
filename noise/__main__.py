from noise.hashrandom import HashRandom
from noise.tests import run_all_tests


#run_all_tests()

class HashRandomTest(HashRandom):
    def getrandbits(self, k: int) -> int:
        if k == 0:
            return 0

        l = self.bit_length()


        b = self._bits_used
        data = int.from_bytes(self, byteorder='little', signed=False)>>(l-k-b)

        print(f'bits to get: {k}, len: {l}, used: {b};; lkb: {l-k-b}')
        print(f'self: {bytes(self).hex()}')
        b = data.bit_length()
        print(f'data: {hex(data)}, len: {b}')

        while b < k:
            data <<= l
            b += l
            data ^= int.from_bytes(self.nextstate(), byteorder='little', signed=False)
        if b > k:
            self._bits_used = b-k
            data >>= self._bits_used
        return data

rng = HashRandomTest('Hello, World!!', size=4)
rng.getrandbits(0)
rng.getrandbits(12)
rng.getrandbits(12)