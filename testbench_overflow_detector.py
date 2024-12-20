from myhdl import block, instance, delay, Signal, intbv, Simulation
from overflow_detector import overflow_detector

@block
def testbench():
    # Define signals
    A = Signal(intbv(0)[1:])
    B = Signal(intbv(0)[1:])
    SUM = Signal(intbv(0)[1:])
    OVERFLOW = Signal(intbv(0)[1:])

    # Instantiate the DUT
    dut = overflow_detector(A, B, SUM, OVERFLOW)

    @instance
    def stimulus():
        print("A B SUM  | Expected Overflow  | Detected Overflow")
        test_vectors = [
            (0, 0, 0, 0),
            (0, 0, 1, 1),
            (0, 1, 0, 0),
            (0, 1, 1, 0),
            (1, 0, 0, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 1),
            (1, 1, 1, 0),
        ]
        
        for a, b, sum_val, expected in test_vectors:
            A.next = a
            B.next = b
            SUM.next = sum_val
            yield delay(10)
            print(f"{int(A)} {int(B)}  {int(SUM)}   |         {expected}          |         {int(OVERFLOW)}")
            assert OVERFLOW == expected, f"Test failed for input {a}, {b}, {sum_val}"

    return dut, stimulus

# Run the simulation
tb = testbench()
sim = Simulation(tb)
sim.run()