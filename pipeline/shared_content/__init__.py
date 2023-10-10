from singleton_decorator import singleton


@singleton
class Status:
    def __init__(self):
        self.agent = ""
        self.status = ""


status = Status()
