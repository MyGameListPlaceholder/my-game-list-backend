from _typeshed import Incomplete
from io import StringIO

TextIO = StringIO

patchsysdict: Incomplete

class FDCapture:
    targetfd: Incomplete
    tmpfile: Incomplete
    def __init__(
        self, targetfd: Incomplete, tmpfile: Incomplete | None = ..., now: bool = ..., patchsys: bool = ...
    ) -> None: ...
    def start(self) -> None: ...
    def done(self) -> Incomplete: ...
    def writeorg(self, data: Incomplete) -> None: ...

def dupfile(
    f: Incomplete,
    mode: Incomplete | None = ...,
    buffering: int = ...,
    raising: bool = ...,
    encoding: Incomplete | None = ...,
) -> Incomplete: ...

class EncodedFile:
    encoding: Incomplete
    def __init__(self, _stream: Incomplete, encoding: Incomplete) -> None: ...
    def write(self, obj: Incomplete) -> None: ...
    def writelines(self, linelist: Incomplete) -> None: ...
    def __getattr__(self, name: Incomplete) -> Incomplete: ...

class Capture:
    def call(cls, func: Incomplete, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def reset(self) -> Incomplete: ...
    def suspend(self) -> Incomplete: ...

class StdCaptureFD(Capture):
    def __init__(
        self,
        out: bool = ...,
        err: bool = ...,
        mixed: bool = ...,
        in_: bool = ...,
        patchsys: bool = ...,
        now: bool = ...,
    ) -> None: ...
    def startall(self) -> None: ...
    def resume(self) -> None: ...
    def done(self, save: bool = ...) -> Incomplete: ...
    def readouterr(self) -> Incomplete: ...

class StdCapture(Capture):
    out: Incomplete
    err: Incomplete
    in_: Incomplete
    def __init__(
        self, out: bool = ..., err: bool = ..., in_: bool = ..., mixed: bool = ..., now: bool = ...
    ) -> None: ...
    def startall(self) -> None: ...
    def done(self, save: bool = ...) -> Incomplete: ...
    def resume(self) -> None: ...
    def readouterr(self) -> Incomplete: ...

class DontReadFromInput:
    def read(self, *args: Incomplete) -> None: ...
    readline = read
    readlines = read
    __iter__ = read
    def fileno(self) -> None: ...
    def isatty(self) -> Incomplete: ...
    def close(self) -> None: ...

devnullpath: Incomplete
