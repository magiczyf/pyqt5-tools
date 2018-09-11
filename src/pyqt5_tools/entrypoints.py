import os
import pathlib
import shutil
import subprocess
import sys

import click
import dotenv

import pyqt5_tools.badplugin
import pyqt5_tools.examplebuttonplugin


here = pathlib.Path(__file__).parent
example_path = str(
    pathlib.Path(pyqt5_tools.examplebuttonplugin.__file__).parent,
)
bad_path = str(
    pathlib.Path(pyqt5_tools.badplugin.__file__).parent,
)

def pyqt5toolsinstalluic():
    destination = here/'bin'
    destination.mkdir(parents=True, exist_ok=True)
    there = pathlib.Path(sys.executable).parent

    shutil.copy(str(there/'pyuic5.exe'), str(destination/'uic.exe'))


@click.command(
    context_settings={
        'ignore_unknown_options': True,
        'allow_extra_args': True,
    },
)
@click.pass_context
@click.option(
    '--widget-path',
    '-p',
    'widget_paths',
    help='Paths to be combined with PYQTDESIGNERPATH',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    multiple=True,
)
@click.option(
    '--example-widget-path',
    help='Include the path for the pyqt5-tools example button ({})'.format(
        example_path,
    ),
    is_flag=True,
)
@click.option(
    '--designer-help',
    help='Pass through to get Designer\'s --help',
    is_flag=True,
)
@click.option(
    '--test-exception-dialog',
    help='Raise an exception to check the exception dialog functionality.',
    is_flag=True,
)
def pyqt5designer(
        ctx,
        widget_paths,
        designer_help,
        example_widget_path,
        test_exception_dialog,
):
    dotenv.load_dotenv()
    extras = []
    widget_paths = list(widget_paths)

    if designer_help:
        extras.append('--help')

    if example_widget_path:
        widget_paths.append(example_path)

    if test_exception_dialog:
        widget_paths.append(bad_path)

    env = dict(os.environ)
    env['PYQTDESIGNERPATH'] = (
        os.pathsep.join((
            *widget_paths,
            env.get('PYQTDESIGNERPATH', ''),
            '',
        ))
    )
    env['PYTHONPATH'] = (
        os.pathsep.join((
            *sys.path,
            env.get('PYTHONPATH', ''),
            '',
        ))
    )

    for name in ('PYQTDESIGNERPATH', 'PYTHONPATH'):
        print('{}: {}'.format(name, env[name]))

    command = [
        str(here / 'designer.exe'),
        *extras,
        *ctx.args,
    ]

    return subprocess.call(command, env=env)


# def designer():
#     return subprocess.call([str(here/'designer.exe'), *sys.argv[1:]])
