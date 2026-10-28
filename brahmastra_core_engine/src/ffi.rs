use crate::crypto::{BfvCiphertext, VECTOR_LEN};

#[no_mangle]
pub extern "C" fn ffi_homomorphic_add(
    c0_a: *const u64,
    c1_a: *const u64,
    c0_b: *const u64,
    c1_b: *const u64,
    out_c0: *mut u64,
    out_c1: *mut u64,
) -> i32 {
    if c0_a.is_null() || c1_a.is_null() || c0_b.is_null() || c1_b.is_null() || out_c0.is_null() || out_c1.is_null() {
        return -1;
    }

    unsafe {
        let mut slice_c0_a = [0u64; VECTOR_LEN];
        let mut slice_c1_a = [0u64; VECTOR_LEN];
        let mut slice_c0_b = [0u64; VECTOR_LEN];
        let mut slice_c1_b = [0u64; VECTOR_LEN];

        std::ptr::copy_nonoverlapping(c0_a, slice_c0_a.as_mut_ptr(), VECTOR_LEN);
        std::ptr::copy_nonoverlapping(c1_a, slice_c1_a.as_mut_ptr(), VECTOR_LEN);
        std::ptr::copy_nonoverlapping(c0_b, slice_c0_b.as_mut_ptr(), VECTOR_LEN);
        std::ptr::copy_nonoverlapping(c1_b, slice_c1_b.as_mut_ptr(), VECTOR_LEN);

        let ct_a = BfvCiphertext::new(slice_c0_a, slice_c1_a);
        let ct_b = BfvCiphertext::new(slice_c0_b, slice_c1_b);

        let ct_res = ct_a.homomorphic_add(&ct_b);

        std::ptr::copy_nonoverlapping(ct_res.c0.as_ptr(), out_c0, VECTOR_LEN);
        std::ptr::copy_nonoverlapping(ct_res.c1.as_ptr(), out_c1, VECTOR_LEN);
    }

    0
}