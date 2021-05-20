class Task:
    def name(self): raise NotImplementedError

    def time_period(self):
        """
        Period of invocation `run` method in seconds
        :return ``int``
        """
        raise NotImplementedError

    def run(self): raise NotImplementedError

    def when_failed(self):
        """
        Method invoke if `run` method fails
        :return ``void``
        """
        pass

    def delay(self):
        """
        Delay of the first invocation `run` method in seconds
        :return ``int``
        """
        return 0
