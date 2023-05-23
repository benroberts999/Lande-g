# Lande-g

Prints possible non-relativistic term symbols, and corresponding non-relativistic g-factors for given electron configuration and (optionally) total angular momentum J.

e.g.

For electron configuraion $s^2d$ (ignore principle quantum number in config), and J=3/2:

**input:**

`./term.py s2d 3/2`

**output:**

```txt
Number of electrons =  3
Config. =  s2d  =  ssd
Parity: even
J =  3/2  =  1.5

2 D_3/2  g = 0.800
4 D_3/2  g = 1.200
```

J is optional; if not given, will print for all possible J's.
May sometimes print non-physical terms.

**input:**

`./term.py s2d`

**output:**

```txt
Number of electrons =  3
Config. =  s2d  =  ssd
Parity: even

2 D_3/2  g = 0.800
2 D_5/2  g = 1.200

4 D_1/2  g = 0.000
4 D_3/2  g = 1.200
4 D_5/2  g = 1.371
4 D_7/2  g = 1.429
```
