from enum import IntEnum
from numpy import Infinity
from test_utils import run_test
from typing import List, Tuple, Dict
from math import sqrt, ceil, floor, prod, lcm
import re
import numpy as np
from functools import cache


class Module:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.inputs = {}
        self.outputs = []
        self.state = False

    def process_pulse(self, pulse: int, source: str) -> int:
        if self.type == 'b':
            return pulse
        elif self.type == '%':
            if pulse == 0:
                self.state = not self.state
                return 1 if self.state else 0
            return None
        elif self.type == '&':
            self.inputs[source] = pulse
            for i in self.inputs.values():
                if i == 0:
                    return 1
            return 0
        elif self.type == '0':
            return None
        else:
            assert False


def solve(data: str) -> int:
    modules = {}
    for module_def in data.splitlines():
        module_name_def, outputs_def = module_def.split(' -> ')
        m = Module()
        m.type = module_name_def[0]
        if m.type == 'b':
            m.name = module_name_def
        else:
            m.name = module_name_def[1:]
        m.outputs = outputs_def.split(', ')
        modules[m.name] = m

    modules_to_add = {}
    for m in modules.values():
        for o in m.outputs:
            if o in modules:
                modules[o].inputs[m.name] = 0
            else:
                md = Module()
                md.name = o
                md.type = '0'
                modules_to_add[o] = md
    for k, v in modules_to_add.items():
        modules[k] = v

    pulses_count = {0: 0, 1: 0}
    for _ in range(1000):
        pulses = [('button', 0, 'broadcaster')]
        while len(pulses) > 0:
            new_pulses = []
            for s, p, m in pulses:
                pulses_count[p] += 1
                r = modules[m].process_pulse(p, s)
                # print(s, ')-', p, '->(', m, ')->', r)
                if r is not None:
                    for dm in modules[m].outputs:
                        new_pulses.append((m, r, dm))
            pulses = new_pulses
    return pulses_count[0] * pulses_count[1]


def solve2(data: str) -> int:
    modules = {}
    for module_def in data.splitlines():
        module_name_def, outputs_def = module_def.split(' -> ')
        m = Module()
        m.type = module_name_def[0]
        if m.type == 'b':
            m.name = module_name_def
        else:
            m.name = module_name_def[1:]
        m.outputs = outputs_def.split(', ')
        modules[m.name] = m

    modules_to_add = {}
    for m in modules.values():
        for o in m.outputs:
            if o in modules:
                modules[o].inputs[m.name] = 0
            else:
                md = Module()
                md.name = o
                md.type = '0'
                md.inputs[m.name] = 0
                modules_to_add[o] = md
    for k, v in modules_to_add.items():
        modules[k] = v

    visited_nodes = set()
    nodes = ['fc']
    while len(nodes) > 0:
        new_nodes = []
        for n in nodes:
            if n not in visited_nodes:
                for s in modules[n].inputs.keys():
                    new_nodes.append(s)
                    print(f'{s}_{modules[s].type} {n}_{modules[n].type}')
                visited_nodes.add(n)
        nodes = new_nodes

    chunks = {'pm': None, 'bd': None, 'cc': None, 'rs': None}
    empty_chunks = len(chunks.keys())

    # pulses_count = { 0: 0, 1: 0 }
    press_count = 0
    while True:
        press_count += 1
        pulses = [('button', 0, 'broadcaster')]
        while len(pulses) > 0:
            new_pulses = []
            for s, p, m in pulses:
                # pulses_count[p] += 1
                r = modules[m].process_pulse(p, s)

                if s in chunks:
                    if chunks[s] is None:
                        if r == 1:
                            chunks[s] = press_count
                            empty_chunks -= 1
                            if empty_chunks == 0:
                                return lcm(*chunks.values())

                if m == 'rx':
                    # print(press_count, ':', s, ')-', p, '->(', m, ')->', r)
                    if p == 0:
                        return press_count + 1
                if r is not None:
                    for dm in modules[m].outputs:
                        new_pulses.append((m, r, dm))
            pulses = new_pulses
    # return pulses_count[0] * pulses_count[1]


small_vector = ''
small_vector_2 = ''
official_vector = ''


def run_tests():
    # run_test(solve, [small_vector], 32000000)
    # run_test(solve, [small_vector_2], 11687500)
    # run_test(solve, [official_vector], 899848294)
    # run_test(solve2, [small_vector], 167409079868000)
    # run_test(solve2, [small_vector_2], 167409079868000)
    run_test(solve2, [official_vector], 130262715574114)


small_vector = r'''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

small_vector_2 = r'''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''

official_vector = r'''%jx -> rt, rs
&cc -> cd, fc, qr, nl, gk, zr
%qs -> cl, rs
%zr -> cq
%mx -> nr, pm
%mj -> qr, cc
%cj -> cc, nt
%jv -> sp
%dj -> bd, zc
%kt -> lt
broadcaster -> gz, xg, cd, sg
&dn -> rx
%br -> nf, bd
%cd -> cc, nl
%zc -> jq, bd
%xg -> cf, pm
%nz -> gm, bd
&dd -> dn
%nb -> sl
&pm -> kt, xg, xp, jv, sp
&fh -> dn
%rt -> qq
%qq -> rs, hd
%hd -> qs, rs
&xp -> dn
%pj -> cc, mj
%gz -> bd, kb
%zd -> jv, pm
%cq -> cj, cc
%qr -> gk
%ng -> jk, bd
%kb -> bd, sv
%cl -> zx, rs
%gj -> zd, pm
%sl -> kx
%sv -> br
%nf -> bd, nz
%zx -> rs
%nt -> mn, cc
%rh -> nb, rs
%gk -> ln
&bd -> gm, gz, fh, sv
%jq -> ng, bd
%sp -> pc
%sg -> rs, rh
%kx -> jx
&fc -> dn
%cf -> gj, pm
%pc -> kt, pm
%jk -> bd
%vf -> pm
&rs -> sg, dd, sl, kx, nb, rt
%nr -> vf, pm
%ln -> zr, cc
%lt -> pm, mx
%gm -> dj
%nl -> pj
%mn -> cc'''

run_tests()
