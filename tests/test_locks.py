from pathlib import Path
from lib.locks import RWLock

def test_read_lock(tmp_path) -> None:
    lock = RWLock(tmp_path)
    lock.acquire_read()
    assert lock.read_lock.exists()
    lock.release_read()
    assert not lock.read_lock.exists()

def test_write_lock(tmp_path) -> None:
    lock = RWLock(tmp_path)
    lock.acquire_write()
    assert lock.write_lock.exists()
    lock.release_write()
    assert not lock.write_lock.exists()

def test_writer_priority(tmp_path) -> None:
    lock = RWLock(tmp_path)

    # Simulate a reader
    lock.acquire_read()

    # Writer should not acquire without wait=True
    try:
        lock.acquire_write(wait=False)
        assert False, "Expected failure"
    except RuntimeError:
        pass

    # Writer waiting should block new readers
    lock.release_read()
    lock.acquire_write(wait=True)
    assert lock.write_lock.exists()
    lock.release_write()

def test_force_clear(tmp_path) -> None:
    lock = RWLock(tmp_path)
    lock.acquire_read()
    lock.acquire_write(wait=False) if not lock.write_lock.exists() else None
    lock.force_clear()
    assert not lock.read_lock.exists()
    assert not lock.write_lock.exists()
    assert not lock.writer_waiting.exists()
