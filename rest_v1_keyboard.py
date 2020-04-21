import os
from glob import glob
import subprocess as sp
from pynput import keyboard

class PowerShell:
    # from scapy
    def __init__(self, coding, ):
        cmd = [self._where('PowerShell.exe'),
               "-NoLogo", "-NonInteractive",  # Do not print headers
               "-Command", "-"]  # Listen commands from stdin
        startupinfo = sp.STARTUPINFO()
        startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
        self.popen = sp.Popen(cmd, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT, startupinfo=startupinfo)
        self.coding = coding

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.popen.kill()

    def run(self, cmd, timeout=15):
        b_cmd = cmd.encode(encoding=self.coding)
        try:
            b_outs, errs = self.popen.communicate(b_cmd, timeout=timeout)
        except sp.TimeoutExpired:
            self.popen.kill()
            b_outs, errs = self.popen.communicate()
        outs = b_outs.decode(encoding=self.coding)
        return outs, errs

    @staticmethod
    def _where(filename, dirs=None, env="PATH"):
        """Find file in current dir, in deep_lookup cache or in system path"""
        if dirs is None:
            dirs = []
        if not isinstance(dirs, list):
            dirs = [dirs]
        if glob(filename):
            return filename
        paths = [os.curdir] + os.environ[env].split(os.path.pathsep) + dirs
        try:
            return next(os.path.normpath(match)
                        for path in paths
                        for match in glob(os.path.join(path, filename))
                        if match)
        except (StopIteration, RuntimeError):
            raise IOError("File not found: %s" % filename)


if __name__ == '__main__':
    # off display
    with PowerShell('GBK') as ps:
        ps.run('$brightness = 0 \n $delay = 5 \n \
            $myMonitor = Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods \n \
             $myMonitor.wmisetbrightness($delay, $brightness)')

    # keyboard exit function
    def on_release(key):
        exit = [keyboard.Key.space, keyboard.Key.space]
        if key in exit:
            # Stop listener
            return False
    # Collect events until released
    with keyboard.Listener(
            on_release=on_release) as listener:
        listener.join()

    # on display
    with PowerShell('GBK') as ps:
        ps.run('$brightness = 100 \n $delay = 5 \n \
            $myMonitor = Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods \n \
             $myMonitor.wmisetbrightness($delay, $brightness)')


