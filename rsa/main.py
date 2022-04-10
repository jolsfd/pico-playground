import time
from machine import Pin, Timer

led = Pin(25, Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)

e_4096 = 17

d_4096 = 1122691313

n_4096 = 2385817433

m_4096 = 232347777

c_4096 = 234347945

e = 5

d = 77

n = 119

class RSA:
    def __init__(self) -> None:
        pass

    def encrypt(self, m: int, e: int, n: int) -> int:
        """
        Verschlüsseln einer Naricht m mit den Zahlen e und n.
        Rückgabe von -1, wenn Naricht zu lang.
        """
        if m < n:
            # c = m^e mod n
            c = pow(m, e, n)
            return c
        else:
            return -1

    def decrypt(self, c: int, d: int, n: int) -> int:
        """
        Entschlüsseln eines Geheimtextes c mit den Zahlen d und n.
        """
        # m = c^d mod n
        m = pow(c, d, n)
        return m

    def encrypt_text(self, m: str, e: int, n: int) -> List[int]:
        """
        Verschlüsseln eines Textes in beliebger Größe.
        """
        blocks = []
        bits = len(bin(n))-2
        num_chars = bits // 8 - 1

        for i in range(0, len(m), num_chars):
            chars = m[i : i + num_chars]

            # (1) Mit 0 auffüllen
            #chars = chars + "\0" * (num_chars - len(m))

            # (2) Zeichen in Binär
            binary = "".join(format(ord(i), "08b") for i in chars)

            # (3) Binär in Zahl
            num = int(binary, 2)

            # (4) Verschlüsseln der Zahl
            c = self.decrypt(num, e, n)

            blocks.append(c)

        return blocks

    def decrypt_text(self, blocks: List[int], d: int, n: int) -> str:
        """
        Entschlüsseln eines Textes.
        """
        bits = n.bit_length()
        format_string = f"0{bits}b"
        message_string = ""

        for c in blocks:
            # (1) Entschlüsseln
            m = self.encrypt(c, d, n)

            # (2) Zahl in Binärzahl
            binary = format(m, format_string)

            # (3) Binärzahl in Zeichen
            message_string += "".join(
                chr(int(binary[i : i + 8], 2)) for i in range(0, len(binary), 8)
            )  # generator

        return message_string
    
class Benchmark:
    def __init__(self, n: int, e: int, d: int, m: int, c: int, text: str) -> None:
        self.n = n
        self.e = e
        self.d = d
        self.m = m
        self.c = c
        self.text = text

        self.rsa = RSA()

    def bench_encrypt(self, n: int) -> float:
        start = time.time()
        for i in range(n):
            self.rsa.encrypt(self.m, self.e, self.n)

        return time.time() - start

    def bench_decrypt(self, n: int) -> float:
        start = time.time()
        for i in range(n):
            self.rsa.decrypt(self.c, self.d, self.n)

        return time.time() - start

    def bench_encrypt_text(self, n: int) -> float:
        start = time.time()
        for i in range(n):
            self.text_c = self.rsa.encrypt_text(self.text, self.d, self.n)

        return time.time() - start

    def bench_decrypt_text(self, n: int) -> float:
        start = time.time()
        for i in range(n):
            self.rsa.decrypt_text(self.text_c, self.d, self.n)

        return time.time() - start


if __name__ == "__main__":
    m = m_4096
    c = c_4096
    
    text = ""

    # Symsteminformationen
    print("RSA-Benchmark on Raspberry Pico")

    # Treiber Code
    count = 100000
    print(f"Running Benchmark {count} times...")
    bench = Benchmark(n_4096, e_4096, d_4096, m, c, text)

    time_decrypt = bench.bench_encrypt(count)
    print(f"{time_decrypt}s for encryption.")

    time_encrypt = bench.bench_decrypt(count)
    print(f"{time_encrypt}s for decryption.")