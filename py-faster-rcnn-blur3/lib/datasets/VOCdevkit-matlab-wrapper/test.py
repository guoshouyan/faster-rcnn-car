import subprocess

cmd = "octave test.m 'comp4-guo'"
print('Running:\n{}'.format(cmd))
status = subprocess.call(cmd, shell=True)
