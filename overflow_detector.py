from myhdl import block, always_comb, Signal, intbv, toVHDL, ConversionError

@block
def overflow_detector(a, b, sum, Overflow):
    @always_comb
    def logic():
        # Correct logic for detecting overflow in signed 1-bit addition
        Overflow.next = (a & b & ~sum) | (~a & ~b & sum)
    
    return logic

# Define input and output signals
A = Signal(intbv(0)[1:])
B = Signal(intbv(0)[1:])
SUM = Signal(intbv(0)[1:])
OVERFLOW = Signal(intbv(0)[1:])

# Create and convert to VHDL
try:
    inst = overflow_detector(A, B, SUM, OVERFLOW)
    inst.convert(hdl='VHDL')
except ConversionError as e:
    print(f"Conversion failed: {e}")