# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Implementation details of the ``spack module`` command."""

import collections
import os.path
import shutil
import sys

from llnl.util import filesystem, lang, tty

import spack.cmd
import spack.modules
import spack.repo
import spack.modules.common

import spack.cmd.common.arguments as arguments

description = "manipulate module files"
section = "environment"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subparser_name')

    refresh_parser = sp.add_parser('refresh', help='regenerate module files')
    refresh_parser.add_argument(
        '--delete-tree',
        help='delete the module file tree before refresh',
        action='store_true'
    )
    refresh_parser.add_argument(
        '--upstream-modules',
        help='generate modules for packages installed upstream',
        action='store_true'
    )
    refresh_parser.add_argument(
        '--latest',
        help='use the last installed package when multiple ones match',
        action='store_true'
    )
    refresh_parser.add_argument(
        '--start-date',
        help='earliest date of installation [YYYY-MM-DD]'
    )
    refresh_parser.add_argument(
        '--end-date', help='latest date of installation [YYYY-MM-DD]'
    )
    arguments.add_common_arguments(
        refresh_parser, ['constraint', 'yes_to_all']
    )

    find_parser = sp.add_parser('find', help='find module files for packages')
    find_parser.add_argument(
        '--full-path',
        help='display full path to module file',
        action='store_true'
    )
    find_parser.add_argument(
        '--latest',
        help='use the last installed package when multiple ones match',
        action='store_true'
    )
    arguments.add_common_arguments(
        find_parser, ['constraint', 'recurse_dependencies']
    )

    rm_parser = sp.add_parser('rm', help='remove module files')
    arguments.add_common_arguments(
        rm_parser, ['constraint', 'yes_to_all']
    )

    loads_parser = sp.add_parser(
        'loads',
        help='prompt the list of modules associated with a constraint'
    )
    loads_parser.add_argument(
        '--latest',
        help='use the last installed package when multiple ones match',
        action='store_true'
    )
    add_loads_arguments(loads_parser)
    arguments.add_common_arguments(loads_parser, ['constraint'])

    return sp


def add_loads_arguments(subparser):
    subparser.add_argument(
        '--input-only', action='store_false', dest='shell',
        help='generate input for module command (instead of a shell script)'
    )
    subparser.add_argument(
        '-p', '--prefix', dest='prefix', default='',
        help='prepend to module names when issuing module load commands'
    )
    subparser.add_argument(
        '-x', '--exclude', dest='exclude', action='append', default=[],
        help="exclude package from output; may be specified multiple times"
    )
    arguments.add_common_arguments(
        subparser, ['recurse_dependencies']
    )


class MultipleSpecsMatch(Exception):
    """Raised when multiple specs match a constraint, in a context where
    this is not allowed.
    """


class NoSpecMatches(Exception):
    """Raised when no spec matches a constraint, in a context where
    this is not allowed.
    """


def one_spec_or_raise(specs):
    """Ensures exactly one spec has been selected, or raises the appropriate
    exception.
    """
    # Ensure a single spec matches the constraint
    if len(specs) == 0:
        raise NoSpecMatches()
    if len(specs) > 1:
        raise MultipleSpecsMatch()

    # Get the spec and module type
    return specs[0]


_missing_modules_warning = (
    "Modules have been omitted for one or more specs, either"
    " because they were blacklisted or because the spec is"
    " associated with a package that is installed upstream and"
    " that installation has not generated a module file. Rerun"
    " this command with debug output enabled for more details.")


