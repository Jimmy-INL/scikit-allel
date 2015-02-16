# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import unittest
import tempfile


import numpy as np
import bcolz
import h5py
from nose.tools import eq_ as eq, assert_raises


from allel.model import GenotypeArray, HaplotypeArray
from allel.test.tools import assert_array_equal as aeq
from allel.test.test_model_api import GenotypeArrayInterface, \
    HaplotypeArrayInterface, diploid_genotype_data, triploid_genotype_data, \
    haplotype_data
from allel.bcolz import GenotypeCArray, HaplotypeCArray


class GenotypeCArrayTests(GenotypeArrayInterface, unittest.TestCase):

    _class = GenotypeCArray

    def setup_instance(self, data):
        return GenotypeCArray(data)

    def test_constructor(self):

        # missing data arg
        with assert_raises(TypeError):
            # noinspection PyArgumentList
            GenotypeCArray()

        # data has wrong dtype
        data = 'foo bar'
        with assert_raises(NotImplementedError):
            GenotypeCArray(data)

        # data has wrong dtype
        data = [4., 5., 3.7]
        with assert_raises(TypeError):
            GenotypeCArray(data)

        # data has wrong dimensions
        data = [1, 2, 3]
        with assert_raises(TypeError):
            GenotypeCArray(data)

        # data has wrong dimensions
        data = [[1, 2], [3, 4]]  # use HaplotypeCArray instead
        with assert_raises(TypeError):
            GenotypeCArray(data)

        # diploid data (typed)
        g = GenotypeCArray(diploid_genotype_data, dtype='i1')
        aeq(diploid_genotype_data, g)
        eq(np.int8, g.dtype)

        # polyploid data (typed)
        g = GenotypeCArray(triploid_genotype_data, dtype='i1')
        aeq(triploid_genotype_data, g)
        eq(np.int8, g.dtype)

        # cparams
        g = GenotypeCArray(diploid_genotype_data,
                           cparams=bcolz.cparams(clevel=10))
        aeq(diploid_genotype_data, g)
        eq(10, g.cparams.clevel)

    def test_slice_types(self):

        g = GenotypeCArray(diploid_genotype_data, dtype='i1')

        # row slice
        s = g[1:]
        self.assertNotIsInstance(s, GenotypeCArray)
        self.assertIsInstance(s, GenotypeArray)

        # col slice
        s = g[:, 1:]
        self.assertNotIsInstance(s, GenotypeCArray)
        self.assertIsInstance(s, GenotypeArray)

        # row index
        s = g[0]
        self.assertNotIsInstance(s, GenotypeCArray)
        self.assertNotIsInstance(s, GenotypeArray)
        self.assertIsInstance(s, np.ndarray)

        # col index
        s = g[:, 0]
        self.assertNotIsInstance(s, GenotypeCArray)
        self.assertNotIsInstance(s, GenotypeArray)
        self.assertIsInstance(s, np.ndarray)

        # ploidy index
        s = g[:, :, 0]
        self.assertNotIsInstance(s, GenotypeCArray)
        self.assertNotIsInstance(s, GenotypeArray)
        self.assertIsInstance(s, np.ndarray)

        # item
        s = g[0, 0, 0]
        self.assertNotIsInstance(s, GenotypeCArray)
        self.assertNotIsInstance(s, GenotypeArray)
        self.assertIsInstance(s, np.int8)

    def test_from_hdf5(self):

        # setup HDF5 file
        node_path = 'test'
        tf = tempfile.NamedTemporaryFile(delete=False)
        file_path = tf.name
        tf.close()
        with h5py.File(file_path, mode='w') as h5f:
            h5f.create_dataset(node_path,
                               data=diploid_genotype_data,
                               chunks=(2, 3, 2))

        # file and node path
        g = GenotypeCArray.from_hdf5(file_path, node_path)
        aeq(diploid_genotype_data, g)
        
        # dataset
        with h5py.File(file_path, mode='r') as h5f:
            dataset = h5f[node_path]
            g = GenotypeCArray.from_hdf5(dataset)
            aeq(diploid_genotype_data, g)


class HaplotypeCArrayTests(HaplotypeArrayInterface, unittest.TestCase):

    _class = HaplotypeCArray

    def setup_instance(self, data):
        return HaplotypeCArray(data)

    def test_constructor(self):

        # missing data arg
        with assert_raises(TypeError):
            # noinspection PyArgumentList
            HaplotypeCArray()

        # data has wrong dtype
        data = 'foo bar'
        with assert_raises(NotImplementedError):
            HaplotypeCArray(data)

        # data has wrong dtype
        data = [4., 5., 3.7]
        with assert_raises(TypeError):
            GenotypeCArray(data)

        # data has wrong dimensions
        data = [1, 2, 3]
        with assert_raises(TypeError):
            HaplotypeCArray(data)

        # data has wrong dimensions
        data = [[[1, 2], [3, 4]]]  # use GenotypeCArray instead
        with assert_raises(TypeError):
            HaplotypeCArray(data)

        # typed data (typed)
        h = HaplotypeCArray(haplotype_data, dtype='i1')
        aeq(haplotype_data, h)
        eq(np.int8, h.dtype)

        # cparams
        h = HaplotypeCArray(haplotype_data,
                            cparams=bcolz.cparams(clevel=10))
        aeq(haplotype_data, h)
        eq(10, h.cparams.clevel)

    def test_slice_types(self):

        h = HaplotypeCArray(haplotype_data, dtype='i1')

        # row slice
        s = h[1:]
        self.assertNotIsInstance(s, HaplotypeCArray)
        self.assertIsInstance(s, HaplotypeArray)

        # col slice
        s = h[:, 1:]
        self.assertNotIsInstance(s, HaplotypeCArray)
        self.assertIsInstance(s, HaplotypeArray)

        # row index
        s = h[0]
        self.assertNotIsInstance(s, HaplotypeCArray)
        self.assertNotIsInstance(s, HaplotypeArray)
        self.assertIsInstance(s, np.ndarray)

        # col index
        s = h[:, 0]
        self.assertNotIsInstance(s, HaplotypeCArray)
        self.assertNotIsInstance(s, HaplotypeArray)
        self.assertIsInstance(s, np.ndarray)

        # item
        s = h[0, 0]
        self.assertNotIsInstance(s, HaplotypeCArray)
        self.assertNotIsInstance(s, HaplotypeArray)
        self.assertIsInstance(s, np.int8)

    def test_from_hdf5(self):

        # setup HDF5 file
        node_path = 'test'
        tf = tempfile.NamedTemporaryFile(delete=False)
        file_path = tf.name
        tf.close()
        with h5py.File(file_path, mode='w') as h5f:
            h5f.create_dataset(node_path,
                               data=haplotype_data,
                               chunks=(2, 3))

        # file and node path
        h = HaplotypeCArray.from_hdf5(file_path, node_path)
        aeq(haplotype_data, h)
        
        # dataset
        with h5py.File(file_path, mode='r') as h5f:
            dataset = h5f[node_path]
            h = HaplotypeCArray.from_hdf5(dataset)
            aeq(haplotype_data, h)