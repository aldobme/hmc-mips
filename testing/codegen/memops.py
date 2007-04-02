# memops.py
# generates memory operations
# 30mar2007, Thomas W. Barr
# tbarr at cs dot hmc dot edu

from operands import *
from codegenClasses import *
import random

class Memop:
    name = 'nop'
    mask = (2**LENGTH) - 1
    isLoad = True
    
    # sw $1 42($1)
    def __init__(self):
        self.ops = (sreg(), sreg())
        
    def __call__(self, machine):
        outIns = ""
        # determine where we'll be jumping to
        loc = memloc().location
        addressReg = treg()
        offset = random.randint(0,32)
        regVector = machine.regs[addressReg.reg] = loc - offset
        
        outIns += "addi %s $0 %d\n" % (str(addressReg.reg), regVector)
        
        if self.isLoad:
            dataReg = treg()
            try:
                data = (machine.mem[loc] & self.mask)
            except KeyError:
                # assuming we load 0 from nowhere
                data = 0
            machine.regs[dataReg.reg] = data
        else:
            dataReg = sreg()
            machine.mem[loc] = (machine.regs[dataReg.reg] & self.mask)
            
        # print the instruction
        outIns += "%s %s %d(%s)" % \
                (self.name, str(dataReg), offset, str(addressReg))
        return outIns
                
class sw(Memop):
    name = 'sw'
    isLoad = False
    
class lw(Memop):
    name = 'lw'
    isLoad = True

class sb(Memop):
    name = 'sb'
    isLoad = False
    mask = 0xFF

class lb(Memop):
    name = 'lb'
    isLoad = True
    mask = 0xFF

weights =  [(sw,    5),
            (lw,    5),
            (sb,    1),
            (lb,    1)]
            
# make weight table. if a weight is too big, this gets kinda slow
instructions = []            
for (op, weight) in weights:
    instructions += weight * [op]

def makeMemop(machine, act=True):
    ins = random.choice(instructions)()
    return ins(machine)            

#debug
if __name__ == '__main__':
    DEBUG = True
    m = MIPSComputer()
    print m.regs
    print m.mem
    s = sb()
    print s(m)
    l = lb()
    print l(m)
    print m.regs
    print m.mem