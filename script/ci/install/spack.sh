#!/usr/bin/env bash

#
# Copyright 2026 Simeon Ehrig
# SPDX-License-Identifier: MPL-2.0
#

: "${APCI_ALPAKA_ROOT?'APCI_ALPAKA_ROOT is not defined. Root directory of the alpaka project'}"
# shellcheck source=script/ci/utils/default.sh
source "${APCI_ALPAKA_ROOT}/script/ci/utils/default.sh"

if [[ "$APCI_OS_NAME" != "Linux" ]]; then
    exit_error "Install GCC script does not support Windows or MacOS"
fi

script_msg "Spack"

if ! command -v spack >/dev/null && [[ ! -d /opt/spack ]]; then
    echo_green "install spack"

    spack_package_dependencies=(
        file
        bzip2
        ca-certificates
        g++
        gcc
        gfortran
        git
        gzip
        lsb-release
        patch
        python3)
    lazy_apt_update
    quiet_run sudo DEBIAN_FRONTEND=noninteractive apt install -y "${spack_package_dependencies[@]}"

    git clone --depth=2 --branch=releases/v1.2 https://github.com/spack/spack.git /opt/spack
    # shellcheck source=/dev/null
    . /opt/spack/share/spack/setup-env.sh

    echo_run spack bootstrap now
    echo_run spack compiler find
fi

if ! spack mirror ls | grep -q gitlabci; then
    source /etc/os-release
    if [[ $NAME != "Ubuntu" ]]; then
        exit_error "Container image does not base on Ubuntu."
    fi

    _mirror_url="oci://registry.hzdr.de/crp/alpaka-spack-buildcache/cache-ubuntu${VERSION_ID//./}"
    echo_run spack mirror add gitlabci "${_mirror_url}"
fi

# TODO: This is hack. Installing GCC and CMake should be done in gcc.sh and cmake.sh. Only for testing
: "${APCI_DEVICE_COMPILER?'The device compiler must be specified'}"

parse_compiler_version "$APCI_DEVICE_COMPILER"

echo_run spack install --use-buildcache only "${compiler_name}@${compiler_version}"
echo_run spack install --use-buildcache only "cmake@${APCI_CMAKE}"
