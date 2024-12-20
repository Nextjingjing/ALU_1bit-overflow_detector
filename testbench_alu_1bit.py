# alu_tb.py
from myhdl import block, instance, delay, Simulation, StopSimulation, Signal, intbv
from alu_1bit import alu_1bit

@block
def testbench():
    # กำหนดสัญญาณอินพุตและเอาต์พุต
    a = Signal(intbv(0)[1:])
    b = Signal(intbv(0)[1:])
    cin = Signal(intbv(0)[1:])
    op = Signal(intbv(0)[2:])
    less = Signal(intbv(0)[1:])
    ainv = Signal(intbv(0)[1:])
    binv = Signal(intbv(0)[1:])
    result = Signal(intbv(0)[1:])
    cout = Signal(intbv(0)[1:])

    # สร้างอินสแตนซ์ของ ALU
    alu_inst = alu_1bit(a, b, cin, op, less, ainv, binv, result, cout)

    # นิยามชุดทดสอบ โดยใช้ dictionary สำหรับแต่ละ Test Case
    test_vectors = [
        {
            'name': 'Test Case 0: AND operation with A=1, B=1, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b00,
            'a': 1,
            'b': 1,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 1,  # 1 & 1 = 1
            'expected_cout': 1     # carry_val = (1&1)|(1&0)|(1&0) = 1
        },
        {
            'name': 'Test Case 1: AND operation with A=1, B=0, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b00,
            'a': 1,
            'b': 0,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 0,  # 1 & 0 = 0
            'expected_cout': 0     # carry_val = (1&0)|(0&0)|(1&0) = 0
        },
        {
            'name': 'Test Case 2: AND operation with A=0, B=0, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b00,
            'a': 0,
            'b': 0,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 0,  # 0 & 0 = 0
            'expected_cout': 0     # carry_val = 0
        },
        {
            'name': 'Test Case 3: OR operation with A=1, B=1, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b01,
            'a': 1,
            'b': 1,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 1,  # 1 | 1 = 1
            'expected_cout': 1     # carry_val = (1&1)|(1&0)|(1&0) = 1
        },
        {
            'name': 'Test Case 4: OR operation with A=1, B=0, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b01,
            'a': 1,
            'b': 0,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 1,  # 1 | 0 = 1
            'expected_cout': 0     # carry_val = (1&0)|(0&0)|(1&0) = 0
        },
        {
            'name': 'Test Case 5: OR operation with A=0, B=0, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b01,
            'a': 0,
            'b': 0,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 0,  # 0 | 0 = 0
            'expected_cout': 0     # carry_val = (0&0)|(0&0)|(0&0) = 0
        },
        {
            'name': 'Test Case 6: ADD operation with A=1, B=1, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b10,
            'a': 1,
            'b': 1,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 0,  # 1 + 1 + 0 = 0 with carry 1
            'expected_cout': 1     # carry_val = (1&1)|(1&0)|(1&0) = 1
        },
        {
            'name': 'Test Case 7: ADD operation with A=1, B=0, CIN=1, AINV=0, BINV=0, LESS=0',
            'op': 0b10,
            'a': 1,
            'b': 0,
            'cin': 1,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 0,  # 1 + 0 + 1 = 0 with carry 1
            'expected_cout': 1     # carry_val = (1&0)|(0&1)|(1&1) = 1
        },
        {
            'name': 'Test Case 8: ADD operation with A=0, B=0, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b10,
            'a': 0,
            'b': 0,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 0,  # 0 + 0 + 0 = 0 with carry 0
            'expected_cout': 0     # carry_val = (0&0)|(0&0)|(0&0) = 0
        },
        {
            'name': 'Test Case 9: SLT operation with A=0, B=0, CIN=0, AINV=0, BINV=0, LESS=1',
            'op': 0b11,
            'a': 0,
            'b': 0,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 1,
            'expected_result': 1,  # SLT = 1
            'expected_cout': 0     # carry_val = (0&0)|(0&0)|(0&0) = 0
        },
        {
            'name': 'Test Case 10: SLT operation with A=1, B=1, CIN=0, AINV=0, BINV=0, LESS=0',
            'op': 0b11,
            'a': 1,
            'b': 1,
            'cin': 0,
            'ainv': 0,
            'binv': 0,
            'less': 0,
            'expected_result': 0,  # SLT = 0
            'expected_cout': 1     # carry_val = (1&1)|(1&0)|(1&0) = 1
        },
        {
            'name': 'Test Case 11: AND operation with AINV=1, BINV=1, A=1, B=1, CIN=0, LESS=0',
            'op': 0b00,
            'a': 1,
            'b': 1,
            'cin': 0,
            'ainv': 1,
            'binv': 1,
            'less': 0,
            'expected_result': 0,  # ~1 & ~1 = 0
            'expected_cout': 0     # carry_val = (1&1)|(1&0)|(1&0) = 1 → อาจจะต้องปรับค่าที่คาดหวังเป็น 1
        },
        {
            'name': 'Test Case 12: OR operation with AINV=1, BINV=0, A=0, B=0, CIN=0, LESS=0',
            'op': 0b01,
            'a': 0,
            'b': 0,
            'cin': 0,
            'ainv': 1,
            'binv': 0,
            'less': 0,
            'expected_result': 1,  # ~0 | 0 = 1
            'expected_cout': 0     # carry_val = (0&0)|(0&0)|(0&0) = 0
        },
    ]

    @instance
    def stim():
        for vector in test_vectors:
            name = vector['name']
            op_val = vector['op']
            a_val = vector['a']
            b_val = vector['b']
            cin_val = vector['cin']
            ainv_val = vector['ainv']
            binv_val = vector['binv']
            less_val = vector['less']
            expected_result = vector['expected_result']
            expected_cout = vector['expected_cout']

            # กำหนดค่าอินพุต
            op.next = op_val
            a.next = a_val
            b.next = b_val
            cin.next = cin_val
            ainv.next = ainv_val
            binv.next = binv_val
            less.next = less_val

            # รอให้ตรรกะแบบ combinational ประมวลผล
            yield delay(1)

            # อ่านค่าผลลัพธ์
            actual_result = int(result)
            actual_cout = int(cout)

            # คำนวณ carry_val จากอินพุต
            computed_cout = (a_val & b_val) | (b_val & cin_val) | (a_val & cin_val)

            # ตรวจสอบค่าที่ได้กับค่าที่คาดหวัง
            if (actual_result != expected_result) or (actual_cout != expected_cout):
                print(f"{name} FAILED:")
                print(f"  Inputs:")
                print(f"    OP     = {op_val:02b}")
                print(f"    A      = {a_val}")
                print(f"    B      = {b_val}")
                print(f"    CIN    = {cin_val}")
                print(f"    AINV   = {ainv_val}")
                print(f"    BINV   = {binv_val}")
                print(f"    LESS   = {less_val}")
                print(f"  Outputs:")
                print(f"    RESULT = {actual_result}")
                print(f"    COUT   = {actual_cout}")
                print(f"  Expected:")
                print(f"    RESULT = {expected_result}")
                print(f"    COUT   = {expected_cout}\n")
            else:
                print(f"{name} PASSED.")
                print(f"  Inputs:")
                print(f"    OP     = {op_val:02b}")
                print(f"    A      = {a_val}")
                print(f"    B      = {b_val}")
                print(f"    CIN    = {cin_val}")
                print(f"    AINV   = {ainv_val}")
                print(f"    BINV   = {binv_val}")
                print(f"    LESS   = {less_val}")
                print(f"  Outputs:")
                print(f"    RESULT = {actual_result}")
                print(f"    COUT   = {actual_cout}")
                print(f"  Expected:")
                print(f"    RESULT = {expected_result}")
                print(f"    COUT   = {expected_cout}\n")

        raise StopSimulation

    return alu_inst, stim

if __name__ == '__main__':
    tb = testbench()
    tb.config_sim(trace=False)
    tb.run_sim()
