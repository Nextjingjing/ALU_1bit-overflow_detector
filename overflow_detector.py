from myhdl import block, always_comb, Signal, intbv, toVHDL, ConversionError

@block
def overflow_detector(a, b, sum, Overflow):
    @always_comb
    def logic():
        # Logic ตามสมการ Overflow
        Overflow.next = ((a ^ b) & ~sum) | (a & b)
    return logic


# Define input and output signals
A = Signal(intbv(0)[1:])    # a เป็น 1-bit Signal
B = Signal(intbv(0)[1:])    # b เป็น 1-bit Signal
SUM = Signal(intbv(0)[1:])  # sum เป็น 1-bit Signal
OVERFLOW = Signal(intbv(0)[1:])  # Overflow เป็น 1-bit Signal

# Create and convert to VHDL
try:
    inst = overflow_detector(A, B, SUM, OVERFLOW)
    inst.convert(hdl='VHDL')  # แปลงเป็น VHDL
except ConversionError as e:
    print(f"Conversion failed: {e}")
