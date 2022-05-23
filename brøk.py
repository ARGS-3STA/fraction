"""bing chilling"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class Brøk:
    teller: int | Brøk
    nevner: int | Brøk

    def __post_init__(self):
        if self.nevner == 0:
            raise ValueError("Nevner kan ikke være 0.")
        if isinstance(self.teller, float):
            raise TypeError("Brøk godtar ikke desimaltall")
        if isinstance(self.nevner, float):
            raise TypeError("Brøk godtar ikke desimaltall")

    @staticmethod
    def fra_streng(streng: str) -> Brøk:
        kart = list(map(int, streng.split("/")))

        if len(kart) < 2:
            raise TypeError("Kan ikke konstruere brøken.")

        nåværende_brøk = Brøk(*kart[0:2])

        if not len(kart) > 2:
            return nåværende_brøk
        for verdi in kart[2:]:
            nåværende_brøk = Brøk(nåværende_brøk, verdi)

        return nåværende_brøk

    @staticmethod
    def til_felles_nevner(*brøker: Brøk | int) -> list[Brøk]:
        felles_nevner = 1
        for brøk in brøker:
            if isinstance(brøk, int):
                continue
            felles_nevner *= brøk.nevner

        res = []

        for brøk in brøker:
            if isinstance(brøk, int):
                brøk = Brøk(brøk, 1)
            res.append(
                Brøk(
                    brøk.teller * (felles_nevner // brøk.nevner),
                    brøk.nevner * (felles_nevner // brøk.nevner),
                )
            )

        return res

    def _flipp(self) -> Brøk:
        return Brøk(self.nevner, self.teller)

    def forkort(self) -> Brøk:
        n1, n2 = self.teller, self.nevner

        while n1 != n2:
            if n1 > n2:
                n1 -= n2
            else:
                n2 -= n1

        return Brøk(self.teller // n1, self.nevner // n1)

    def __add__(self, other: Brøk | int) -> Brøk:
        if isinstance(other, int):
            other = Brøk(other, 1)

        return Brøk(
            self.teller * other.nevner + other.teller * self.nevner,
            self.nevner * other.nevner,
        ).forkort()

    def __sub__(self, other: Brøk | int) -> Brøk:
        if isinstance(other, int):
            other = Brøk(other, 1)

        return Brøk(
            self.teller * other.nevner - other.teller * self.nevner,
            self.nevner * other.nevner,
        ).forkort()

    def __mul__(self, other: Brøk | int) -> Brøk:
        if isinstance(other, int):
            other = Brøk(other, 1)

        return Brøk(
            self.teller * other.teller,
            self.nevner * other.nevner,
        ).forkort()

    def __truediv__(self, other: Brøk | int) -> Brøk:
        if isinstance(other, int):
            other = Brøk(other, 1)

        return self * other._flipp()

    def __gt__(self, other: Brøk | int) -> bool:
        self, other = Brøk.til_felles_nevner(self, other)
        return self.teller > other.teller

    def __lt__(self, other: Brøk | int) -> bool:
        self, other = Brøk.til_felles_nevner(self, other)
        return self.teller < other.teller

    def __eq__(self, other: Brøk | int) -> bool:
        self, other = Brøk.til_felles_nevner(self, other)
        return self.teller == other.teller

    def __str__(self) -> str:
        return f"({self.teller}/{self.nevner})"

    def __float__(self) -> float:
        return self.teller / self.nevner


def main() -> None:
    import time

    start = time.perf_counter()

    a = Brøk.fra_streng("10/5/2/3")

    print(a)


if __name__ == "__main__":
    main()
