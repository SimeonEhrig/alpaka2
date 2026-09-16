# pylint: disable=missing-docstring

"""Copyright 2026 Simeon Ehrig
SPDX-License-Identifier: MPL-2.0

Custom filter for alpaka specific filter rules.
"""

import io
import unittest

from bashi.globals import ALPAKA_ACC_GPU_CUDA_ENABLE, CLANG, DEVICE_COMPILER, GCC, HOST_COMPILER, NVCC, OFF
from utils import parse_bashi_row

from alpaka_bashi.alpaka_filter import (
    AlpakaFilter,
    check_clang_host_compiler_supported_cuda_sdk_a2,
    check_clang_host_compiler_supported_nvcc_a3,
)


class TestClangHostCompilerCUDAsdk(unittest.TestCase):
    VALID_ROWS = [
        [(HOST_COMPILER, CLANG, 17), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.3")],
        [(HOST_COMPILER, CLANG, 9), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.8")],
        [(HOST_COMPILER, CLANG, 12), (ALPAKA_ACC_GPU_CUDA_ENABLE, OFF)],
        [(HOST_COMPILER, GCC, 13), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.3")],
    ]

    def test_valid_clang_host_compiler_supported_cuda_sdk_a2(self):
        for row in self.VALID_ROWS:
            with self.subTest(row=row):
                self.assertTrue(
                    check_clang_host_compiler_supported_cuda_sdk_a2(parse_bashi_row(row), AlpakaFilter()),
                    f"{row}",
                )
                self.assertTrue(AlpakaFilter()(parse_bashi_row(row)), f"{row}")

    INVALID_ROWS = [
        [(HOST_COMPILER, CLANG, 17), (ALPAKA_ACC_GPU_CUDA_ENABLE, "13.2")],
        [(HOST_COMPILER, CLANG, 9), (ALPAKA_ACC_GPU_CUDA_ENABLE, "12.8")],
        [(HOST_COMPILER, CLANG, 30), (ALPAKA_ACC_GPU_CUDA_ENABLE, "11.0")],
    ]

    def test_invalid_clang_host_compiler_supported_cuda_sdk_a2(self):
        EXPECTED_ERROR_MSG = "Clang as nvcc host compiler is only working since CUDA 13.3."

        for row in self.INVALID_ROWS:
            with self.subTest(row=row):
                reason_msg_func = io.StringIO()
                self.assertFalse(
                    check_clang_host_compiler_supported_cuda_sdk_a2(
                        parse_bashi_row(row), AlpakaFilter(output=reason_msg_func)
                    ),
                    f"{row}",
                )
                self.assertEqual(reason_msg_func.getvalue(), EXPECTED_ERROR_MSG, f"{row}")

                reason_msg_filter = io.StringIO()
                self.assertFalse(AlpakaFilter(output=reason_msg_filter)(parse_bashi_row(row)), f"{row}")
                self.assertEqual(reason_msg_filter.getvalue(), EXPECTED_ERROR_MSG, f"{row}")


class TestClangHostCompilerNvcc(unittest.TestCase):
    VALID_ROWS = [
        [(HOST_COMPILER, CLANG, 17), (DEVICE_COMPILER, NVCC, "13.3")],
        [(HOST_COMPILER, CLANG, 9), (DEVICE_COMPILER, NVCC, "13.8")],
        [(HOST_COMPILER, GCC, 13), (DEVICE_COMPILER, NVCC, "13.3")],
    ]

    def test_valid_check_clang_host_compiler_supported_nvcc_a3(self):
        for row in self.VALID_ROWS:
            with self.subTest(row=row):
                self.assertTrue(
                    check_clang_host_compiler_supported_nvcc_a3(parse_bashi_row(row), AlpakaFilter()),
                    f"{row}",
                )
                self.assertTrue(AlpakaFilter()(parse_bashi_row(row)), f"{row}")

    INVALID_ROWS = [
        [(HOST_COMPILER, CLANG, 17), (DEVICE_COMPILER, NVCC, "13.2")],
        [(HOST_COMPILER, CLANG, 9), (DEVICE_COMPILER, NVCC, "12.8")],
        [(HOST_COMPILER, CLANG, 30), (DEVICE_COMPILER, NVCC, "11.0")],
    ]

    def test_invalid_check_clang_host_compiler_supported_nvcc_a3(self):
        EXPECTED_ERROR_MSG = "The Clang host compiler is only working since nvcc 13.3."

        for row in self.INVALID_ROWS:
            with self.subTest(row=row):
                reason_msg_func = io.StringIO()
                self.assertFalse(
                    check_clang_host_compiler_supported_nvcc_a3(
                        parse_bashi_row(row), AlpakaFilter(output=reason_msg_func)
                    ),
                    f"{row}",
                )
                self.assertEqual(reason_msg_func.getvalue(), EXPECTED_ERROR_MSG, f"{row}")

                reason_msg_filter = io.StringIO()
                self.assertFalse(AlpakaFilter(output=reason_msg_filter)(parse_bashi_row(row)), f"{row}")
                self.assertEqual(reason_msg_filter.getvalue(), EXPECTED_ERROR_MSG, f"{row}")
