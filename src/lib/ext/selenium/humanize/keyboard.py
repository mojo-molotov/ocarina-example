"""Selenium utility that mimics human typing behavior when filling in form fields.

Instead of injecting text instantly, it types character by character with
variable delays, occasional typos drawn from AZERTY keyboard neighbors, and
two realistic correction strategies:

- Immediate correction: the wrong key is noticed at once and erased with a
  single backspace before continuing.
- Late correction: the user carries on typing for a few more characters before
  spotting the mistake, then backspaces all the way to the typo and retypes
  the affected sequence cleanly.

Typing rhythm is modeled with three regimes:
- Normal:      Gaussian-distributed delay centred on the wpm-derived base delay.
- Burst:       Unusually fast keystrokes, as fingers glide across adjacent keys.
- Hesitation:  A longer pause simulating a brief loss of focus or uncertainty.

Usage:

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome()
    driver.get("https://example.com/login")

    field = driver.find_element(By.ID, "username")
    humanized_send_keys(field, "instagram.enjoyer@mail.com", wpm=70, typo_rate=0.06)

"""

import random
import time
from typing import TYPE_CHECKING, TypedDict

from selenium.webdriver.common.keys import Keys

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class KeyboardConfig(TypedDict, total=False):
    """Typing configuration forwarded verbatim to humanized_send_keys.

    All fields are optional — any omitted key falls back to the default
    value defined in humanized_send_keys.

    Attributes:
        wpm:                       Target typing speed in words per minute.
        typo_rate:                 Probability of a typo on any given character.
        hesitation_rate:           Probability of a natural pause between keystrokes.
        burst_rate:                Probability of an unusually fast keystroke sequence.
        late_correction_rate:      Probability that a typo is corrected late rather
                                   than immediately.
        max_chars_before_noticing: Maximum characters typed after a typo before
                                   the user notices and corrects it.

    """

    wpm: int
    typo_rate: float
    hesitation_rate: float
    burst_rate: float
    late_correction_rate: float
    max_chars_before_noticing: int


_AZERTY_NEIGHBORS: dict[str, str] = {
    "a": "qzs",
    "z": "aeqs",
    "e": "rzd",
    "r": "etf",
    "t": "ryg",
    "y": "tuh",
    "u": "yij",
    "i": "uok",
    "o": "ipl",
    "p": "om",
    "q": "asz",
    "s": "qzaed",
    "d": "sefx",
    "f": "drgv",
    "g": "fthb",
    "h": "gynj",
    "j": "hukm",
    "k": "jil",
    "l": "kom",
    "w": "xsc",
    "x": "wcd",
    "c": "xvf",
    "v": "cbg",
    "b": "vnh",
    "n": "bmj",
    "m": "nk",
    "1": "2a",
    "2": "1ze3",
    "3": "2er4",
    "4": "3rt5",
    "5": "4ty6",
    "6": "5yu7",
    "7": "6ui8",
    "8": "7io9",
    "9": "8op0",
    "0": "9p",
}


def _is_typable(char: str) -> bool:
    """Return True if the character is eligible for a simulated typo.

    Whitespace of any kind is excluded — mistyping whitespace as whitespace
    produces an undetectable error that silently corrupts the final text.

    Args:
        char: Single character to test.

    Returns:
        True if the character has a known neighbor on the AZERTY layout
        and is not whitespace.

    """
    return char.lower() in _AZERTY_NEIGHBORS and not char.isspace()


def _pick_blind_length(text: str, typo_index: int, max_chars: int) -> int:
    """Sample how many characters the user types after a typo before noticing it.

    Bounded by both `max_chars` and the number of characters remaining in the
    string after the typo. Early detection is favored via a 1/k probability
    weight, so the user is more likely to catch the mistake after 1 character
    than after 5.

    Args:
        text:        Full text being typed.
        typo_index:  Index of the character where the typo occurred.
        max_chars:   Hard upper bound on how many characters can be missed.

    Returns:
        Number of characters to type blindly before triggering correction.
        Returns 0 if there are no characters left after the typo.

    """
    remaining = len(text) - typo_index - 1
    max_possible = min(max_chars, remaining)
    if max_possible <= 0:
        return 0

    return random.choices(  # noqa: S311
        range(1, max_possible + 1),
        weights=[1 / k for k in range(1, max_possible + 1)],
        k=1,
    )[0]


def _human_delay(base: float, burst_rate: float, hesitation_rate: float) -> None:
    """Sleep for a variable, human-like duration between two keystrokes.

    Three regimes are possible, sampled at random on each call:
    - Burst:       Very short delay (fingers gliding across adjacent keys).
    - Hesitation:  Long delay (brief loss of focus or moment of uncertainty).
    - Normal:      Gaussian-distributed delay centred on `base`, clipped at 10%
                   of `base` to avoid unrealistically short pauses.

    Args:
        base:             Base delay in seconds derived from the target wpm.
        burst_rate:       Probability of entering burst mode.
        hesitation_rate:  Probability of entering hesitation mode.

    """
    r = random.random()  # noqa: S311

    if r < burst_rate:
        delay = base * random.uniform(0.2, 0.5)  # noqa: S311
    elif r < burst_rate + hesitation_rate:
        delay = base * random.uniform(2.5, 5.0)  # noqa: S311
    else:
        delay = random.gauss(base, base * 0.3)
        delay = max(delay, base * 0.1)

    time.sleep(delay)


