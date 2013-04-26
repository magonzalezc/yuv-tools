#!/usr/bin/env python

import unittest
import hashlib

from ycbcr import YCbCr


SIZE_420 = 152064    # CIF w*h*3/2
SIZE_422 = 202752    # CIF w*h*2

def get_sha1(f, size):
    """
    return sha1sum
    """
    with open(f, 'rb') as fd:
        buf = fd.read(size)
        return hashlib.sha1(buf).hexdigest()

class TestYCbCrFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_1(self):
        """
        convert YV12 into itself
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                  yuv_format_in='YV12',
                  yuv_format_out='YV12', filename_out='test_1.yuv')
        a.convert()

        ret = get_sha1('test_1.yuv', SIZE_420)

        self.assertEqual(ret, 'c9120ccf583b410b75379c48325dd50ec8d16ce8')

    def test_2(self):
        """
        YV12 -> UYVY
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                  yuv_format_in='YV12',
                  yuv_format_out='UYVY', filename_out='test_2.yuv')
        a.convert()

        ret = get_sha1('test_2.yuv', SIZE_422)

        self.assertEqual(ret, 'f50fc0500b217256a87c7cd1e867da0c49c51ace')

    def test_3(self):
        """
        YV12 -> YVYU
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                  yuv_format_in='YV12',
                  yuv_format_out='YVYU', filename_out='test_3.yuv')
        a.convert()

        ret = get_sha1('test_3.yuv', SIZE_422)

        self.assertEqual(ret, '68ac533290a89625b910731c93fbecba89b61870')

    def test_4(self):
        """
        YV12 -> UVYU -> YV12
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                  yuv_format_in='YV12',
                  yuv_format_out='UYVY', filename_out='test_4.yuv')
        a.convert()

        b = YCbCr(width=352, height=288, filename='test_4.yuv',
                  yuv_format_in='UYVY',
                  yuv_format_out='YV12', filename_out='test_4_2.yuv')
        b.convert()

        ret = get_sha1('test_4_2.yuv', SIZE_422)

        self.assertEqual(ret, 'b8934d77e0d71e77e90b4ba777a0cb978679d8ec')

    def test_5(self):
        """
        YV12 -> 422
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                yuv_format_in='YV12',
                yuv_format_out='422', filename_out='test_5.yuv')
        a.convert()

        ret = get_sha1('test_5.yuv', SIZE_422)

        self.assertEqual(ret, 'c700a31a209df30b72c1097898740d4c42d63a42')

    def test_6(self):
        """
        diff
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                yuv_format_in='YV12',
                filename_diff='foreman_cif_frame_1.yuv')
        a.diff()

        ret = get_sha1('foreman_cif_frame_0_foreman_cif_frame_1_diff.yuv', SIZE_420)

        self.assertEqual(ret, '6b508de1971eaae965d3a3cf0c8715c6fe907aff')

    def test_7(self):
        """
        split
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                  yuv_format_in='YV12')
        a.split()

        ret = get_sha1('frame0.yuv', SIZE_420)

        self.assertEqual(ret, 'c9120ccf583b410b75379c48325dd50ec8d16ce8')

    def test_8(self):
        """
        psnr
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                  yuv_format_in='YV12', filename_diff='foreman_cif_frame_1.yuv')

        ret = a.psnr().next()

        self.assertEqual(ret, [27.717365657171168, 43.05959038403312, 43.377451819757276, 29.417480696534724])

    def test_9(self):
        """
        ssim
        """
        a = YCbCr(width=352, height=288, filename='foreman_cif_frame_0.yuv',
                  yuv_format_in='YV12', filename_diff='foreman_cif_frame_1.yuv')

        ret = a.ssim().next()

        self.assertEqual(ret, 0.8714863949031405)

    def test_10(self):
        """
        8bpp -> 10bpp
        """
        a = YCbCr(filename='foreman_cif_frame_0.yuv', filename_out='test_10.yuv')
        a.eight2ten()

        ret = get_sha1('test_10.yuv', SIZE_420 * 2)
        self.assertEqual(ret, '9cbade807771aa135f7f90b07e4bb510273b4e4f')

    def test_11(self):
        """
        10bpp -> 8bpp
        """
        a = YCbCr(filename='test_10.yuv', filename_out='test_11.yuv')
        a.ten2eight()

        ret = get_sha1('test_11.yuv', SIZE_420)
        self.assertEqual(ret, 'c9120ccf583b410b75379c48325dd50ec8d16ce8')

if __name__ == '__main__':
    unittest.main()