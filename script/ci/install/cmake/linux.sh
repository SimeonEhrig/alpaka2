#!/usr/bin/env bash

#
# Copyright 2026 Simeon Ehrig
# SPDX-License-Identifier: MPL-2.0
#

if agc-manager -e "cmake@${APCI_CMAKE}"; then
    echo_green "use preinstalled cmake@${APCI_CMAKE}"

    APCI_CMAKE_BIN_PATH=$(agc-manager -b "cmake@${APCI_CMAKE}")/bin
    export APCI_CMAKE_BIN_PATH
else
    install_msg "cmake@${APCI_CMAKE}"

    _cmake_install_path="/opt/cmake/${APCI_CMAKE}"
    if [[ -d "${_cmake_install_path}" ]]; then
        if "${_cmake_install_path}/bin/cmake" --version; then
            echo_yellow "${_cmake_install_path} already exist. Skip install."
        else
            exit_error "${_cmake_install_path}/bin/cmake is not installed"
        fi
    else

        IFS="." read -r -a _cmake_ver_semantic <<<"${APCI_CMAKE}"
        _cmake_ver_major="${_cmake_ver_semantic[0]}"
        _cmake_ver_minor="${_cmake_ver_semantic[1]}"
        _cmake_pkg_file_name_base=cmake-${APCI_CMAKE}-linux-x86_64
        _cmake_pkg_file_name=${_cmake_pkg_file_name_base}.tar.gz

        _cmake_tmp_dir=$(mktemp -d)

        if ! RETRY_CONTINUE=ON ci_wget \
            https://cmake.org/files/v"${_cmake_ver_major}"."${_cmake_ver_minor}"/"${_cmake_pkg_file_name}" \
            "${_cmake_tmp_dir}/${_cmake_pkg_file_name}"; then
            echo_yellow "[WARNING]: use github.com mirror to download CMake"
            ci_wget "https://github.com/Kitware/CMake/releases/download/v${APCI_CMAKE}/${_cmake_pkg_file_name}" \
                "${_cmake_tmp_dir}/${_cmake_pkg_file_name}"
        fi

        echo_run tar -xzf "${_cmake_tmp_dir}/${_cmake_pkg_file_name}" -C "${_cmake_tmp_dir}"

        mkdir -p "${_cmake_install_path}"
        sudo mv "${_cmake_tmp_dir}/${_cmake_pkg_file_name_base}"/* "${_cmake_install_path}"
        sudo rm -rf "${_cmake_tmp_dir}"

        unset _cmake_ver_semantic \
            _cmake_ver_major \
            _cmake_ver_minor \
            _cmake_pkg_file_name_base \
            _cmake_pkg_file_name \
            _cmake_tmp_dir
    fi

    APCI_CMAKE_BIN_PATH="${_cmake_install_path}/bin"
    export APCI_CMAKE_BIN_PATH
    unset _cmake_install_path
fi
