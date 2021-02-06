"""A module that contain all possible exception definitions."""


class WorkerRunningError(RuntimeError):
    pass


class WorkerSetupCrawlerFail(TypeError):
    pass
