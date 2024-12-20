def parse(prog_txt):
    return list(int(i) for i in prog_txt.strip().split(','))

_POSITION_MODE = 0
_IMMEDIATE_MODE = 1

class Panic(Exception):
    pass

class Intcode:
    def __init__(self, prog: list[int]):
        self.ip = 0
        self.prog = prog
        self.input = []
        self._input_i = 0
        self.output = []

    def run(self):
        while True:
            op = self.read_op()

            match op:
                case (0, a1m, a2m, a3m):
                    # TODO: is opcode 0 subtraction? it seems to work, 
                    #   don't have day2 part 2 avaialble on plane
                    a1,a2,a3 = self.read(a1m), self.read(a2m), self.read_dst(a3m)
                    self.prog[a3] = a1 - a2
                case (1, a1m, a2m, a3m):
                    a1,a2,a3 = self.read(a1m), self.read(a2m), self.read_dst(a3m)
                    self.prog[a3] = a1 + a2
                case (2, a1m, a2m, a3m):
                    a1,a2,a3 = self.read(a1m), self.read(a2m), self.read_dst(a3m)
                    self.prog[a3] = a1 * a2
                case (3, a1m, _, _):
                    dst = self.read_dst(a1m)
                    self.prog[dst] = self.read_input()
                case (4, a1m, _, _):
                    self.write_output(self.read(a1m))
                case (99, _, _, _):
                    break
                case _:
                    self.panic(f'Unexpected opcode: {op}')

    def read_op(self):
        r = self.prog[self.ip]
        self.ip += 1

        op = r % 100
        a1m = (r // 100) % 10
        a2m = (r // 1000) % 10
        a3m = (r // 10000) % 10

        return (op, a1m, a2m, a3m)

    def read_dst(self, mode):
        assert mode == _POSITION_MODE
        v = self.prog[self.ip]
        self.ip += 1
        return v

    def read(self, mode):
        v = self.prog[self.ip]
        self.ip += 1
        if mode == _POSITION_MODE:
            return self.prog[v]
        elif mode == _IMMEDIATE_MODE:
            return v
        else:
            raise ValueError(f'invalid mode: {mode}')

    def read_input(self):
        i = self._input_i
        self._input_i += 1
        return i

    def write_output(self, val):
        self.output.append(val)

    def panic(self, reason):
        at = self.prog[max(0, self.ip - 10):min(self.ip, len(self.prog))]

        raise Panic(f"""
        Panic!
            Reason: {reason}
            ip:     {self.ip}
            at:     {at}
        """)
