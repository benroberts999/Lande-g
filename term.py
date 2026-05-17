#!/usr/bin/env python3
import sys
from fractions import Fraction

spectroscopic = "spdfghiklmnopqrtuvwxyz"
SPECTROSCOPIC = "SPDFGHIKLMNOPQRTUVWXYZ"
Global_Max_L = 10


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


def print_term_each_J(l_list: list):
    """Given list of single-electron l: prints all possible terms + g-factors"""
    L0, L1 = minmax_L(l_list)

    N = len(l_list)

    print()
    for L in range(L0, min(L1, Global_Max_L) + 1):
        min_2S, max_2S = minmax_twoS(l_list)
        for twoS in range(min_2S, max_2S + 2, 2):
            min_2J = 2 * L - twoS
            if min_2J < 0:
                min_2J = twoS
            max_2J = 2 * L + twoS

            for twoJ in range(min_2J, max_2J + 2, 2):
                J = 0.5 * twoJ
                if J > L + 0.5 * twoS or J < L - 0.5 * twoS:
                    continue
                M = twoS + 1
                Term = Symbol_from_L(L)
                g = gJ(J, L, 0.5 * twoS)
                print("{} {}_{}  g = {gfac:.3f}".format(M, Term, format_J(J), gfac=g))
            print()
    return


def print_term_single_J(l_list: list, J: float):
    """Given list of single-electron l, and total J: prints all possible terms + g-factors"""
    twoS0, twoS1 = minmax_twoS(l_list)
    L0, L1 = minmax_L(l_list)

    N = len(l_list)
    print("J = ", format_J(J), " = ", J)
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
    return


def parse_term_symbol(s: str) -> tuple[int, int]:
    """Parse a term symbol like '3H' into (twoS, L). Multiplicity = 2S+1."""
    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] == "/"):
        i += 1
    if i == 0 or i >= len(s):
        raise ValueError(f"Invalid term symbol: {s}")
    M = int(Fraction(s[:i]))
    lchar = s[i].upper()
    if lchar not in SPECTROSCOPIC:
        raise ValueError(f"Invalid L symbol in term: {s}")
    L = SPECTROSCOPIC.index(lchar)
    twoS = M - 1
    return twoS, L


def print_term_each_J_for_term(l_list: list, twoS: int, L: int):
    """Given list of single-electron l, and a term (2S, L): prints all valid J states with g-factors"""
    twoS0, twoS1 = minmax_twoS(l_list)
    L0, L1 = minmax_L(l_list)

    M = twoS + 1
    Term = Symbol_from_L(L)
    print("Term: {} {}".format(M, Term))

    if L < L0 or L > L1 or twoS < twoS0 or twoS > twoS1 or (twoS - twoS0) % 2 != 0:
        print("Warning: term not allowed by this configuration")

    print()
    S = 0.5 * twoS
    min_2J = abs(2 * L - twoS)
    max_2J = 2 * L + twoS
    for twoJ in range(min_2J, max_2J + 2, 2):
        J = 0.5 * twoJ
        g = gJ(J, L, S)
        print("{} {}_{}  g = {gfac:.3f}".format(M, Term, format_J(J), gfac=g))
    return


################################################################################

if __name__ == "__main__":
    input_J = -1.0
    input_term = None
    config_string = ""
    do_each_J = False
    if len(sys.argv) == 2:
        do_each_J = True
    elif len(sys.argv) > 2:
        arg2 = sys.argv[2]
        # If contains a letter, treat as a term symbol (e.g. '3H'); else J
        if any(c.isalpha() for c in arg2):
            input_term = parse_term_symbol(arg2)
        else:
            input_J = float(Fraction(arg2))
    else:
        print(
            "Please provide two arguments in form: 'electron config' J_or_term.\n"
            "e.g., 'sp2d 3/2' for config s,p^2,d, and J=3/2\n"
            "e.g., 'sp2d 3H' for config s,p^2,d, and term 3H (lists all J)\n"
            "Second arg is optional; if none given, will print for all. (May print unphysical terms)"
        )
        sys.exit()
    config_string = sys.argv[1]

    l_list = form_l_list(config_string)

    even_parity = sum(l_list) % 2 == 0

    N = len(l_list)
    print("Number of electrons = ", N)
    print("Config. = ", config_string, " = ", expand_config_string(config_string))
    if even_parity:
        print("Parity: even")
    else:
        print("Parity: odd")

    if do_each_J:
        print_term_each_J(l_list)
    elif input_term is not None:
        twoS, L = input_term
        print_term_each_J_for_term(l_list, twoS, L)
    else:
        print_term_single_J(l_list, input_J)
