from enum import IntEnum
from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple
from math import sqrt, ceil, floor
import re
import numpy as np
from functools import cache


directions = {
    'U': (-1,  0),
    'L': (0, -1),
    'R': (0,  1),
    'D': (1,  0)
}


def sign(v: int) -> int:
    return v // abs(v)


def flip_dir(d, reverse):
    if not reverse:
        return d
    if d == 'U':
        return 'D'
    if d == 'L':
        return 'R'
    if d == 'D':
        return 'U'
    if d == 'R':
        return 'L'
    assert False


def solve(data: str) -> int:
    ops = []
    for line in data.splitlines():
        direction, count, _ = line.split(' ')
        ops.append((direction, int(count)))
    return solve_internal(ops)


code_to_dir = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}


def solve2(data: str) -> int:
    ops = []
    for line in data.splitlines():
        _, _, hashed = line.split(' ')
        direction = code_to_dir[hashed[7]]
        count = int(hashed[2:7], 16)
        ops.append((direction, count))
    return solve_internal(ops)


def solve_internal(ops):
    surface = 0
    pi, pj = 0, 0
    for k, (direction, cnt) in enumerate(ops):
        di, dj = directions[direction]
        i, j = pi + di * cnt, pj + dj * cnt
        s = (j - pj) * i
        surface += s
        pi, pj = i, j

    should_reverse = surface < 0
    if should_reverse:
        ops = list(reversed(ops))
    surface = 0
    pi, pj = 0, 0
    for k, (direction, cnt) in enumerate(ops):
        direction = flip_dir(direction, should_reverse)
        di, dj = directions[direction]
        prev_dir = flip_dir(ops[k - 1][0], should_reverse)
        next_dir = flip_dir(ops[(k + 1) % len(ops)][0], should_reverse)
        dic = 0
        djc = 0
        if direction == 'U' and prev_dir == 'R' and next_dir == 'L':
            dic = 1
        if direction == 'D' and prev_dir == 'L' and next_dir == 'R':
            dic = 1
        if direction == 'U' and prev_dir == 'L' and next_dir == 'R':
            dic = -1
        if direction == 'D' and prev_dir == 'R' and next_dir == 'L':
            dic = -1
        if direction == 'R' and prev_dir == 'D' and next_dir == 'U':
            djc = 1
        if direction == 'L' and prev_dir == 'U' and next_dir == 'D':
            djc = 1
        if direction == 'R' and prev_dir == 'U' and next_dir == 'D':
            djc = -1
        if direction == 'L' and prev_dir == 'D' and next_dir == 'U':
            djc = -1
        i, j = pi + di * (cnt + dic), pj + dj * (cnt + djc)

        s = (j - pj) * i
        surface += s
        # print(direction, (pi, pj), '->', (i, j), s, surface)

        pi, pj = i, j

    return surface


small_vector = ''
official_vector = ''


def run_tests():
    run_test(solve, [small_vector], 62)
    run_test(solve, [official_vector], 50746)
    run_test(solve2, [small_vector], 952408144115)
    run_test(solve2, [official_vector], 70086216556038)


