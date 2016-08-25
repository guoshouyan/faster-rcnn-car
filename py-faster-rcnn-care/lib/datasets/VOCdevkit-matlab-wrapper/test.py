import subprocess

cmd = "octave test.m 'comp4-29636'"
print('Running:\n{}'.format(cmd))
status = subprocess.call(cmd, shell=True)
