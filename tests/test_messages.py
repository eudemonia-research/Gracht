#!/usr/bin/env python3

import unittest
import threading
import time

import cryptonet
from examples.grachten import GrachtenBlock

class TestMessage(unittest.TestCase):
    ''' Test messages
    To Test:
    blocks_handler:
        repeated sending of blocks should not break the connection - this should be in both directions
    '''

    def setUp(self):
        ''' Create chain_vars for two clients and have them connect to each other.
         Using GrachtenBlock to test.
        '''
        chain_vars = (cryptonet.datastructs.ChainVars(), cryptonet.datastructs.ChainVars())
        chain_vars[0].mine = False
        chain_vars[1].mine = False
        chain_vars[0].address = ('127.0.0.1',32345)
        chain_vars[0].seeds = [('127.0.0.1',32346)]
        chain_vars[1].address = ('127.0.0.1',32346)
        chain_vars[1].seeds = [('127.0.0.1',32345)]
        chain_vars[0].genesis_binary = b'\x01O\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB\t\x00\xabT\xa9\x8c\xdcgs\xf46\x01\x01\x01\x01\x00 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x01\x00\x04SG\x9c\x93\x01\x00\x01\x00\x03\x01\x01\x00\x01\x01'
        chain_vars[1].genesis_binary = b'\x01O\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB\t\x00\xabT\xa9\x8c\xdcgs\xf46\x01\x01\x01\x01\x00 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x01\x00\x04SG\x9c\x93\x01\x00\x01\x00\x03\x01\x01\x00\x01\x01'

        self.networks = (cryptonet.Cryptonet(chain_vars=chain_vars[0]), cryptonet.Cryptonet(chain_vars=chain_vars[1]))

        self.networks[0].block(GrachtenBlock)
        self.networks[1].block(GrachtenBlock)

        self.threads = [threading.Thread(target=n.run) for n in self.networks]
        for t in self.threads:
            t.start()

        time.sleep(0.5) # give everything time to warm up

    def test_block_propagation(self):
        ''' Broadcast blocks randomly and check both peers know about them at the end.
        '''
        blocks = [
            b'\x01\xe3\x01\xe1\x01\x01\x86\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB \x0e"\x08\x03Q~\x132\x045\x82\x9c\x17\xed\xb3\xd8d\x8f\xaa\xd4|\x8a\xcehm*\xd1@v\xe5@\xb9 A\x7f\x00\x84\xd1#\x9e\x90N^\x1cM\x80;\xae\xecV9\xaa\x1e.#D\xde\x04\x9f\xc5$o\x88\xb7\xa8 E\x9a\xb0\xf2\r3\x1b\xb9\xd2\x1e\xa7^Waz\xd1\x9as\xdfc\x12\xa3\xbd\x12\xd2\xc3V<y\xcc\x06=U\x01\x01\x01\x01\x01 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x02\x00\x04SU\x12\xdf\x01\x00\x01\x00"\x01 \x00\xdbq:*V\x1cv\xca\xac\xa9\x97M\x87\xb3\xb0\x88\x0et\x84G\xff\x07\x8d\xd8.\x03\xa9KR\xf2\x9c\x01\x01',
            b'\x01\xfb\x01\x06\x01\xfb\x01\x02\x01\x01\x86\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB eE.\xac\xf6#\xcb\x90k\x92\xac\xaf\xc8Sm\xa1g!\xb2#U\x1c\xa0\xdc\xc4\xfa\xe3_K\xd7\x08\x1c A\x7f\x00\x84\xd1#\x9e\x90N^\x1cM\x80;\xae\xecV9\xaa\x1e.#D\xde\x04\x9f\xc5$o\x88\xb7\xa8 E\x9a\xb0\xf2\r3\x1b\xb9\xd2\x1e\xa7^Waz\xd1\x9as\xdfc\x12\xa3\xbd\x12\xd2\xc3V<y\xcc\x05\xbfv\x01\x01\x01\x01\x02 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x03\x00\x04SU\x12\xe0\x01\x00\x01\x00C\x01 \x00\xfe\x03w\xdf!\x1b\xce}\xd7\x00\x83\xf6\xa5u\x87\xac\x14sJ_\xbd\xe4\xedd9\xd8\xed\x1a_\xad\xce \x00\xdbq:*V\x1cv\xca\xac\xa9\x97M\x87\xb3\xb0\x88\x0et\x84G\xff\x07\x8d\xd8.\x03\xa9KR\xf2\x9c\x01\x01',
            b'\x01\xfb\x01\x06\x01\xfb\x01\x02\x01\x01\x86\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB \x7f\xb8\xb5\x03\x03\xea\xb4\xb7\xaf>\xb6\x12:\xe60\xe3\x16\x11R\xea=3m{o4\xdeG\xab\xb5\x83\xe2 A\x7f\x00\x84\xd1#\x9e\x90N^\x1cM\x80;\xae\xecV9\xaa\x1e.#D\xde\x04\x9f\xc5$o\x88\xb7\xa8 E\x9a\xb0\xf2\r3\x1b\xb9\xd2\x1e\xa7^Waz\xd1\x9as\xdfc\x12\xa3\xbd\x12\xd2\xc3V<y\xcc\x07Yv\x01\x01\x01\x01\x03 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x04\x00\x04SU\x12\xe0\x01\x00\x01\x00C\x01 \x00\xf6\xad\xc0\x97\xf1\\G\xd7<%\xf3\xb8\xdb2\xc8\xd8\xabwYc\xf2\xd4\xcb%@\xfe\x1fvY@0 \x00\xfe\x03w\xdf!\x1b\xce}\xd7\x00\x83\xf6\xa5u\x87\xac\x14sJ_\xbd\xe4\xedd9\xd8\xed\x1a_\xad\xce\x01\x01',
            b'\x01\xfb\x01(\x01\xfb\x01$\x01\x01\x87\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB!\x00\xcc\xe2\x17Y\x00\x18\xd0k;\xc5H\x11\x97N\x18.\x91\x05\xedI\x08l\x88\xef\xa4\x88\x93I\x02\xed\x14\x02 A\x7f\x00\x84\xd1#\x9e\x90N^\x1cM\x80;\xae\xecV9\xaa\x1e.#D\xde\x04\x9f\xc5$o\x88\xb7\xa8 E\x9a\xb0\xf2\r3\x1b\xb9\xd2\x1e\xa7^Waz\xd1\x9as\xdfc\x12\xa3\xbd\x12\xd2\xc3V<y\xcc\x06\xd5\x97\x01\x01\x01\x01\x04 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x05\x00\x04SU\x12\xe0\x01\x00\x01\x00d\x01 \x00\x9e\t\xe7H\x00g\xd6\xfa\x8cZX(/\xe9(Sa\x03l\xeb\xf8aZ\xf7c)\xfc\xc6\x9b\x11t \x00\xf6\xad\xc0\x97\xf1\\G\xd7<%\xf3\xb8\xdb2\xc8\xd8\xabwYc\xf2\xd4\xcb%@\xfe\x1fvY@0 \x00\xdbq:*V\x1cv\xca\xac\xa9\x97M\x87\xb3\xb0\x88\x0et\x84G\xff\x07\x8d\xd8.\x03\xa9KR\xf2\x9c\x01\x01',
            b"\x01\xfb\x01'\x01\xfb\x01#\x01\x01\x87\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB!\x00\x99\xde\x18\xb8`l\x8a\xa3\x17\xf0\xf2\xd6\x19{F|\x92\x11D\x03\x92\xf5\x88\xcba\xd8\xb9\x867w\xbf\xfb A\x7f\x00\x84\xd1#\x9e\x90N^\x1cM\x80;\xae\xecV9\xaa\x1e.#D\xde\x04\x9f\xc5$o\x88\xb7\xa8 E\x9a\xb0\xf2\r3\x1b\xb9\xd2\x1e\xa7^Waz\xd1\x9as\xdfc\x12\xa3\xbd\x12\xd2\xc3V<y\xcc\x05\xa1\x96\x01\x01\x01\x01\x05 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x06\x00\x04SU\x12\xe0\x01\x00\x01\x00c\x01\x1f2R\xde\x88\x1b\x08V\x83\x85\x1c\xd1\x9c\xa8X\x9c\x8d\xe1?\xfe\xf4\xcak!\x10\x92\xdf\x1bj\x1b\x1a& \x00\x9e\t\xe7H\x00g\xd6\xfa\x8cZX(/\xe9(Sa\x03l\xeb\xf8aZ\xf7c)\xfc\xc6\x9b\x11t \x00\xfe\x03w\xdf!\x1b\xce}\xd7\x00\x83\xf6\xa5u\x87\xac\x14sJ_\xbd\xe4\xedd9\xd8\xed\x1a_\xad\xce\x01\x01",
            b'\x01\xfb\x01&\x01\xfb\x01"\x01\x01\x86\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB jV\xb24\x1cd\xa0q*\t\x18\x08\xdb\x98%\xd5\x15\xc2)/\x98E3R7\xac\x02\xc7\xa5\x83\xb0\xa3 A\x7f\x00\x84\xd1#\x9e\x90N^\x1cM\x80;\xae\xecV9\xaa\x1e.#D\xde\x04\x9f\xc5$o\x88\xb7\xa8 E\x9a\xb0\xf2\r3\x1b\xb9\xd2\x1e\xa7^Waz\xd1\x9as\xdfc\x12\xa3\xbd\x12\xd2\xc3V<y\xcc\x05\xce\x96\x01\x01\x01\x01\x06 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x07\x00\x04SU\x12\xe1\x01\x00\x01\x00c\x01 \x00\x9cv\xf7Y\xf2I\xcd\xe0\xe2\xbb\x95\\\xb2d9j\x1e}\xa5\xc1\x0c\xf9\x0e)jH\xaa@\x9f\xfb%\x1f2R\xde\x88\x1b\x08V\x83\x85\x1c\xd1\x9c\xa8X\x9c\x8d\xe1?\xfe\xf4\xcak!\x10\x92\xdf\x1bj\x1b\x1a& \x00\xf6\xad\xc0\x97\xf1\\G\xd7<%\xf3\xb8\xdb2\xc8\xd8\xabwYc\xf2\xd4\xcb%@\xfe\x1fvY@0\x01\x01',
            b"\x01\xfb\x01'\x01\xfb\x01#\x01\x01\x87\x01!\x00\xd7gm\xa06{\xa2\xa6\xa3{\x0b\xd6\xb6\xc2\x80\xfc\x19\xca\xf5WD\x8am\xae\xe1+\xaf\xaa\x86\x9b\xfbB!\x00\xc46/nj\xb2\x8bq\xd0\xb1f\x91\xfa3\xb0\xc5\x80b\x15G|_\xdc\x19\xac\x06\x85\x13\xfc\xaa\xf5. A\x7f\x00\x84\xd1#\x9e\x90N^\x1cM\x80;\xae\xecV9\xaa\x1e.#D\xde\x04\x9f\xc5$o\x88\xb7\xa8 E\x9a\xb0\xf2\r3\x1b\xb9\xd2\x1e\xa7^Waz\xd1\x9as\xdfc\x12\xa3\xbd\x12\xd2\xc3V<y\xcc\x05{\x96\x01\x01\x01\x01\x07 \x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x02\x08\x00\x04SU\x12\xe1\x01\x00\x01\x00c\x01\x1f^\xd5&H3e\x7f\xc3M,Q\x98z86\x8eo!\xba\xf3r[]\x00\x7fT\xd4K\xf5\x8a\x9c \x00\x9cv\xf7Y\xf2I\xcd\xe0\xe2\xbb\x95\\\xb2d9j\x1e}\xa5\xc1\x0c\xf9\x0e)jH\xaa@\x9f\xfb% \x00\x9e\t\xe7H\x00g\xd6\xfa\x8cZX(/\xe9(Sa\x03l\xeb\xf8aZ\xf7c)\xfc\xc6\x9b\x11t\x01\x01",
        ]

        network_order = (0,0,1,1,0,1,0,0,1,1)
        for i in range(len(blocks)):
            self.networks[network_order[i]].p2p.broadcast('blocks', blocks[i])
            time.sleep(0.5)
        print(self.networks[0].chain.head.height)
        self.assertTrue(self.networks[0].chain.head.height == 7)
        self.assertTrue(self.networks[1].chain.head.height == 7)

    def tearDown(self):
        for n in self.networks:
            n.shutdown()


if __name__ == '__main__':
    unittest.main()
