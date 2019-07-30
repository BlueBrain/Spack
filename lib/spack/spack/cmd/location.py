# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import argparse
import llnl.util.tty as tty

import spack.environment as ev
import spack.cmd
import spack.environment
import spack.paths
import spack.repo

description = "print out locations of packages and spack directories"
section = "basic"
level = "long"


def setup_parser(subparser):
    global directories
    directories = subparser.add_mutually_exclusive_group()

    directories.add_argument(
        '-m', '--module-dir', action='store_true',
        help="spack python module directory")
    directories.add_argument(
        '-r', '--spack-root', action='store_true',
        help="spack installation root")

    directories.add_argument(
        '-i', '--install-dir', action='store_true',
        help="install prefix for spec (spec need not be installed)")
    directories.add_argument(
        '-p', '--package-dir', action='store_true',
        help="directory enclosing a spec's package.py file")
    directories.add_argument(
        '-P', '--packages', action='store_true',
        help="top-level packages directory for Spack")
    directories.add_argument(
        '-s', '--stage-dir', action='store_true',
        help="stage directory for a spec")
    directories.add_argument(
        '-S', '--stages', action='store_true',
        help="top level stage directory")
    directories.add_argument(
        '-b', '--build-dir', action='store_true',
        help="checked out or expanded source directory for a spec "
             "(requires it to be staged first)")
    directories.add_argument(
        '-e', '--env', action='store',
        help="location of an environment managed by spack")

    subparser.add_argument(
        '--latest',
        help='use the last installed package when multiple ones match',
        action='store_true'
    )

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="spec of package to fetch directory for")


def location(parser, args):
    if args.module_dir:
        print(spack.paths.module_path)

    elif args.spack_root:
        print(spack.paths.prefix)

    elif args.env:
        path = spack.environment.root(args.env)
        if not os.path.isdir(path):
            tty.die("no such environment: '%s'" % args.env)
        print(path)

    elif args.packages:
        print(spack.repo.path.first_repo().root)

    elif args.stages:
        print(spack.paths.stage_path)

    else:
        specs = spack.cmd.parse_specs(args.spec)

        if not specs:
            tty.die("You must supply a spec.")
        if len(specs) != 1:
            tty.die("Too many specs.  Supply only one.")

        if args.install_dir:
            # install_dir command matches against installed specs.
            env = ev.get_env(args, 'location')
            spec = spack.cmd.disambiguate_spec(specs[0], env, args.latest)
            print(spec.prefix)

        else:
            spec = specs[0]

            if args.package_dir:
                # This one just needs the spec name.
                print(spack.repo.path.dirname_for_package_name(spec.name))

            else:
                # These versions need concretized specs.
                spec.concretize()
                pkg = spack.repo.get(spec)

                if args.stage_dir:
                    print(pkg.stage.path)

                else:  # args.build_dir is the default.
                    if not pkg.stage.expanded:
                        tty.die("Build directory does not exist yet. "
                                "Run this to create it:",
                                "spack stage " + " ".join(args.spec))
                    print(pkg.stage.source_path)
