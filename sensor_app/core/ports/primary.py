from typing import Protocol

class UseCase(Protocol):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()
