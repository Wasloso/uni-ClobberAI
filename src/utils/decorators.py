import time
from functools import wraps
from typing import Callable, Optional, Union


def timeit(_func: Optional[Callable] = None, *, precision: int = 4):
    def decorator_timeit(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(
                f"Execution time of {func.__name__}: {end_time - start_time:.{precision}f} seconds"
            )
            return result

        return wrapper

    if _func is None:
        return decorator_timeit
    else:
        return decorator_timeit(_func)
