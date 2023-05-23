#!/usr/bin/env python3
import sys
from fractions import Fraction

spectroscopic = "spdfghiklmnopqrtuvwxyz"
SPECTROSCOPIC = "SPDFGHIKLMNOPQRTUVWXYZ"
Global_Max_L = 6


def l_from_symbol(lchar: str) -> int:
    """Converts a single-electron l symbol (s,p,d,...) to corresponding integer (0,1,2,...)"""
    return spectroscopic.index(lchar)


def Symbol_from_L(Lint: int) -> str:
    """Converts a multi-electron L quantum number (0,1,2,...) to corresponding symbol (S,P,D,...)"""
    return SPECTROSCOPIC[Lint]


def expand_config_string(string: str) -> str:
    """Converts an 'electron configuration string' from short to long form: e.g., sp3d -> spppd"""
    expanded_string = ""
    prev_char = ""
    pprev_char = ""

    for char in string:
        if char.isdigit():
            if prev_char.isdigit():
                expanded_string += pprev_char * (10 * int(prev_char) + int(char) - 1)
            else:
                expanded_string += prev_char * (int(char) - 1)
        else:
            expanded_string += char
        pprev_char = prev_char
        prev_char = char

    return expanded_string


def form_l_list(l_str: str) -> list:
    """Given an 'electron configuration string', forms a list of integer single-electron 'l's: e.g., sp3d -> [0,1,1,1,2]"""
    outlist = []
    for c in expand_config_string(l_str):
        outlist.append(l_from_symbol(c))
    return outlist


def num_electrons(l_list: list) -> int:
    """Given a list of single-electron l, returns number of electrons (simply size of the list)"""
    return len(l_list)


def max_L(l_list: list) -> int:
    """Given a list of single-electron l, returns maximum total L"""
    return sum(l_list)


def min_L(l_list: list) -> int:
    """Given a list of single-electron l, returns minimum* total L (*Not always: may return 0 when actual minimum is >0)"""
    # max - sum(rest) = 2*max - sum(all)
    temp = 2 * max(l_list) - sum(l_list)
    # This isn't quite right?
    return temp if temp > 0 else 0


def minmax_L(l_list: list) -> tuple[int, int]:
    """Given a list of single-electron l, returns [min_L, max_L]"""
    return min_L(l_list), max_L(l_list)


def max_twoS(l_list: list) -> int:
    """Given a list of single-electron l, returns maximum value of 2*S (total spin x2, integer)"""
    n = num_electrons(l_list)
    return n


def min_twoS(l_list: list) -> int:
    """Given a list of single-electron l, returns minimum value of 2*S (total spin x2, integer)"""
    n = num_electrons(l_list)
    return 0 if (n % 2) == 0 else 1


def minmax_twoS(l_list: list) -> tuple[int, int]:
    """Given a list of single-electron l, returns [min_2S, max_2S]"""
    return min_twoS(l_list), max_twoS(l_list)


def gJ(J: float, L: int, S: float) -> float:
    """Given angular momentums J, L, S, returns non-relativistic Lande g-factor"""
    return (
        1.5 + (S * (S + 1.0) - L * (L + 1.0)) / (2.0 * J * (J + 1.0)) if J != 0 else 0.0
    )


def format_J(J: float) -> str:
    """Formats J nicely for integer and half-integer"""
    return str(int(J)) if J.is_integer() else str(int(2 * J)) + "/2"


################################################################################

if __name__ == "__main__":
    input_J = -1.0
    input_string = ""
    if len(sys.argv) >= 3:
        input_J = float(Fraction(sys.argv[1]))
        input_string = sys.argv[2]
    else:
        print(
            "Please provide two arguments in form: J 'electron config'.\n"
            "e.g., '3/2 sp2d' for J=3/2, and config s,p^2,d"
        )
        sys.exit()

    l_list = form_l_list(input_string)
    J = input_J
    twoS0, twoS1 = minmax_twoS(l_list)
    L0, L1 = minmax_L(l_list)

    N = len(l_list)
    print("Number of electrons = ", N)
    print("J = ", format_J(J))
    print("Config. = ", input_string, " = ", expand_config_string(input_string))
    if (
        (N % 2 != 0 and J.is_integer())
        or (N % 2 == 0 and not J.is_integer())
        or J < 0
        or J > L1 + 0.5 * twoS1
    ):
        print("Invalid J for number of electrons")
        sys.exit()

    print()

    for L in range(L0, min(L1, Global_Max_L) + 1):
        if J > L + 0.5 * twoS1 or J < L - 0.5 * twoS1:
            continue
        for twoS in range(twoS0, twoS1 + 2, 2):
            if J > L + 0.5 * twoS or J < L - 0.5 * twoS:
                continue
            M = twoS + 1
            Term = Symbol_from_L(L)
            g = gJ(J, L, 0.5 * twoS)
            print("{} {}_{}  g = {gfac:.3f}".format(M, Term, format_J(J), gfac=g))
        print()
