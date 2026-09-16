# pylint: disable=missing-docstring

"""Copyright 2026 Simeon Ehrig
SPDX-License-Identifier: MPL-2.0

Custom filter for alpaka specific filter rules.
"""

import unittest

from bashi.globals import ALPAKA_ACC_GPU_CUDA_ENABLE, CLANG, CMAKE, DEVICE_COMPILER, GCC, HOST_COMPILER, NVCC
from bashi.types import ParameterValuePair
from utils import default_remove_test, parse_expected_val_pairs

from alpaka_bashi.verify import remove_unsupported_cuda_sdk_for_clang_host_compiler


class TestClangHostCompilerForNvcc(unittest.TestCase):
    def test_remove_invalid_combinations(self):

        test_param_value_pairs: list[ParameterValuePair] = parse_expected_val_pairs(
            [
                ((HOST_COMPILER, GCC, 6), (CMAKE, "3.30.2")),
                ((HOST_COMPILER, CLANG, 9), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.2")),
                ((HOST_COMPILER, CLANG, 10), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.3")),
                ((HOST_COMPILER, CLANG, 12), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.4")),
                ((DEVICE_COMPILER, NVCC, 10.0), (HOST_COMPILER, CLANG, 12)),
                ((DEVICE_COMPILER, NVCC, 13.2), (HOST_COMPILER, CLANG, 14)),
                ((DEVICE_COMPILER, NVCC, 13.3), (HOST_COMPILER, CLANG, 16)),
                ((HOST_COMPILER, CLANG, 16), (DEVICE_COMPILER, NVCC, 13.4)),
                ((DEVICE_COMPILER, NVCC, 12.3), (HOST_COMPILER, GCC, 16)),
            ]
        )

        expected_results: list[ParameterValuePair] = parse_expected_val_pairs(
            [
                ((HOST_COMPILER, GCC, 6), (CMAKE, "3.30.2")),
                ((HOST_COMPILER, CLANG, 10), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.3")),
                ((HOST_COMPILER, CLANG, 12), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.4")),
                ((DEVICE_COMPILER, NVCC, 13.3), (HOST_COMPILER, CLANG, 16)),
                ((HOST_COMPILER, CLANG, 16), (DEVICE_COMPILER, NVCC, 13.4)),
                ((DEVICE_COMPILER, NVCC, 12.3), (HOST_COMPILER, GCC, 16)),
            ]
        )

        default_remove_test(
            remove_unsupported_cuda_sdk_for_clang_host_compiler,
            test_param_value_pairs,
            expected_results,
            self,
        )
