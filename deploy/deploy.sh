#!/bin/bash -l

# This script assumes that the following variables are set in the environment:
#
# DEPLOYMENT_ROOT: path to deploy to

set -o errexit
set -o nounset

DEFAULT_DEPLOYMENT_ROOT="/gpfs/bbp.cscs.ch/apps/hpc/test/$(whoami)/deployment"
DEFAULT_DEPLOYMENT_DATA="/gpfs/bbp.cscs.ch/data/project/proj20/pramod_scratch/SPACK_DEPLOYMENT/download"
DEFAULT_DEPLOYMENT_DATE="$(date +%Y-%m-%d)"
DEFAULT_DEPLOYMENT_TYPE="install"

# Set variables to default. The user may override the following:
#
# * `DEPLOYMENT_TYPE` for the installation kind: mostly either "install" or
#    "pulls/####"
# * `DEPLOYMENT_ROOT` for the installation directory
# * `DEPLOYMENT_DATA` containing tarballs of proprietary software
# * `DEPLOYMENT_DATE` to force a date for the installation directory
#
# for the latter, see also the comment of `last_install_dir`
DEPLOYMENT_DATA=${DEPLOYMENT_DATA:-${DEFAULT_DEPLOYMENT_DATA}}
DEPLOYMENT_ROOT=${DEPLOYMENT_ROOT:-${DEFAULT_DEPLOYMENT_ROOT}}
DEPLOYMENT_TYPE=${DEPLOYMENT_TYPE:-${DEFAULT_DEPLOYMENT_TYPE}}

SPACK_SOURCE_MIRROR_DIR="${DEPLOYMENT_ROOT}/mirror/sources"
SPACK_BINARY_MIRROR_DIR="${DEPLOYMENT_ROOT}/mirror/binaries"
SPACK_PROPRIETARY_MIRROR_DIR="${DEPLOYMENT_ROOT}/mirror/proprietary"

export DEPLOYMENT_ROOT SPACK_BINARY_MIRROR_DIR SPACK_SOURCE_MIRROR_DIR

PATH=/usr/bin:${PATH}

export PATH

. ./deploy.lib

usage() {
    echo "usage: $0 [-cgil] stage..." 1>&2
    exit 1
}

do_copy=default
do_link=default
do_generate=default
do_install=default
while getopts "cgil" arg; do
    case "${arg}" in
        c)
            do_copy=yes
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_generate} = "default" ]] && do_generate=no
            [[ ${do_link} = "default" ]] && do_link=no
            ;;
        g)
            do_generate=yes
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_link} = "default" ]] && do_link=no
            [[ ${do_copy} = "default" ]] && do_copy=no
            ;;
        i)
            do_install=yes
            [[ ${do_generate} = "default" ]] && do_generate=no
            [[ ${do_link} = "default" ]] && do_link=no
            [[ ${do_copy} = "default" ]] && do_copy=no
            ;;
        l)
            do_link=yes
            [[ ${do_install} = "default" ]] && do_install=no
            [[ ${do_generate} = "default" ]] && do_generate=no
            [[ ${do_copy} = "default" ]] && do_copy=no
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND - 1))

if [[ "$@" = "all" ]]; then
    set -- ${stages}
else
    unknown=
    for what in "$@"; do
        if [[ ! ${spec_definitions[${what}]+_} ]]; then
            unknown="${unknown} ${what}"
        fi
    done
    if [[ -n "${unknown}" ]]; then
        echo "unknown stage(s):${unknown}"
        echo "allowed:          ${stages}"
        exit 1
    fi
fi

declare -A desired
for what in "$@"; do
    desired[${what}]=Yes
done

unset $(set +x; env | awk -F= '/^(PMI|SLURM)_/ {print $1}' | xargs)

[[ ${do_generate} != "no" ]] && generate_specs "$@"
for what in ${stages}; do
    if [[ ${desired[${what}]+_} && ${do_install} != "no" ]]; then
        install_specs ${what}
    fi
done

for what in ${stages}; do
    if [[ ${desired[${what}]+_} && ${do_link} = "yes" ]]; then
        set_latest ${what}
    fi
done

for what in ${stages}; do
    if [[ ${desired[${what}]+_} && ${do_copy} = "yes" ]]; then
        copy_configuration_user ${what}
    fi
done
