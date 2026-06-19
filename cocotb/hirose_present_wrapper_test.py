import os
import random
import time

import cocotb
import hirose_present
import numpy as np
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.result import ReturnValue, TestFailure
from cocotb.triggers import FallingEdge, RisingEdge, Timer

home = os.getenv("HOME")


CLK_PERIOD = 20  # 50 MHz
C_LEN = 64

# the keyword await
#   Testbenches built using Cocotb use coroutines.
#   While the coroutine is executing the simulation is paused.
#   The coroutine uses the await keyword
#   to pass control of execution back to
#   the simulator and simulation time can advance again.
#
#   await return when the 'Trigger' is resolve
#
#   Coroutines may also await a list of triggers
#   to indicate that execution should resume if any of them fires


def setup_function(dut, plaintext, c):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD).start())
    dut.rst.value = 0
    dut.c.value = c
    dut.plaintext.value = plaintext


async def rst_function_test(dut):
    dut.rst.value = 1

    await n_cycles_clock(dut, 10)

    if dut.hash_output != 0:
        raise TestFailure(
            """Error rst hash_output,wrong hash value = {0}, expected value is {1}""".format(
                hex(int(dut.hash_output.value)), 0
            )
        )

    if dut.end_signal != 0:
        raise TestFailure(
            """Error rst end_signal,wrong end_signal value = {0}, expected value is {1}""".format(
                hex(int(dut.end_signal.value)), 0
            )
        )

    dut.rst.value = 0


async def hash_test(dut, expected_value):

    i = 0
    while dut.end_signal.value == 0:
        # print(int(dut.current_state.value))

        if dut.end_hash.value:
            print("++++++++++++++++++++++++")
            # print(i)
            print(int(dut.counter_output))
            # print(hex(int(dut.plaintext)))
            # print(hex(int(dut.c.value)))
            print(hex(int(dut.h_left_o.value)))
            print(hex(int(dut.h_right_o.value)))
            print(hex(int(dut.hash_output.value)))

            print("~~~~~~~~~~~~~~~~~~")
            print(hex(int(dut.hash_impl.key_i.value)))
            print(hex(int(dut.hash_impl.input_left.value)))
            print(hex(int(dut.hash_impl.input_right.value)))
            print(hex(int(dut.hash_impl.output_left.value)))
            print(hex(int(dut.hash_impl.output_right.value)))

            print("++++++++++++++++++++++++++")
            await n_cycles_clock(dut, 2)
            print("++++++++++++++++++++++++")
            # print(i)
            print(int(dut.counter_output))
            # print(hex(int(dut.plaintext)))
            # print(hex(int(dut.c.value)))
            print(hex(int(dut.h_left_o.value)))
            print(hex(int(dut.h_right_o.value)))
            print(hex(int(dut.hash_output.value)))

            print("~~~~~~~~~~~~~~~~~~")
            print(hex(int(dut.hash_impl.key_i.value)))
            print(hex(int(dut.hash_impl.input_left.value)))
            print(hex(int(dut.hash_impl.input_right.value)))
            print(hex(int(dut.hash_impl.output_left.value)))
            print(hex(int(dut.hash_impl.output_right.value)))

            print("++++++++++++++++++++++++++")

        i = i + 1

        await n_cycles_clock(dut, 1)

    # await n_cycles_clock(dut,1)
    print(hex(int(dut.hash_output.value)))
    if dut.hash_output != expected_value:
        raise TestFailure(
            """Error hash,wrong value = {0}, expected value is {1}""".format(
                hex(int(dut.hash_output.value)), hex(expected_value)
            )
        )


async def n_cycles_clock(dut, n):
    for i in range(0, n):
        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)


async def run_test(dut, index=0):
    c = random.getrandbits(C_LEN)

    text = random.getrandbits(dut.DATA_WIDTH.value)
    hash_SW = hirose_present.HirosePresent(c, dut.DATA_WIDTH.value)
    expected_value = hash_SW.generate_hash(text)

    setup_function(dut, text, c)

    await rst_function_test(dut)
    await hash_test(dut, expected_value)


n = 5
factory = TestFactory(run_test)

# array de 10 int aleatorios entre 0 y 31
factory.add_option("index", range(0, n))
factory.generate_tests()
