from dataclasses import InitVar, dataclass, field
import datetime
from io import BytesIO
from logging import Logger
from math import floor, pi
from os import startfile
from pathlib import Path
from types import EllipsisType
from typing import Literal, override

UINT_64_MAX = 0xFFFF_FFFF_FFFF_FFFF
UINT_64_INT_OFFSET = 0x8000_0000_0000_0000
SALT = (3250700844, 0x43db74813eb90181, 23187203243, 8066144883, 0x3095263a168efaf0, 0x173414df45a40672)

if False:
    import random
    print(hex(random.randint(0, UINT_64_INT_OFFSET)))
    exit()


def seedify(s: str | bytes | int) -> int:
    if isinstance(s, int):
        return s % UINT_64_INT_OFFSET
    elif isinstance(s, str):
        try:
            return int(s, base=0) % UINT_64_INT_OFFSET
        except:
            s = bytes(s, "latin-1")
    b = s if isinstance(s, bytes) else bytes(s)
    h = len(b)
    for i in range(h):
        h = (h << i) ^ b[i]
    return ~(h & UINT_64_MAX) - UINT_64_INT_OFFSET


def clamp(value: float, min: float = 0, max: float = 1) -> float:
    return min if value < min else max if value > max else value


@dataclass(frozen=True, slots=True, kw_only=True)
class NoiseMachine:
    seed: int = 0
    scale: float = 1
    persistance: float = 1
    lacunarity: float = 1
    octaves: int = 1
    base_x_offset: int = 0
    base_y_offset: int = 0

    def random(self, x: int, y: int = 0) -> float:
        h = self.seed
        h ^= x * SALT[0]
        h ^= y * SALT[1]
        h ^= (h >> 29) * SALT[3]
        h *= SALT[2]
        h ^= (h >> 32) * SALT[2]
        h *= SALT[3]
        h ^= (h >> 28) * SALT[4]
        h *= SALT[5]
        h ^= (h >> 4) ^ (h >> 33) ^ (h >> 48) ^ SALT[5]
        return (h & UINT_64_MAX) / UINT_64_MAX

    @classmethod
    def inflate(cls, x: float) -> float:
        return (3 - 2 * x) * x * x

    @classmethod
    def smoothen(cls, a: float, b: float, c: float) -> float:
        return a + (b - a) * cls.inflate(c)

    def gradient(
        self, a: float, b: float, c: float, d: float, dx: float, dy: float
    ) -> float:
        if (
            self.smoothen is NoiseMachine.smoothen
            and self.inflate is NoiseMachine.inflate
        ):
            p, q = (3 - 2 * dx) * dx * dx, (3 - 2 * dy) * dy * dy
            return a + (b - a) * p + (c - a + (d - c - b + a) * p) * q
        return self.smoothen(self.smoothen(a, b, dx), self.smoothen(c, d, dx), dy)

    def perform_gradient(self, x: float, y: float) -> float:
        fx, fy = floor(x), floor(y)
        dx, dy = x - fx, y - fy
        a, b, c, d = (
            self.random(fx, fy),
            self.random(fx + 1, fy),
            self.random(fx, fy + 1),
            self.random(fx + 1, fy + 1),
        )
        return self.gradient(a, b, c, d, dx, dy)

    @classmethod
    def transform(cls, x: float) -> float:
        return normalize_float(x)

    def noise2d(
        self, x: float, y: float, x_offset: float = 0, y_offset: float = 0
    ) -> float:
        # want to start at full detail (at full scale) then each octave will add smaller details
        x = (x + x_offset + self.base_x_offset) / self.scale
        y = (y + y_offset + self.base_y_offset) / self.scale
        
        weight = 0 # = sum(persistance**o for o in range(octaves))
        value = 0
        amplitude = 1 # = persistance[0-1]**octave
        frequency = 1 # = lacunarity[1+]**octave

        for _ in range(self.octaves):
            weight += amplitude
            value += amplitude * self.perform_gradient(x / frequency, y / frequency)
            amplitude *= self.persistance
            frequency *= self.lacunarity
            
        return self.transform(value / weight)


ONE_THIRD = 1 / 3
FOUR_SEVENTHS = 4 / 7
ONE_SIXTH = 1 / 6
EIGHTY_THIRTEENTHS = 80/13