def loads(module_type, specs, args, out=sys.stdout):
    """Prompt the list of modules associated with a list of specs"""

    if args.latest:
        def install_date(s):
            _, record = spack.store.db.query_by_spec_hash(s.dag_hash())
            return record.installation_time
        specs = sorted(specs, key=install_date, reverse=True)[:1]

    # Get a comprehensive list of specs
    if args.recurse_dependencies:
        specs_from_user_constraint = specs[:]
        specs = []
        # FIXME : during module file creation nodes seem to be visited
        # FIXME : multiple times even if cover='nodes' is given. This
        # FIXME : work around permits to get a unique list of spec anyhow.
        # FIXME : (same problem as in spack/modules.py)
        seen = set()
        seen_add = seen.add
        for spec in specs_from_user_constraint:
            specs.extend(
                [item for item in spec.traverse(order='post', cover='nodes')
                 if not (item in seen or seen_add(item))]
            )

    modules = list(
        (spec,
         spack.modules.common.get_module(
             module_type, spec, get_full_path=False, required=False))
        for spec in specs)

    module_commands = {
        'tcl': 'module load ',
        'lmod': 'module load ',
    }

    d = {
        'command': '' if not args.shell else module_commands[module_type],
        'prefix': args.prefix
    }

    exclude_set = set(args.exclude)
    load_template = '{comment}{exclude}{command}{prefix}{name}'
    for spec, mod in modules:
        if not mod:
            module_output_for_spec = (
                '## blacklisted or missing from upstream: {0}'.format(
                    spec.format()))
        else:
            d['exclude'] = '## ' if spec.name in exclude_set else ''
            d['comment'] = '' if not args.shell else '# {0}\n'.format(
                spec.format())
            d['name'] = mod
            module_output_for_spec = load_template.format(**d)
        out.write(module_output_for_spec)
        out.write('\n')

    if not all(mod for _, mod in modules):
        tty.warn(_missing_modules_warning)


def find(module_type, specs, args):
    """Returns the module file "use" name if there's a single match. Raises
    error messages otherwise.
    """
    if args.latest:
        def install_date(s):
            _, record = spack.store.db.query_by_spec_hash(s.dag_hash())
            return record.installation_time
        specs = sorted(specs, key=install_date, reverse=True)[:1]

    spec = one_spec_or_raise(specs)

    if spec.package.installed_upstream:
        module = spack.modules.common.upstream_module(spec, module_type)
        if module:
            print(module.path)
        return

    # Check if the module file is present
    def module_exists(spec):
        writer = spack.modules.module_types[module_type](spec)
        return os.path.isfile(writer.layout.filename)

    if args.recurse_dependencies:
        dependency_specs_to_retrieve = list(
            spec.traverse(root=False, order='post', cover='nodes',
                                 deptype=('link', 'run')))
    else:
        dependency_specs_to_retrieve = []

    try:
        modules = [
            spack.modules.common.get_module(
                module_type, spec, args.full_path, required=False)
            for spec in dependency_specs_to_retrieve]

        modules.append(
            spack.modules.common.get_module(
                module_type, spec, args.full_path, required=True))
    except spack.modules.common.ModuleNotFoundError as e:
        tty.die(e.message)

    if not all(modules):
        tty.warn(_missing_modules_warning)
    modules = list(x for x in modules if x)
    print(' '.join(modules))


def rm(module_type, specs, args):
    """Deletes the module files associated with every spec in specs, for every
    module type in module types.
    """

    module_cls = spack.modules.module_types[module_type]
    module_exist = lambda x: os.path.exists(module_cls(x).layout.filename)

    specs_with_modules = [spec for spec in specs if module_exist(spec)]

    modules = [module_cls(spec) for spec in specs_with_modules]

    if not modules:
        tty.die('No module file matches your query')

    # Ask for confirmation
    if not args.yes_to_all:
        msg = 'You are about to remove {0} module files for:\n'
        tty.msg(msg.format(module_type))
        spack.cmd.display_specs(specs_with_modules, long=True)
        print('')
        answer = tty.get_yes_or_no('Do you want to proceed?')
        if not answer:
            tty.die('Will not remove any module files')

    # Remove the module files
    for s in modules:
        s.remove()


def keep_latest(writers):
    """Keep the module writer with the most recently installed package
    """
    def install_date(w):
        _, record = spack.store.db.query_by_spec_hash(w.spec.dag_hash())
        return record.installation_time
    return sorted(writers, key=install_date, reverse=True)[0]


