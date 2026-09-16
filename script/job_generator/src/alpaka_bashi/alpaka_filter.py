"""Copyright 2026 Simeon Ehrig
SPDX-License-Identifier: MPL-2.0

Custom filter for alpaka specific filter rules.
"""

import bashi
import packaging.version
from bashi.globals import ALPAKA_ACC_GPU_CUDA_ENABLE, CLANG, DEVICE_COMPILER, HOST_COMPILER, NVCC
from bashi.results import OFF_VER

from alpaka_bashi.versions import get_allowed_backend_combinations, get_used_backends


def check_only_valid_backend_combinations_a1(row: bashi.BashiRow, alpaka_filter: "AlpakaFilter") -> bool:
    """
    Check if still possible valid backend combinations exist.

    Args:
        row (bashi.BashiRow): parameter-value-tuple to verify.
        alpaka_filter (AlpakaFilter): alpaka filter

    Returns:
        bool: True if passed.
    """
    if (
        len(bashi.get_valid_compiler_backend_combinations(row, get_allowed_backend_combinations(), get_used_backends()))
        == 0
    ):
        alpaka_filter.reason("No valid backend combination available.")
        return False
    return True


def check_clang_host_compiler_supported_cuda_sdk_a2(row: bashi.BashiRow, alpaka_filter: "AlpakaFilter") -> bool:
    """
    Clang as nvcc host compiler is only working since CUDA 13.3.

    Args:
        row (bashi.BashiRow): parameter-value-tuple to verify.
        alpaka_filter (AlpakaFilter): alpaka filter

    Returns:
        bool: True if passed.
    """
    if (
        row[HOST_COMPILER].name == CLANG
        and row[ALPAKA_ACC_GPU_CUDA_ENABLE].version > OFF_VER
        and row[ALPAKA_ACC_GPU_CUDA_ENABLE].version < packaging.version.parse("13.3")
    ):
        alpaka_filter.reason("Clang as nvcc host compiler is only working since CUDA 13.3.")
        return False

    return True


def check_clang_host_compiler_supported_nvcc_a3(row: bashi.BashiRow, alpaka_filter: "AlpakaFilter") -> bool:
    """
    Clang as nvcc host compiler is only working since CUDA 13.3.

    Args:
        row (bashi.BashiRow): parameter-value-tuple to verify.
        alpaka_filter (AlpakaFilter): alpaka filter

    Returns:
        bool: True if passed.
    """
    if (
        row[HOST_COMPILER].name == CLANG
        and row[DEVICE_COMPILER].name == NVCC
        and row[DEVICE_COMPILER].version < packaging.version.parse("13.3")
    ):
        alpaka_filter.reason("The Clang host compiler is only working since nvcc 13.3.")
        return False

    return True


# pylint: disable=too-few-public-methods
class AlpakaFilter(bashi.FilterBase):
    """Alpaka specific filter rules."""

    def __call__(
        self,
        row: bashi.BashiRow,
    ) -> bool:
        """Check if given parameter-value-tuple is valid

        Args:
            row (bashi.BashiRow): parameter-value-tuple to verify.

        Returns:
            bool: True, if parameter-value-tuple is valid.
        """

        return (
            check_only_valid_backend_combinations_a1(row, self)
            and check_clang_host_compiler_supported_cuda_sdk_a2(row, self)
            and check_clang_host_compiler_supported_nvcc_a3(row, self)
        )
