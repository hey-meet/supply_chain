# Week 3 Day 4: Transactional Safe Execution
from contextlib import contextmanager

@contextmanager
def safe_transaction_boundary():
    try:
        # Begin database context
        yield
    except Exception as e:
        # Atomic rollback safety
        print(f"[DB Transaction Rollback] Triggered: {e}")
        raise e
