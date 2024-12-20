from myhdl import block, instance, delay, Signal, intbv, Simulation
from overflow_detector import overflow_detector

@block
def testbench():
    # Define signals
    A = Signal(intbv(0)[1:])
    B = Signal(intbv(0)[1:])
    SUM = Signal(intbv(0)[1:])
    Overflow = Signal(intbv(0)[1:])

    # Instantiate the DUT
    dut = overflow_detector(A, B, SUM, Overflow)

    @instance
    def stimulus():
        print("A B SUM  | Expected Overflow  | Detected Overflow")
        test_vectors = [
            # Test cases
            (0, 1, 0, 1),  # Overflow
            (1, 0, 0, 1),  # Overflow
            (1, 1, 0, 1),  # Overflow
            (0, 0, 0, 0),  # No Overflow
            (0, 0, 1, 0),  # No Overflow
            (0, 1, 1, 0),  # No Overflow
            (1, 0, 1, 0),  # No Overflow
            (1, 1, 1, 1),  # Overflow
        ]
        
        for a, b, sum_val, expected in test_vectors:
            A.next = a
            B.next = b
            SUM.next = sum_val
            yield delay(10)
            print(f"{int(A)} {int(B)}  {int(SUM)}   |         {expected}          |         {int(Overflow)}")
            assert Overflow == expected, f"Test failed for input A={int(A)}, B={int(B)}, SUM={int(SUM)}"

    return dut, stimulus

# Run the simulation
tb = testbench()
sim = Simulation(tb)
sim.run()
