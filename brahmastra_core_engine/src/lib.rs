pub mod crypto;
pub mod math;
pub mod memory;
pub mod errors;
pub mod ffi;
#[cfg(test)]
mod tests {
    use super::*;
    use zeroize::Zeroize;
    use std::time::Instant;

    #[test]
    fn test_modular_setup() {
        assert!(math::verify_age_constraint(2026, 1995, 18));
        assert!(!math::verify_age_constraint(2026, 2012, 18));
    }

    #[test]
    fn test_constant_time_operations() {
        let a = [1u8, 2, 3, 4];
        let b = [1u8, 2, 3, 4];
        let c = [1u8, 2, 3, 5];

        let eq = math::constant_time_eq_slices(&a, &b);
        assert_eq!(eq.unwrap_u8(), 1);

        let neq = math::constant_time_eq_slices(&a, &c);
        assert_eq!(neq.unwrap_u8(), 0);

        let selected_a = math::constant_time_select(eq, 10, 20);
        assert_eq!(selected_a, 20);

        let selected_b = math::constant_time_select(neq, 10, 20);
        assert_eq!(selected_b, 10);
    }

    #[test]
    fn test_memory_zeroize_on_drop() {
        let mut key_buffer = [0x42u8; 32];
        assert_eq!(key_buffer[0], 0x42);

        key_buffer.zeroize();

        for byte in key_buffer.iter() {
            assert_eq!(*byte, 0x00);
        }

        let sensitive_key = memory::SensitiveKey::new([0xAAu8; 32]);
        assert_eq!(sensitive_key.expose_key()[0], 0xAA);
        drop(sensitive_key);
    }

    #[test]
    fn test_bfv_homomorphic_gates_and_benchmark() {
        let ct1 = crypto::BfvCiphertext::new([10, 20, 30, 40], [1, 2, 3, 4]);
        let ct2 = crypto::BfvCiphertext::new([5, 15, 25, 35], [2, 3, 4, 5]);

        let start_add = Instant::now();
        let ct_add = ct1.homomorphic_add(&ct2);
        let add_duration = start_add.elapsed();

        assert_eq!(ct_add.c0, [15, 35, 55, 75]);
        assert_eq!(ct_add.c1, [3, 5, 7, 9]);

        let start_mul = Instant::now();
        let ct_mul = ct1.homomorphic_mul_plain(2);
        let mul_duration = start_mul.elapsed();

        assert_eq!(ct_mul.c0, [20, 40, 60, 80]);
        assert_eq!(ct_mul.c1, [2, 4, 6, 8]);

        println!("\n[Benchmark] Homomorphic Add Duration: {:?}", add_duration);
        println!("[Benchmark] Homomorphic Mul Duration: {:?}", mul_duration);
    }
}