from typing import Generator
from __future__ import annotations
from pathlib import Path
import time
import os
from typing import Optional
from contextlib import contextmanager

READ_LOCK = ".read.lock"
WRITE_LOCK = ".write.lock"
WRITER_WAITING = ".writer_waiting.lock"


class RWLock:
    """
    Writer-priority read/write lock implemented using filesystem lock files.
    """

    def __init__(self, root: Path):
        self.root = root
        self.read_lock = root / READ_LOCK
        self.write_lock = root / WRITE_LOCK
        self.writer_waiting = root / WRITER_WAITING

    # ----------------------------
    # Utility helpers
    # ----------------------------
    def _exists(self, path: Path) -> bool:
        return path.exists()

    def _touch(self, path: Path) -> None:
        path.touch(exist_ok=True)

    def _remove(self, path: Path) -> None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    # ----------------------------
    # Read lock
    # ----------------------------
    def acquire_read(self, wait: bool = False, timeout: int = 30) -> None:
        start = time.time()

        while True:
            if not self._exists(self.write_lock) and not self._exists(self.writer_waiting):
                # Safe to read
                self._touch(self.read_lock)
                return

            if not wait:
                raise RuntimeError("Cannot acquire read lock: writer active or waiting")

            if time.time() - start > timeout:
                raise TimeoutError("Timed out waiting for read lock")

            time.sleep(0.1)

    def release_read(self) -> None:
        self._remove(self.read_lock)

    # ----------------------------
    # Write lock
    # ----------------------------
    def acquire_write(self, wait: bool = False, timeout: int = 30) -> None:
        start = time.time()
        self._touch(self.writer_waiting)

        while True:
            if not self._exists(self.read_lock) and not self._exists(self.write_lock):
                self._touch(self.write_lock)
                self._remove(self.writer_waiting)
                return

            if not wait:
                self._remove(self.writer_waiting)
                raise RuntimeError("Cannot acquire write lock: readers or writer active")

            if time.time() - start > timeout:
                self._remove(self.writer_waiting)
                raise TimeoutError("Timed out waiting for write lock")

            time.sleep(0.1)

    def release_write(self) -> None:
        self._remove(self.write_lock)

    # ----------------------------
    # Force clear
    # ----------------------------
    def force_clear(self) -> None:
        self._remove(self.read_lock)
        self._remove(self.write_lock)
        self._remove(self.writer_waiting)

    # ----------------------------
    # Context managers
    # ----------------------------
    @contextmanager
    def read_lock_cm(self, wait: bool = False, timeout: int = 30) -> Generator[None, None, None]:
        self.acquire_read(wait=wait, timeout=timeout)
        try:
            yield
        finally:
            self.release_read()

    @contextmanager
    def write_lock_cm(self, wait: bool = False, timeout: int = 30) -> Generator[None, None, None]:
        self.acquire_write(wait=wait, timeout=timeout)
        try:
            yield
        finally:
            self.release_write()