small_vector = r'''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

official_vector = r'''L 3 (#33fba2)
U 5 (#1ff653)
L 5 (#0006a0)
U 5 (#648243)
R 6 (#666550)
U 7 (#648241)
L 6 (#31ec40)
U 8 (#3dc2f3)
L 3 (#839b40)
U 8 (#2332e3)
L 4 (#377d90)
U 8 (#8a5ad3)
L 6 (#377d92)
D 5 (#3208e3)
L 4 (#17b572)
D 8 (#408643)
L 6 (#4c2032)
D 3 (#1d96d3)
L 4 (#232562)
U 6 (#4a3503)
L 7 (#5076c2)
U 4 (#1cc1e3)
L 7 (#4481b2)
U 4 (#1bcef3)
L 9 (#138800)
U 3 (#211353)
L 2 (#34b290)
U 5 (#02c723)
L 4 (#6328c0)
D 10 (#76ae53)
L 3 (#230750)
D 2 (#3b34e3)
L 4 (#27c540)
D 4 (#931163)
L 7 (#078f72)
U 4 (#074ff3)
L 7 (#8fa702)
U 8 (#074ff1)
L 3 (#5ef972)
U 6 (#55ecc3)
L 4 (#1544a0)
U 3 (#256de3)
L 9 (#6ac6c0)
U 4 (#24c7a1)
L 6 (#22cae0)
U 3 (#0c4eb3)
L 3 (#0c6600)
U 9 (#977c93)
L 4 (#4716a0)
U 5 (#0c43d3)
R 10 (#429010)
U 5 (#112c81)
L 7 (#386202)
U 4 (#79c271)
L 3 (#386200)
U 3 (#147581)
L 9 (#164db0)
D 3 (#10aaa1)
L 5 (#4df340)
D 2 (#24c7a3)
L 7 (#0a8a50)
D 5 (#127ec3)
R 6 (#4bf3b2)
D 3 (#7eed73)
R 6 (#52eea2)
D 4 (#8d8dc3)
L 6 (#127cf2)
D 9 (#6c5cb1)
L 5 (#530dd2)
U 3 (#51a121)
L 5 (#1760e2)
U 2 (#39e1d1)
L 5 (#434682)
U 7 (#205543)
L 9 (#03f9f2)
D 4 (#486aa3)
L 3 (#3f2a42)
D 5 (#6f6b43)
L 6 (#1fb142)
D 3 (#6f6b41)
L 3 (#391ac2)
D 6 (#07e0e3)
R 3 (#1f9312)
D 3 (#19b523)
R 9 (#326a80)
D 5 (#52d763)
R 7 (#8918c0)
D 6 (#1ab263)
R 6 (#4899c2)
D 7 (#5dde03)
R 9 (#33fba0)
D 2 (#7e0bf3)
L 9 (#44ad80)
D 8 (#448023)
L 6 (#1c1ad0)
D 3 (#044f93)
L 3 (#471330)
D 8 (#3aad13)
L 4 (#3fbc50)
D 6 (#44f833)
L 3 (#1e92a0)
U 4 (#4d2a03)
L 9 (#22c7e0)
U 4 (#196d41)
L 4 (#44af50)
U 3 (#8bdfb1)
R 7 (#44af52)
U 3 (#4804e1)
R 6 (#00e920)
U 3 (#1a1ae1)
L 3 (#69edf0)
U 6 (#778b11)
L 5 (#430540)
U 7 (#642b81)
L 6 (#04a7d0)
U 4 (#417d51)
L 4 (#76c6e0)
U 3 (#404871)
L 4 (#1afc60)
U 2 (#5ab0d1)
L 5 (#3a69f0)
U 10 (#2c9331)
L 6 (#040ed0)
U 6 (#163481)
L 7 (#13a220)
U 5 (#62b1f1)
L 3 (#643c50)
U 4 (#62b1f3)
R 4 (#3efc20)
U 3 (#4579c1)
L 6 (#03fed0)
U 4 (#30dcb1)
L 6 (#093c90)
U 4 (#2714e3)
R 5 (#600820)
U 5 (#2714e1)
L 8 (#3018c0)
U 3 (#3377e1)
R 8 (#333a00)
U 4 (#0665b1)
R 3 (#073b92)
D 12 (#0ba311)
R 4 (#526382)
U 3 (#89fca1)
R 2 (#24afe2)
U 5 (#959fb3)
R 4 (#35bd32)
D 7 (#1dcd41)
R 7 (#75c192)
U 7 (#2d4911)
R 3 (#48bbf2)
U 5 (#2d4913)
R 10 (#2d9f62)
U 3 (#92d631)
R 4 (#25c092)
U 11 (#41ed91)
L 4 (#50bfe0)
U 5 (#413db1)
L 4 (#389910)
U 6 (#4efdb1)
L 6 (#4eaa52)
U 3 (#06cac1)
L 5 (#78a002)
D 9 (#06cac3)
L 5 (#0a29a2)
U 10 (#32f5c1)
L 4 (#358000)
U 7 (#1ddb41)
L 6 (#23bd30)
U 4 (#2bea51)
L 5 (#55aed0)
U 3 (#2bea53)
L 5 (#2287f0)
U 3 (#476591)
R 5 (#08e380)
U 2 (#0c72e1)
R 8 (#07bcd0)
U 5 (#0b3ef1)
L 3 (#8a32b0)
U 11 (#5884c1)
L 4 (#32f3b0)
D 11 (#16c381)
L 6 (#66a4a0)
U 3 (#1d9711)
L 4 (#079e00)
U 2 (#171d21)
L 3 (#03f9f0)
U 2 (#4747d1)
L 6 (#5ba020)
D 9 (#301811)
R 7 (#416c60)
D 8 (#269611)
L 7 (#33cdf2)
D 3 (#2cdb21)
L 4 (#682ae2)
U 5 (#1f18e1)
L 12 (#0caba2)
U 2 (#36ce31)
L 4 (#6a78a2)
U 7 (#43a111)
R 4 (#6a78a0)
U 3 (#599d11)
R 4 (#7f57b0)
U 2 (#5234e3)
R 8 (#801470)
U 4 (#21a943)
R 6 (#43c930)
U 2 (#3d3c73)
R 3 (#60e952)
U 9 (#282843)
R 3 (#62f452)
U 4 (#075d53)
R 5 (#7163f0)
U 3 (#530583)
R 3 (#290100)
D 6 (#3f94e3)
R 8 (#290102)
D 3 (#4a9b53)
R 4 (#2d79f0)
D 9 (#1bb753)
R 5 (#06e672)
U 8 (#1d8213)
R 7 (#34c6a2)
U 7 (#5808f3)
R 5 (#3e3ad2)
U 12 (#090c83)
R 3 (#79e7e0)
U 3 (#159043)
R 7 (#160c30)
D 7 (#622921)
R 8 (#31d690)
D 8 (#1ea571)
R 3 (#6e86d0)
U 6 (#031e71)
R 3 (#901d10)
U 4 (#038011)
R 12 (#3cb0a0)
U 4 (#14c7e1)
L 7 (#4ea712)
U 10 (#03f931)
R 7 (#39f882)
U 6 (#7ee061)
R 6 (#442e22)
D 10 (#2bf951)
R 2 (#448f60)
D 4 (#413bf1)
R 3 (#4bb5a0)
U 4 (#36e453)
R 2 (#6984f0)
U 10 (#4e53b3)
R 4 (#4adc40)
D 5 (#7c4253)
R 6 (#4adc42)
D 3 (#09fae3)
R 2 (#354170)
D 10 (#78a7f3)
R 3 (#428720)
U 4 (#0826a3)
R 5 (#6e5e30)
U 4 (#628873)
R 3 (#087050)
U 10 (#50de93)
R 4 (#24a8b0)
D 8 (#391e83)
R 4 (#22f4e2)
D 5 (#6cc6c3)
L 4 (#30e662)
D 11 (#1135d1)
R 5 (#636062)
U 7 (#586bf1)
R 3 (#4b54f2)
U 10 (#2a4161)
R 4 (#555d02)
D 5 (#479501)
R 3 (#361622)
D 9 (#0c4471)
R 6 (#75f512)
D 5 (#511ef1)
R 7 (#8bff32)
D 6 (#034163)
R 4 (#248e92)
D 3 (#89acb3)
R 7 (#081222)
D 6 (#24baf3)
R 3 (#52c0e2)
D 4 (#43e083)
R 4 (#3ad2a2)
U 6 (#689b71)
R 8 (#584f22)
U 6 (#7b48d3)
R 2 (#1a0840)
U 3 (#1ead13)
R 6 (#77f8c0)
U 9 (#1ead11)
R 6 (#5bf3c0)
U 4 (#30a4a3)
R 2 (#945222)
U 6 (#25a563)
R 3 (#197882)
U 4 (#381af3)
R 4 (#1ba310)
D 8 (#3759d3)
R 8 (#41ca50)
D 3 (#5711e3)
R 3 (#6c2800)
D 6 (#3710b3)
R 4 (#035c90)
U 6 (#459c01)
R 9 (#44da60)
U 4 (#6373d1)
R 5 (#238490)
D 5 (#1c6c91)
R 3 (#3a59f0)
D 8 (#2db993)
R 2 (#52adc0)
D 3 (#6c2d93)
R 5 (#52adc2)
U 11 (#3c2903)
R 5 (#363f00)
U 5 (#20c4a3)
R 4 (#313ed2)
U 2 (#26cd03)
R 4 (#417022)
U 8 (#60ec73)
R 5 (#72aef0)
U 4 (#2646e3)
R 4 (#4b1240)
U 8 (#2f4143)
L 7 (#555e20)
U 7 (#335fc3)
R 7 (#62b4f0)
U 5 (#4c3a13)
R 3 (#2146f0)
U 4 (#536ff3)
R 9 (#426922)
D 8 (#3fdbe3)
R 7 (#582a52)
D 3 (#487023)
R 8 (#31a302)
D 6 (#487021)
R 2 (#3ba5a2)
D 11 (#416e53)
R 6 (#1c9032)
D 4 (#442c83)
L 4 (#140b10)
D 5 (#107a03)
L 3 (#7d98d0)
U 5 (#2b15b3)
L 6 (#69ec72)
D 3 (#1cb1b3)
L 4 (#27b772)
D 3 (#366713)
R 2 (#36cc30)
D 2 (#1e5673)
R 10 (#3bc850)
D 2 (#561f11)
R 5 (#247cd0)
D 3 (#561f13)
L 4 (#5c4430)
D 11 (#08e5e3)
L 2 (#15a080)
D 3 (#2f59c1)
R 4 (#1a7fe0)
D 3 (#26bd21)
R 9 (#1a7fe2)
D 5 (#4e1951)
R 4 (#48ddf0)
D 6 (#06b7e3)
R 7 (#10b390)
D 2 (#890e13)
R 4 (#10b392)
D 2 (#146a43)
R 4 (#501670)
D 10 (#23d621)
R 3 (#0cf3c0)
D 3 (#3b86a1)
L 2 (#3db5e0)
D 4 (#005de1)
L 11 (#3623c0)
D 5 (#1df161)
L 2 (#47f230)
D 5 (#7c2bf1)
R 5 (#5222c0)
D 4 (#0243c1)
L 9 (#0d3390)
D 6 (#5c4971)
R 9 (#50dda0)
D 3 (#88be83)
R 4 (#2c5110)
U 4 (#40f933)
R 2 (#606a00)
U 9 (#6ccd63)
R 4 (#2d4cd0)
D 4 (#12c131)
R 3 (#356b10)
D 9 (#5a7701)
R 6 (#7cc460)
U 9 (#053501)
R 5 (#1c6860)
D 2 (#5932b1)
R 6 (#829ef2)
U 9 (#197471)
R 5 (#4bf8e2)
D 3 (#5170c1)
R 5 (#46bc80)
D 8 (#7cba21)
L 5 (#4de0b2)
D 7 (#066181)
R 9 (#879d82)
U 4 (#066183)
R 4 (#895762)
U 8 (#030f21)
L 4 (#601432)
U 6 (#01c761)
R 6 (#175150)
U 3 (#1e5d11)
R 10 (#0cfb00)
U 3 (#3fecf1)
L 5 (#0cfb02)
U 3 (#520e71)
L 5 (#175152)
U 8 (#6ca291)
R 5 (#4e79c2)
U 3 (#501701)
R 5 (#5e5f22)
U 3 (#14b3d1)
L 8 (#5e5f20)
D 3 (#5eb7a1)
L 5 (#4bf7c2)
D 9 (#16dff1)
L 2 (#3c49d0)
D 5 (#63e7e1)
L 3 (#520800)
U 6 (#8a6bb1)
L 4 (#2656a0)
U 8 (#550813)
L 5 (#67bc90)
U 3 (#301783)
L 3 (#279ca0)
U 3 (#4a17c3)
R 3 (#4dbe50)
U 4 (#7a2f41)
R 8 (#588e40)
U 5 (#56c093)
R 3 (#3a0e20)
U 4 (#428af3)
L 11 (#420100)
U 4 (#8b20e1)
L 11 (#2eb8c0)
U 6 (#2d7951)
L 4 (#28e890)
U 5 (#44ef81)
L 4 (#262a40)
D 7 (#44ef83)
L 5 (#4e8760)
D 3 (#112951)
L 5 (#3527e0)
U 5 (#3c5341)
L 4 (#7a4540)
U 5 (#214271)
L 6 (#282a10)
U 6 (#439991)
R 9 (#14ea70)
U 8 (#4134a1)
R 4 (#399260)
U 8 (#553401)
R 5 (#724270)
U 4 (#0a6113)
R 5 (#95ecb0)
D 5 (#0a6111)
R 7 (#63fff0)
D 3 (#3cfe01)
R 3 (#332aa2)
D 4 (#34fa61)
R 6 (#706922)
U 5 (#27d4b1)
R 2 (#23f172)
U 7 (#389de1)
R 3 (#34d942)
U 4 (#5e2491)
R 4 (#431c12)
U 5 (#0a4aa1)
R 4 (#48ff92)
U 10 (#0b6491)
R 6 (#51f202)
U 2 (#097e43)
R 6 (#334d02)
U 8 (#4977d3)
R 9 (#2f9ee2)
D 8 (#5619e3)
R 5 (#02f8a2)
U 4 (#3f4431)
R 7 (#20a7c2)
D 6 (#2fb691)
R 6 (#20a7c0)
D 6 (#3a1531)
R 5 (#076272)
D 3 (#250c41)
R 4 (#754080)
D 5 (#03f991)
R 3 (#351350)
D 9 (#4ab431)
L 4 (#14f6e2)
D 8 (#1a6061)
L 3 (#753a82)
D 5 (#550071)
R 5 (#202272)
D 5 (#438361)
R 6 (#365e12)
D 4 (#3203f3)
R 8 (#172d52)
D 6 (#5b9673)
L 2 (#10fa22)
D 4 (#2081b3)
L 2 (#10fa20)
D 4 (#4852e3)
L 10 (#172d50)
D 2 (#302f43)
L 10 (#3de852)
D 4 (#1f91a1)
R 7 (#610462)
D 2 (#4871b1)
R 5 (#12df82)
D 4 (#845931)
R 2 (#572182)
D 7 (#577d11)
R 8 (#009db2)
D 4 (#47c451)
L 6 (#55a262)
D 7 (#0fdf51)
L 3 (#17d632)
D 9 (#553f81)
L 4 (#517a32)
U 7 (#27aaa1)
L 2 (#236612)
U 9 (#754401)
L 3 (#5c45f2)
D 6 (#002a43)
L 3 (#7a76c2)
D 3 (#275c13)
L 10 (#1d92b2)
D 4 (#2574a3)
L 3 (#88e710)
D 5 (#4feac3)
L 8 (#1183a0)
D 9 (#304733)
L 3 (#1347f2)
D 5 (#458e01)
L 6 (#535682)
D 3 (#458e03)
L 4 (#33cc42)
D 3 (#3cc2b3)
L 6 (#1d92b0)
D 3 (#1b6883)
L 4 (#439cb2)
D 6 (#5381c3)
L 8 (#35de52)
D 5 (#287503)
L 5 (#0ac662)
D 8 (#110591)
L 3 (#6d3d02)
D 6 (#5d5c01)
L 4 (#166182)
D 9 (#46ca71)
R 6 (#217612)
D 7 (#529671)
L 8 (#1ea022)
D 5 (#1d2df1)
R 5 (#0df5f0)
D 7 (#4f0551)
R 3 (#69ebf0)
D 3 (#5b2421)
L 6 (#77e1e2)
D 5 (#174db1)
L 10 (#4cea52)
D 6 (#4bdc43)
L 5 (#37fd22)
U 9 (#92c8d3)
R 7 (#05f212)
U 4 (#1177f1)
L 3 (#5b9162)
U 3 (#485621)
L 9 (#135642)
U 4 (#4802e1)
R 5 (#360aa2)
U 5 (#491861)
R 7 (#783872)
U 4 (#2154d1)
L 7 (#083e92)
U 6 (#3f1521)
L 8 (#43af32)
U 5 (#7ff2f3)
L 6 (#2c3072)
U 2 (#366a03)
L 6 (#0725f2)
D 4 (#26a1f3)
L 9 (#7a76f2)
U 4 (#4fa793)
L 5 (#482da2)
D 4 (#18bb91)
L 5 (#155a62)
D 4 (#7d9b21)
L 2 (#488ef2)
U 4 (#9656b3)
L 6 (#193ce2)
U 4 (#4fa791)
L 6 (#02c4e2)
D 11 (#535e93)
L 5 (#010b42)
D 7 (#1af5d3)
L 6 (#80a212)
D 6 (#497393)
L 2 (#3c86b2)
D 7 (#5d6823)
L 3 (#189a02)
D 8 (#5cd783)
L 8 (#0e62c2)
D 4 (#90bc33)
L 9 (#17c7c2)
D 3 (#188773)
R 8 (#4a09e2)
D 5 (#16e571)
R 7 (#688e12)
D 3 (#5bb031)
R 2 (#43c9e0)
D 3 (#493e01)
R 11 (#2a55e0)
D 3 (#2e8a31)
R 2 (#6e1fc2)
D 5 (#5f5071)
R 2 (#2801f2)
D 4 (#19d501)
L 7 (#241b62)
U 8 (#847db1)
L 7 (#3170d2)
D 3 (#312c53)
R 4 (#2bee22)
D 12 (#5d3bc3)
L 4 (#242f32)
D 3 (#7ec591)
L 4 (#3b8892)
U 4 (#0fa281)
L 2 (#226c32)
U 8 (#847db3)
L 4 (#2fc5f2)
U 6 (#7f1163)
L 3 (#2f8f32)
D 8 (#02d8f3)
L 5 (#883e72)
D 3 (#230943)
R 7 (#520692)
D 9 (#2697e3)
L 7 (#39c192)
D 3 (#639863)
L 3 (#40fbd0)
D 4 (#515d93)
L 7 (#4acc50)
U 3 (#29cb83)
L 2 (#2835a2)
U 10 (#066c93)'''

run_tests()