def humanized_send_keys(  # noqa: PLR0912, PLR0913, PLR0915
    element: WebElement,
    text: str,
    wpm: int = 80,
    typo_rate: float = 0.05,
    hesitation_rate: float = 0.08,
    burst_rate: float = 0.10,
    late_correction_rate: float = 0.6,
    max_chars_before_noticing: int = 6,
) -> None:
    """Type a string into a Selenium element in a human-like fashion.

    Simulates realistic typing behavior including variable keystroke delays,
    natural hesitations, bursts of fast typing, and two kinds of typo corrections:
    immediate (catch-and-fix right away) and late (keep typing for a few chars,
    then backspace back to the mistake and retype cleanly).

    Args:
        element:                   Target WebElement to type into.
        text:                      The string to type.
        wpm:                       Target typing speed in words per minute.
                                   One "word" is assumed to be 5 characters.
        typo_rate:                 Probability of making a typo on any given character.
                                   E.g. 0.05 means ~5% of keystrokes = wrong key.
        hesitation_rate:           Probability of a natural pause between two keystrokes
                                   (simulates thinking or losing focus briefly).
        burst_rate:                Probability of a burst — a short sequence of keys
                                   typed unusually fast, as fingers "glide" together.
        late_correction_rate:      Probability that a typo is corrected late (i.e. the
                                   user keeps typing some characters before noticing)
                                   vs. corrected immediately with a quick backspace.
        max_chars_before_noticing: Maximum number of characters that can be typed after
                                   a typo before the user "notices" and corrects it.
                                   Actual count is sampled from a 1/k distribution so
                                   early detection is more likely than late detection.

    Raises:
        ValueError: If any parameter is out of its valid range.

    """
    if wpm <= 0:
        msg = "wpm must be greater than 0"
        raise ValueError(msg)
    if not 0.0 <= typo_rate <= 1.0:
        msg = "typo_rate must be between 0.0 and 1.0"
        raise ValueError(msg)
    if not 0.0 <= hesitation_rate <= 1.0:
        msg = "hesitation_rate must be between 0.0 and 1.0"
        raise ValueError(msg)
    if not 0.0 <= burst_rate <= 1.0:
        msg = "burst_rate must be between 0.0 and 1.0"
        raise ValueError(msg)
    if burst_rate + hesitation_rate > 1.0:
        msg = "burst_rate + hesitation_rate must not exceed 1.0"
        raise ValueError(msg)
    if not 0.0 <= late_correction_rate <= 1.0:
        msg = "late_correction_rate must be between 0.0 and 1.0"
        raise ValueError(msg)
    if max_chars_before_noticing < 1:
        msg = "max_chars_before_noticing must be at least 1"
        raise ValueError(msg)

    base_delay = 60 / (wpm * 5)

    i = 0
    while i < len(text):
        char = text[i]

        if _is_typable(char) and random.random() < typo_rate:  # noqa: S311
            neighbors = _AZERTY_NEIGHBORS[char.lower()]
            typo_char = random.choice(neighbors)  # noqa: S311
            if char.isupper():
                typo_char = typo_char.upper()

            if random.random() < late_correction_rate:  # noqa: S311
                blind_chars = _pick_blind_length(text, i, max_chars_before_noticing)
                actually_typed = min(blind_chars, len(text) - i - 1)
                blind_sequence = text[i + 1 : i + 1 + actually_typed]

                element.send_keys(typo_char)

                for c in blind_sequence:
                    _human_delay(base_delay, burst_rate, hesitation_rate)
                    element.send_keys(c)

                time.sleep(random.uniform(0.3, 0.7))  # noqa: S311

                for _ in range(actually_typed + 1):
                    delay = random.uniform(0.04, 0.18)  # noqa: S311
                    if random.random() < 0.1:  # noqa: PLR2004, S311
                        delay += random.uniform(0.1, 0.3)  # noqa: S311
                    time.sleep(delay)
                    element.send_keys(Keys.BACKSPACE)

                time.sleep(random.uniform(0.2, 0.5))  # noqa: S311

                element.send_keys(char)

                for c in blind_sequence:
                    _human_delay(base_delay, burst_rate, hesitation_rate)
                    element.send_keys(c)

                i += actually_typed + 1
                _human_delay(base_delay, burst_rate, hesitation_rate)
                continue

            element.send_keys(typo_char + Keys.BACKSPACE + char)
            time.sleep(random.uniform(0.1, 0.4))  # noqa: S311

        else:
            element.send_keys(char)
            if i < len(text) - 1:
                _human_delay(base_delay, burst_rate, hesitation_rate)

        i += 1


def humanized_send_keys_with_config(
    element: WebElement,
    text: str,
    config: KeyboardConfig,
) -> None:
    """Type a string into a Selenium element using a KeyboardConfig mapping.

    Convenience wrapper around humanized_send_keys for callers that hold
    the typing configuration as a KeyboardConfig dict rather than as
    individual keyword arguments.

    Args:
        element: Target WebElement to type into.
        text:    The string to type.
        config:  Typing configuration. All fields are optional and fall back
                 to the defaults defined in humanized_send_keys.

    """
    humanized_send_keys(element, text, **config)