def refresh(module_type, specs, args):
    """Regenerates the module files for every spec in specs and every module
    type in module types.
    """

    # Prompt a message to the user about what is going to change
    if not specs:
        tty.msg('No package matches your query')
        return

    if not args.upstream_modules:
        specs = list(s for s in specs if not s.package.installed_upstream)

    if not args.yes_to_all:
        msg = 'You are about to regenerate {types} module files for:\n'
        tty.msg(msg.format(types=module_type))
        spack.cmd.display_specs(specs, long=True)
        print('')
        answer = tty.get_yes_or_no('Do you want to proceed?')
        if not answer:
            tty.die('Module file regeneration aborted.')

    # Cycle over the module types and regenerate module files

    cls = spack.modules.module_types[module_type]

    # Skip unknown packages.
    writers = [
        cls(spec) for spec in specs
        if spack.repo.path.exists(spec.name)]

    # Filter blacklisted packages early
    with spack.store.db.read_transaction():
        writers = [x for x in writers if not x.conf.blacklisted]

    # Detect name clashes in module files
    file2writer = collections.defaultdict(list)
    for item in writers:
        file2writer[item.layout.filename].append(item)

    if args.latest:
        writers = []
        with spack.store.db.read_transaction():
            for fn, matches in file2writer.items():
                writers.append(keep_latest(matches))
    elif len(file2writer) != len(writers):
        message = 'Name clashes detected in module files:\n'
        for filename, writer_list in file2writer.items():
            if len(writer_list) > 1:
                message += '\nfile: {0}\n'.format(filename)
                for x in writer_list:
                    message += 'spec: {0}\n'.format(x.spec.format())
        tty.error(message)
        tty.error('Operation aborted')
        raise SystemExit(1)

    if len(writers) == 0:
        msg = 'Nothing to be done for {0} module files.'
        tty.msg(msg.format(module_type))
        return

    # If we arrived here we have at least one writer
    module_type_root = writers[0].layout.dirname()
    spack.modules.common.generate_module_index(module_type_root, writers)
    # Proceed regenerating module files
    tty.msg('Regenerating {name} module files'.format(name=module_type))
    if os.path.isdir(module_type_root) and args.delete_tree:
        shutil.rmtree(module_type_root, ignore_errors=False)
    filesystem.mkdirp(module_type_root)
    with spack.store.db.read_transaction():
        for x in writers:
            try:
                x.write(overwrite=True)
            except Exception as e:
                tty.debug(e)
                msg = 'Could not write module file [{0}]'
                tty.warn(msg.format(x.layout.filename))
                tty.warn('\t--> {0} <--'.format(str(e)))


#: Dictionary populated with the list of sub-commands.
#: Each sub-command must be callable and accept 3 arguments:
#:
#:   - module_type: the type of module it refers to
#:   - specs : the list of specs to be processed
#:   - args : namespace containing the parsed command line arguments
callbacks = {
    'refresh': refresh,
    'rm': rm,
    'find': find,
    'loads': loads
}


def query_arguments(args):
    """Set up query arguments
    """
    # Qualifiers to be used when querying the db for specs
    constraint_qualifiers = {
        'refresh': {
            'installed': True,
            'known': True
        },
    }

    q_args = constraint_qualifiers.get(args.subparser_name, {})

    # Time window of installation
    for attribute in ('start_date', 'end_date'):
        date = getattr(args, attribute, None)
        if date:
            q_args[attribute] = lang.pretty_string_to_date(date)

    return q_args


def modules_cmd(parser, args, module_type, callbacks=callbacks):

    query_args = query_arguments(args)

    # Get the specs that match the query from the DB
    with spack.store.db.read_transaction():
        specs = args.specs(**query_args)

    try:

        callbacks[args.subparser_name](module_type, specs, args)

    except MultipleSpecsMatch:
        msg = "the constraint '{query}' matches multiple packages:\n"
        for s in specs:
            spec_fmt = '{hash:7} {name}{@version}{%compiler}'
            spec_fmt += '{compiler_flags}{variants}{arch=architecture}'
            msg += '\t' + s.cformat(spec_fmt) + '\n'
        tty.error(msg.format(query=args.constraint))
        tty.die('In this context exactly **one** match is needed: please specify your constraints better.')  # NOQA: ignore=E501

    except NoSpecMatches:
        msg = "the constraint '{query}' matches no package."
        tty.error(msg.format(query=args.constraint))
        tty.die('In this context exactly **one** match is needed: please specify your constraints better.')  # NOQA: ignore=E501
