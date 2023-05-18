#!/usr/bin/env python3
import sys
from fractions import Fraction

spectroscopic = "spdfghiklmnopqrtuvwxyz"
SPECTROSCOPIC = "SPDFGHIKLMNOPQRTUVWXYZ"
Global_Max_L = 6


def l_from_symbol(lchar):
    return spectroscopic.index(lchar)


def Symbol_from_L(Lint):
    return SPECTROSCOPIC[Lint]


def expand_config_string(string):
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


def form_l_list(l_str):
    outlist = []
    for c in expand_config_string(l_str):
        outlist.append(l_from_symbol(c))
    return outlist


def num_electrons(l_list):
    return len(l_list)


def max_L(l_list):
    return sum(l_list)


def min_L(l_list):
    # max - sum(rest) = 2*max - sum(all)
    temp = 2 * max(l_list) - sum(l_list)
    # This isn't quite right? or is it?
    return temp if temp > 0 else 0


def minmax_L(l_list):
    return min_L(l_list), max_L(l_list)


def max_twoS(l_list):
    n = num_electrons(l_list)
    return n


def min_twoS(l_list):
    n = num_electrons(l_list)
    return 0 if (n % 2) == 0 else 1


def minmax_twoS(l_list):
    return min_twoS(l_list), max_twoS(l_list)


def gJ(J, L, S):
    return (
        1.5 + (S * (S + 1.0) - L * (L + 1.0)) / (2.0 * J * (J + 1.0)) if J != 0 else 0
    )


def format_J(J):
    return str(int(J)) if J.is_integer() else str(int(2 * J)) + "/2"


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
        if J > L + 0.5 * twoS1:
            continue
        for twoS in range(twoS0, twoS1 + 2, 2):
            if J > L + 0.5 * twoS:
                continue
            M = twoS + 1
            Term = Symbol_from_L(L)
            g = gJ(J, L, 0.5 * twoS)
            print("{} {}_{}  g = {gfac:.3f}".format(M, Term, format_J(J), gfac=g))
        print()
