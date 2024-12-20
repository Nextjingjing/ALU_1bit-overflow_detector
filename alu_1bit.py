from myhdl import block, always_comb, Signal, intbv, ConversionError

@block
def alu_1bit(a, b, cin, op, less, ainv, binv, result, cout):
    # กำหนดสัญญาณภายในที่มีชนิดชัดเจน
    a_val = Signal(intbv(0)[1:])
    b_val = Signal(intbv(0)[1:])
    sum_val = Signal(intbv(0)[1:])
    carry_val = Signal(intbv(0)[1:])
    and_res = Signal(intbv(0)[1:])
    or_res = Signal(intbv(0)[1:])

    @always_comb
    def logic():
        # Invert inputs if needed
        a_val.next = ~a if ainv else a
        b_val.next = ~b if binv else b

        # Compute intermediate results
        sum_val.next = a_val ^ b_val ^ cin
        carry_val.next = (a_val & b_val) | (b_val & cin) | (a_val & cin)
        and_res.next = a_val & b_val
        or_res.next = a_val | b_val

        # Select operation based on 'op'
        if op == 0b00:   # AND
            result.next = and_res
        elif op == 0b01: # OR
            result.next = or_res
        elif op == 0b10: # ADD
            result.next = sum_val
        elif op == 0b11: # SLT
            result.next = less
        else:
            result.next = 0  # Default case

        # Set carry out
        cout.next = carry_val

    return logic


# สัญญาณอินพุตและเอาต์พุต
a = Signal(intbv(0)[1:])
b = Signal(intbv(0)[1:])
cin = Signal(intbv(0)[1:])
op = Signal(intbv(0)[2:])
less = Signal(intbv(0)[1:])
ainv = Signal(intbv(0)[1:])
binv = Signal(intbv(0)[1:])
result = Signal(intbv(0)[1:])
cout = Signal(intbv(0)[1:])

# การแปลงไปเป็น VHDL
try:
    alu_inst = alu_1bit(a, b, cin, op, less, ainv, binv, result, cout)
    alu_inst.convert(hdl='VHDL')
except ConversionError as e:
    print(f"Conversion failed: {e}")
