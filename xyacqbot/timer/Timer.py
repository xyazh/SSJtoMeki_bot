import asyncio
import concurrent.futures
import inspect
import threading
import traceback
from datetime import datetime, timedelta
from ..xyazhServer.ConsoleMessage import ConsoleMessage


class Timer:
    _loop: asyncio.AbstractEventLoop | None = None
    _thread: threading.Thread | None = None
    _futures: set[concurrent.futures.Future] = set()
    _lock = threading.RLock()
    _ready = threading.Event()

    @classmethod
    def _thread_main(cls):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        cls._loop = loop
        cls._ready.set()
        try:
            loop.run_forever()
        finally:
            pending = [task for task in asyncio.all_tasks(
                loop) if not task.done()]
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(asyncio.gather(
                    *pending, return_exceptions=True))
            loop.close()
            with cls._lock:
                cls._loop = None
                cls._thread = None
                cls._futures.clear()
                cls._ready.clear()

    @classmethod
    def run(cls):
        with cls._lock:
            if cls._thread is not None and cls._thread.is_alive():
                return
            cls._ready.clear()
            cls._thread = threading.Thread(
                target=cls._thread_main, name="TimerLoop", daemon=True)
            cls._thread.start()
            ConsoleMessage.printC("[Timer] 定时器启动")
        cls._ready.wait()

    @classmethod
    def stop(cls, cancel_tasks: bool = True, wait: bool = True, timeout: int | float | None = 1):
        loop = cls._loop
        if loop is None:
            return
        futures: list[concurrent.futures.Future] = []
        if cancel_tasks:
            with cls._lock:
                futures = list(cls._futures)
            for future in futures:
                future.cancel()
            if wait:
                for future in futures:
                    try:
                        future.result(timeout=timeout)
                    except (concurrent.futures.CancelledError, concurrent.futures.TimeoutError):
                        pass
                    except Exception:
                        pass
        loop.call_soon_threadsafe(loop.stop)

    @classmethod
    def join(cls, timeout: int | float | None = None):
        thread = cls._thread
        if thread is not None:
            thread.join(timeout=timeout)

    @classmethod
    def _submit(cls, coro):
        cls.run()
        loop = cls._loop
        if loop is None:
            raise RuntimeError("Timer event loop is not ready")
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        with cls._lock:
            cls._futures.add(future)

        def _on_done(_):
            with cls._lock:
                cls._futures.discard(future)
        future.add_done_callback(_on_done)
        return future

    @staticmethod
    async def _run_func(func):
        try:
            result = func()
            if inspect.isawaitable(result):
                await result
        except Exception:
            traceback.print_exc()

    @classmethod
    def _build_decorator(cls, schedule_func, arg_value):
        def _decorator(func):
            schedule_func(func, arg_value)
            return func
        return _decorator

    @classmethod
    def setTimeout(cls, func_or_delay=None, delay: int | float | None = None):
        """
        延时执行一次

        直接调用:
            Timer.setTimeout(func, 3)
        装饰器:
            @Timer.setTimeout(3)
            def job():
                ...
        """

        def _schedule(func, wait):
            async def _job():
                await asyncio.sleep(max(float(wait), 0.0))
                await cls._run_func(func)
            return cls._submit(_job())
        if callable(func_or_delay):
            if delay is None:
                raise TypeError("setTimeout(func, delay) missing delay")
            return _schedule(func_or_delay, delay)
        if delay is None:
            delay = func_or_delay
        if delay is None:
            raise TypeError("setTimeout requires delay")
        ConsoleMessage.printC(f"[Timer] setTimeout {func_or_delay} {delay}")
        return cls._build_decorator(_schedule, delay)

    @classmethod
    def setInterval(cls, func_or_interval=None, interval: int | float | None = None):
        """
        周期执行

        直接调用:
            Timer.setInterval(func, 5)
        装饰器:
            @Timer.setInterval(5)
            def job():
                ...
        """
        def _schedule(func, wait):
            async def _job():
                interval_wait = max(float(wait), 0.0)
                while True:
                    await asyncio.sleep(interval_wait)
                    await cls._run_func(func)
            return cls._submit(_job())
        if callable(func_or_interval):
            if interval is None:
                raise TypeError("setInterval(func, interval) missing interval")
            return _schedule(func_or_interval, interval)
        if interval is None:
            interval = func_or_interval
        if interval is None:
            raise TypeError("setInterval requires interval")
        ConsoleMessage.printC(
            f"[Timer] setInterval {func_or_interval} {interval}")
        return cls._build_decorator(_schedule, interval)

    @classmethod
    def setTimeoutAt(cls, func_or_date=None, date: str | None = None):
        """
        在指定日期时间执行一次
        格式: 2026-03-01 12:30:00

        直接调用:
            Timer.setTimeoutAt(func, "2026-03-01 12:30:00")
        装饰器:
            @Timer.setTimeoutAt("2026-03-01 12:30:00")
            def job():
                ...
        """
        def _schedule(func, date_text):
            target = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")

            async def _job():
                now = datetime.now()
                wait = (target - now).total_seconds()
                if wait > 0:
                    await asyncio.sleep(wait)
                await cls._run_func(func)
            return cls._submit(_job())
        if callable(func_or_date):
            if date is None:
                raise TypeError("setTimeoutAt(func, date) missing date")
            return _schedule(func_or_date, date)
        if date is None:
            date = func_or_date
        if date is None:
            raise TypeError("setTimeoutAt requires date")
        ConsoleMessage.printC(f"[Timer] setTimeoutAt {func_or_date} {date}")
        return cls._build_decorator(_schedule, date)

    @classmethod
    def setDailyAt(cls, func_or_time=None, time_str: str | None = None):
        """
        每天固定时分秒执行
        格式: 12:30:00

        直接调用:
            Timer.setDailyAt(func, "12:30:00")
        装饰器:
            @Timer.setDailyAt("12:30:00")
            def job():
                ...
        """
        def _schedule(func, clock_text):
            datetime.strptime(clock_text, "%H:%M:%S")

            async def _job():
                while True:
                    now = datetime.now()
                    today_target = datetime.strptime(
                        now.strftime("%Y-%m-%d") + " " + clock_text,
                        "%Y-%m-%d %H:%M:%S",
                    )
                    if today_target <= now:
                        today_target += timedelta(days=1)
                    wait = (today_target - now).total_seconds()
                    await asyncio.sleep(wait)
                    await cls._run_func(func)
            return cls._submit(_job())
        if callable(func_or_time):
            if time_str is None:
                raise TypeError("setDailyAt(func, time_str) missing time_str")
            return _schedule(func_or_time, time_str)
        if time_str is None:
            time_str = func_or_time
        if time_str is None:
            raise TypeError("setDailyAt requires time_str")
        ConsoleMessage.printC(
            f"[Timer] setDailyAt {func_or_time} {time_str}")
        return cls._build_decorator(_schedule, time_str)


if __name__ == "__main__":
    print("timeout1")
    Timer.setTimeout(lambda: print("timeout1a"), 1)

    @Timer.setTimeout(2)
    def timeout2_job():
        print("timeout2a")

    @Timer.setInterval(1)
    def interval_job():
        print("interval")

    target_dt = datetime.now() + timedelta(seconds=5)
    target_date_str = target_dt.strftime("%Y-%m-%d %H:%M:%S")
    target_time_str = target_dt.strftime("%H:%M:%S")

    @Timer.setTimeoutAt(target_date_str)
    def timeout_at_job():
        print(f"timeoutAt -> {target_date_str}")

    @Timer.setDailyAt(target_time_str)
    def daily_at_job():
        print(f"dailyAt -> {target_time_str}")

    Timer.run()
    Timer.join(10)
    Timer.stop()
    Timer.join(1)
