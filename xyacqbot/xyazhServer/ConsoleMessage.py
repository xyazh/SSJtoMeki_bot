import ctypes
import time
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# Console color constants (Windows console attributes)
FOREGROUND_BLACK = 0x00
FOREGROUND_DARK_BLUE = 0x01
FOREGROUND_DARK_GREEN = 0x02
FOREGROUND_DARK_CYAN = 0x03
FOREGROUND_DARK_RED = 0x04
FOREGROUND_DARK_MAGENTA = 0x05
FOREGROUND_DARK_YELLOW = 0x06
FOREGROUND_GRAY = 0x07
FOREGROUND_INTENSITY = 0x08

# Bright foreground colors (keep existing names compatible)
FOREGROUND_BLUE = FOREGROUND_DARK_BLUE | FOREGROUND_INTENSITY
FOREGROUND_GREEN = FOREGROUND_DARK_GREEN | FOREGROUND_INTENSITY
FOREGROUND_CYAN = FOREGROUND_DARK_CYAN | FOREGROUND_INTENSITY
FOREGROUND_RED = FOREGROUND_DARK_RED | FOREGROUND_INTENSITY
FOREGROUND_MAGENTA = FOREGROUND_DARK_MAGENTA | FOREGROUND_INTENSITY
FOREGROUND_YELLOW = FOREGROUND_DARK_YELLOW | FOREGROUND_INTENSITY
FOREGROUND_WHITE = FOREGROUND_GRAY | FOREGROUND_INTENSITY

BACKGROUND_BLACK = 0x00
BACKGROUND_DARK_BLUE = 0x10
BACKGROUND_DARK_GREEN = 0x20
BACKGROUND_DARK_CYAN = 0x30
BACKGROUND_DARK_RED = 0x40
BACKGROUND_DARK_MAGENTA = 0x50
BACKGROUND_DARK_YELLOW = 0x60
BACKGROUND_GRAY = 0x70
BACKGROUND_INTENSITY = 0x80

BACKGROUND_BLUE = BACKGROUND_DARK_BLUE | BACKGROUND_INTENSITY
BACKGROUND_GREEN = BACKGROUND_DARK_GREEN | BACKGROUND_INTENSITY
BACKGROUND_CYAN = BACKGROUND_DARK_CYAN | BACKGROUND_INTENSITY
BACKGROUND_RED = BACKGROUND_DARK_RED | BACKGROUND_INTENSITY
BACKGROUND_MAGENTA = BACKGROUND_DARK_MAGENTA | BACKGROUND_INTENSITY
BACKGROUND_YELLOW = BACKGROUND_DARK_YELLOW | BACKGROUND_INTENSITY
BACKGROUND_WHITE = BACKGROUND_GRAY | BACKGROUND_INTENSITY
class ConsoleMessage:
    DEBUG_LEVEL = 4

    @staticmethod
    def getTime():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def _normalize_sep(sep: str | None) -> str:
        if sep is None:
            return " "
        return str(sep)

    @staticmethod
    def _build_titles(titles: list[str] | None) -> str:
        if not titles:
            return ""
        return "".join(f"[{title}]" for title in titles)

    @staticmethod
    def _format(level: str, *msg, sep: str | None = " ", titles: list[str] | None = None) -> str:
        msg_text = ConsoleMessage._normalize_sep(sep).join(map(str, msg))
        title_text = ConsoleMessage._build_titles(titles)
        return f"[{ConsoleMessage.getTime()}]{title_text}[{level}]:{msg_text}"

    @staticmethod
    def printWarning(*msg, sep: str | None = " ", end="\n", titles: list[str] | None = None):
        if ConsoleMessage.DEBUG_LEVEL < 2:
            return
        text = ConsoleMessage._format(
            "WARNING", *msg, sep=sep, titles=titles)
        ConsoleMessage.P.printYellow(text, end=end)

    @staticmethod
    def printError(*msg, sep: str | None = " ", end="\n", titles: list[str] | None = None):
        if ConsoleMessage.DEBUG_LEVEL < 1:
            return
        text = ConsoleMessage._format("ERROR", *msg, sep=sep, titles=titles)
        ConsoleMessage.P.printRed(text, end=end)

    @staticmethod
    def printInfo(*msg, sep: str | None = " ", end="\n", titles: list[str] | None = None):
        if ConsoleMessage.DEBUG_LEVEL < 3:
            return
        text = ConsoleMessage._format("INFO", *msg, sep=sep, titles=titles)
        print(text, end=end)

    @staticmethod
    def printMsg(*msg, sep: str | None = " ", end="\n", titles: list[str] | None = None):
        text = ConsoleMessage._format("MSG", *msg, sep=sep, titles=titles)
        print(text, end=end)

    @staticmethod
    def printDebug(*msg, sep: str | None = " ", end="\n", titles: list[str] | None = None):
        if ConsoleMessage.DEBUG_LEVEL < 4:
            return
        text = ConsoleMessage._format("DEBUG", *msg, sep=sep, titles=titles)
        ConsoleMessage.P.printBlue(text, end=end)

    @staticmethod
    def print(*msg, sep: str | None = " ", end="\n", titles: list[str] | None = None):
        msg_text = ConsoleMessage._normalize_sep(sep).join(map(str, msg))
        title_text = ConsoleMessage._build_titles(titles)
        text = f"[{ConsoleMessage.getTime()}]{title_text}:{msg_text}"
        print(text, end=end)

    class P:
        _kernel32 = getattr(ctypes, "windll", None)
        std_out_handle = (
            _kernel32.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            if _kernel32 is not None
            else None
        )

        @staticmethod
        def set_cmd_text_color(color):
            if ConsoleMessage.P.std_out_handle is None:
                return False
            return ConsoleMessage.P._kernel32.kernel32.SetConsoleTextAttribute(
                ConsoleMessage.P.std_out_handle, color
            )

        @staticmethod
        def resetColor():
            ConsoleMessage.P.set_cmd_text_color(
                FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE
            )

        @staticmethod
        def _to_text(mess):
            if isinstance(mess, bytes):
                return str(mess, encoding="utf8", errors="replace")
            return str(mess)

        @staticmethod
        def printGreen(mess, end: str = "\n"):
            mess = ConsoleMessage.P._to_text(mess)
            ConsoleMessage.P.set_cmd_text_color(FOREGROUND_GREEN)
            sys.stdout.write(mess + end)
            ConsoleMessage.P.resetColor()

        @staticmethod
        def printRed(mess, end: str = "\n"):
            mess = ConsoleMessage.P._to_text(mess)
            ConsoleMessage.P.set_cmd_text_color(FOREGROUND_RED)
            sys.stdout.write(mess + end)
            ConsoleMessage.P.resetColor()

        @staticmethod
        def printYellow(mess, end: str = "\n"):
            mess = ConsoleMessage.P._to_text(mess)
            ConsoleMessage.P.set_cmd_text_color(FOREGROUND_YELLOW)
            sys.stdout.write(mess + end)
            ConsoleMessage.P.resetColor()

        @staticmethod
        def printBlue(mess, end: str = "\n"):
            mess = ConsoleMessage.P._to_text(mess)
            ConsoleMessage.P.set_cmd_text_color(FOREGROUND_BLUE)
            sys.stdout.write(mess + end)
            ConsoleMessage.P.resetColor()

