from Crypto.Hash import BLAKE2b

from .base import AttestationBase


class Blake2Attestation(AttestationBase):
    def __init__(self, secret: bytes, digest_bits=192):
        self._secret = secret
        self._digest_bits = digest_bits

    @staticmethod
    def load(path, *args, **kwargs):
        from pathlib import Path
        key = Path(path).read_bytes()
        return Blake2Attestation(key, *args, **kwargs)

    def _common(self, raw: bytes):
        return BLAKE2b.new(data=raw, digest_bits=self._digest_bits, key=self._secret)

    def _generate(self, raw: bytes) -> bytes:
        h = self._common(raw)
        return h.digest()

    def _verify(self, raw: bytes, quote: bytes):
        h = self._common(raw)
        h.verify(quote)


if __name__ == "__main__":
    from pathlib import Path
    from Crypto.Random import get_random_bytes

    secret = get_random_bytes(16)
    Path('hsecret.bin').write_bytes(secret)

    a = Blake2Attestation(secret)
