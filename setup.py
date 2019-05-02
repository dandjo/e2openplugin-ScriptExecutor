from distutils.core import setup

pkg = 'Extensions.ScriptExecutor'
setup (name = 'enigma2-plugin-extensions-scriptexecutor',
       version = '0.1',
       description = 'Executes scripts in /usr/scripts/*',
       packages = [pkg],
       package_dir = {pkg: 'plugin'}
      )
