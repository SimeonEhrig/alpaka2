#!/usr/bin/env bash

#
# Copyright 2026 Simeon Ehrig
# SPDX-License-Identifier: MPL-2.0
#

if ! command -v spack && [[ -d /spack ]]; then
    . /spack/share/spack/setup-env.sh
fi
