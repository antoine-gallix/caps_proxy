from invoke import task
from pathlib import Path
import os


@task
def setup(ctx):
    """setup"""
    command = 'pip install -r requirements.txt'
    ctx.run(command)


@task
def tests(ctx):
    """run tests"""
    here = Path(__file__).resolve().parent
    os.environ['PYTHONPATH'] = str(here)
    command = 'py.test'
    ctx.run(command)


@task
def run(ctx, config):
    """run the application
    config : ['prod','dev']
    """
    # if the following import is called before installing requirements,
    # it would crash the file
    from caps_proxy import create_app
    app = create_app()
    if config == 'prod':
        app.run(host='0.0.0.0')
    elif config == 'dev':
        app.run(debug=True)


@task
def build_image(ctx, name='caps_proxy', version='dev'):
    """build docker image"""

    command = 'docker build -t {}:{} .'.format(name, version)
    ctx.run(command)


@task
def run_image(ctx, name='caps_proxy', version='dev'):
    """run docker image"""

    command = 'docker run --rm -p 5000:5000 {}:{}'.format(name, version)
    ctx.run(command)
