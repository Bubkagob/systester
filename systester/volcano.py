import time
import subprocess
import threading
import logging

logging.basicConfig(level=logging.NOTSET)


class Volcano(threading.Thread):
    def __init__(self, env_obj=None):
        super().__init__()
        self.proc = None
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("Volcano initialization")
        self.evt_launch_done = threading.Event()
        self.launch_ok = False
        self._stop_status = False
        self._env = env_obj
        self._wd = None

    def launch(self, wd):
        self._wd = wd
        self.start()
        self.evt_launch_done.wait()
        if not self.launch_ok:
            raise Exception("vc not started")

    def run(self):
        self._stop_status = False
        exec_name = self._env["corex"]
        lib_mask = self._env["lib"]

        try:
            self.proc = subprocess.Popen(
                [exec_name, "-lib", lib_mask],
                cwd=self._wd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            self.logger.warning("Error starting volcano:%s", str(e))
            self.launch_ok = False
            self.evt_launch_done.set()
            return

        time.sleep(0.5)
        ret_code = self.proc.poll()
        if ret_code is not None:
            self.launch_ok = False
            self.evt_launch_done.set()
            return

        self.launch_ok = True
        self.evt_launch_done.set()

        while not self._stop_status:
            self.logger.debug("vc(pid=%s) is still working", self.proc.pid)
            time.sleep(0.2)
        self.proc.terminate()

    def stop_me(self):
        self.logger.debug("vc(pid=%s) is stopping", self.proc.pid)
        self._stop_status = True
        try:
            self.proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            self.logger.warning("vc(pid=%s) stopping timeout", self.proc.pid)
            self.proc.kill()
            self.proc.communicate()