def Continentalness(seed: int = 0, x_offset: int = 0, y_offset: int = 0) -> NoiseMachine:
    return NoiseMachine(
        seed=seed,
        scale=66.87,
        persistance=0.56001511,
        lacunarity=3.69743099,
        octaves=4,
        base_x_offset=-seed & SALT[3] ^ 0x34ef0a + x_offset,
        base_y_offset=seed & SALT[4] ^ 0x34ef0a + y_offset,
    )
    



def smooth_periodic_fn(x: float) -> float:
    x = normalize_float(x)
    return (3-2*x)*x*x

def normalize_float(x: float) -> float:
    """Linearly flattens a float value to be in range [0,1]

    Args:
            x (float): any float number (-inf, inf)

    Returns:
            float: the flattened value [0,1]
    """
    if 0 <= x <= 1:
        return x
    return 1 - abs((x % 2) - 1)

INV_PI = 1/pi
def approx_sin(x: float) -> float:
    return 2*smooth_periodic_fn(x*INV_PI + 0.5)-1


def float_to_int8(v: float) -> int:
    return floor(normalize_float(v) * 0xFF)


THREE_ROOT_THREE = 3 * (3**0.5)

DEEP_OCEAN_LEVEL = 0.13
OCEAN_LEVEL = 0.43
COAST_LEVEL = 0.47
BEACH_LEVEL = 0.50
PLAINS_LEVEL = 0.88
ROCKY_LEVEL = 1.00



def float_to_hsv(x: float, mode: Literal['default', 'minecraft_colorize']='minecraft_colorize') -> tuple[float, float, float]:
    x = normalize_float(x)
    value = 0.5+0.5*(x-1)**2
    match mode:
        case 'minecraft_colorize':
            saturation = ONE_THIRD+2*ONE_THIRD*(x-1)**2
            if x<=DEEP_OCEAN_LEVEL:
                hue = 0.72
                saturation**=0.5
                value**=2
            elif x<=OCEAN_LEVEL:
                hue = 0.65
            elif x<=COAST_LEVEL:
                hue = 0.60
            elif x<=BEACH_LEVEL:
                hue = 0.22
                saturation*=0.5
                value=1
            elif x<=PLAINS_LEVEL:
                steepness = ((x-BEACH_LEVEL)/(PLAINS_LEVEL-BEACH_LEVEL))**2
                hue = 0.3
                saturation = 0.6 + 0.2*steepness
                value = 0.6 - 0.2*steepness
            elif x<=ROCKY_LEVEL:
                rockiness = ((x-PLAINS_LEVEL)/(ROCKY_LEVEL-PLAINS_LEVEL))**0.5
                mountainousness = rockiness**6
                hue = 0.095
                saturation = (0.8-0.8*rockiness)*(1-mountainousness)+(mountainousness)*(0.4-0.4*rockiness)
                value = (0.4-0.265*rockiness)*(1-mountainousness)+(mountainousness)*(0.9+0.1*rockiness)
            else:
                raise RuntimeError()
        case _:
            hue = 1 - 16 * (x - x * x) * (2 * x - 1) ** 2
            saturation = 0.5 + THREE_ROOT_THREE * (x * x * (3 - 2 * x) - x)
    return (hue, saturation, value)


def float_to_grayscale_bytes(v: float) -> bytes:
    return bytes(
        [float_to_int8(v),]
    )


SEXTANT_MAP = ((0, 1, 2), (1, 0, 2), (2, 0, 1), (2, 1, 0), (1, 2, 0), (0, 2, 1))


def hsv_to_rgba_bytes(
    hue: float, saturation: float, value: float, opacity: float = 1.0
) -> bytes:
    CHROMA = saturation * value  # chromaticity
    GRAY = value - CHROMA
    H = 6 * hue  # sextant angle
    X = CHROMA * normalize_float(H)  # adjacent color value
    r, g, b = ((CHROMA, X, 0)[i] for i in SEXTANT_MAP[floor(H)])
    return bytes(
        (
            float_to_int8(r + GRAY),
            float_to_int8(g + GRAY),
            float_to_int8(b + GRAY),
            float_to_int8(opacity),
        )
    )


def float_to_rgba_bytes(x: float, alpha: float = 1.0) -> bytes:
    return hsv_to_rgba_bytes(*float_to_hsv(x), opacity=alpha)


type MODE_GRAYSCALE = Literal["GRAYSCALE"]
type MODE_COLOR = Literal["COLOR"]
type MODE_RAW = Literal["RAW"]
type GENERATOR_MODE = MODE_COLOR | MODE_GRAYSCALE | MODE_RAW
type P_MODE = Literal["RGBA", "L", None]


