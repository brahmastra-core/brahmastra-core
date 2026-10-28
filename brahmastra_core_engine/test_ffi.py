import ctypes
import os

# Load the compiled Rust shared library
lib_path = os.path.abspath("./target/release/libbrahmastra_core_engine.so")
rust_lib = ctypes.CDLL(lib_path)

# Define array type for length 4 with uint64
U64Array4 = ctypes.c_uint64 * 4

# Set argument and return types for ffi_homomorphic_add
rust_lib.ffi_homomorphic_add.argtypes = [
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint64),
    ctypes.POINTER(ctypes.c_uint64),
]
rust_lib.ffi_homomorphic_add.restype = ctypes.c_int32

# Test inputs
c0_a = U64Array4(10, 20, 30, 40)
c1_a = U64Array4(1, 2, 3, 4)

c0_b = U64Array4(5, 15, 25, 35)
c1_b = U64Array4(2, 3, 4, 5)

out_c0 = U64Array4(0, 0, 0, 0)
out_c1 = U64Array4(0, 0, 0, 0)

# Call Rust C-FFI function
status = rust_lib.ffi_homomorphic_add(c0_a, c1_a, c0_b, c1_b, out_c0, out_c1)

print(f"FFI Status Code: {status}")
print(f"Result c0: {list(out_c0)}")
print(f"Result c1: {list(out_c1)}")

# Validate output
assert status == 0
assert list(out_c0) == [15, 35, 55, 75]
assert list(out_c1) == [3, 5, 7, 9]

print("\n[SUCCESS] Python -> Rust C-FFI Bridge Test Passed!")