def get_datetime_formatted() -> str:
    return datetime.datetime.now().isoformat("_").replace(":","-");

def generate_chunk(
    chunk_size: int = 16,
    chunk_x: float = 0,
    chunk_y: float = 0,
    nm: NoiseMachine = NoiseMachine(),
    mode: GENERATOR_MODE = "GRAYSCALE",
    logger: Logger = Logger.root,
) -> BytesIO:
    match mode:
        case "COLOR":
            TO_BYTES = float_to_rgba_bytes
        case "GRAYSCALE" | "RAW" | _:
            TO_BYTES = float_to_grayscale_bytes
    bytes = BytesIO()
    x_offset, y_offset = (chunk_x * chunk_size, chunk_y * chunk_size)
    for y in range(chunk_size):
        for x in range(chunk_size):
            v = nm.noise2d(x, y, x_offset=x_offset, y_offset=y_offset)
            b = TO_BYTES(v)
            """logger.info(
                "TO_BYTES(nm.noise2d(%d,%d,x_offset=%d,y_offset=%d) -> %0.4f) -> 0x%s" % (
                x,
                y,
                x_offset,
                y_offset,
                v,
                b.hex(),
            ))"""
            bytes.write(b)
        print(f"\r Generating y: {y+1}/{chunk_size}\t\t\t\r", end="")
    print()
    return bytes

DEFAULT_SAVE_PATH = Path.home().joinpath("Downloads")
def visualize(
    bytes: BytesIO,
    mode: GENERATOR_MODE,
    size: tuple[int, int] | int | EllipsisType = ...,
    save_as: Path | EllipsisType | str | None = ...,
) -> Path | None:
    from PIL import Image
    
    p_mode: P_MODE
    match mode:
        case "RAW":
            p_mode = None
            filetype = "bin"
        case "COLOR":
            p_mode = "RGBA"
            filetype = "png"
        case "GRAYSCALE" | _:
            p_mode = "L"
            filetype = "png"
    del mode

    if size is ...:
        size = int(bytes.__sizeof__() ** 0.5) >> (1 if p_mode == "RGBA" else 0)
    if isinstance(size, int):
        size = (size, size)
    byte_size = size[0] * size[1] * (4 if p_mode == "RGBA" else 1)
    if bytes.__sizeof__() > byte_size:
        bytes.truncate(byte_size)
    del byte_size
    if save_as is ...:
        save_as = get_datetime_formatted()
    if isinstance(save_as, str):
        save_as = DEFAULT_SAVE_PATH.joinpath(
            f"generated_{'data' if p_mode is None else 'image'}_{save_as}.{filetype}",
        )
    
    img = Image.frombuffer(p_mode or "L", size, bytes.getvalue())

    if save_as is not None:
        save_as.parent.mkdir(exist_ok=True, parents=True)
        save_as.touch()
        if p_mode is None:
            save_as.write_bytes(bytes.read1())
            img.show("Generated Data:")
        else:
            img.save(save_as)
            startfile(save_as, cwd=save_as.parent)
    else:
        img.show("Generated Data:")
    
    return save_as


TESTING_SEED = (
    seedify("This Is The Testing Seed")
    ^ seedify("Ryley just left to go take a shower wheee")
    ^ seedify(
        "'I just really want to go home...' she said, .. but no one answered back."
    )
    ^ seedify("'Should I stay or should I go?' -- The Clash")
    ^ seedify("""
        I may or may not have done too many of these ...
        (If 'these' refers to generations, seeds, time spent on revisions, etc...)
        """)
    ^ seedify("""
        1 + 1 is 2, but me + you is??
        Us hehehe
        """)
)



if __name__ == "__main__":
    continentalness = Continentalness(seed=TESTING_SEED)
    print(continentalness)
    CHUNK_SIZE = 512
    CHUNKS = (1,1)
    MODE: GENERATOR_MODE = "GRAYSCALE"
    FILENAME_BASE = get_datetime_formatted() + '_x%d_y%d'
    for cy in range(CHUNKS[1]):
        for cx in range(CHUNKS[0]):
            print("Saved to",visualize(
                generate_chunk(
                    CHUNK_SIZE,
                    cx,
                    cy,
                    continentalness,
                    mode = MODE,
                ),
                mode=MODE,
                size=CHUNK_SIZE,
                save_as=FILENAME_BASE%(cx,cy)
            ))
