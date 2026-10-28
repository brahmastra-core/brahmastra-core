pub const VECTOR_LEN: usize = 4;
pub const MODULUS: u64 = 65537;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BfvCiphertext {
    pub c0: [u64; VECTOR_LEN],
    pub c1: [u64; VECTOR_LEN],
}

impl BfvCiphertext {
    pub fn new(c0: [u64; VECTOR_LEN], c1: [u64; VECTOR_LEN]) -> Self {
        Self { c0, c1 }
    }

    pub fn homomorphic_add(&self, other: &Self) -> Self {
        let mut res_c0 = [0u64; VECTOR_LEN];
        let mut res_c1 = [0u64; VECTOR_LEN];

        for i in 0..VECTOR_LEN {
            res_c0[i] = (self.c0[i] + other.c0[i]) % MODULUS;
            res_c1[i] = (self.c1[i] + other.c1[i]) % MODULUS;
        }

        Self {
            c0: res_c0,
            c1: res_c1,
        }
    }

    pub fn homomorphic_mul_plain(&self, scalar: u64) -> Self {
        let mut res_c0 = [0u64; VECTOR_LEN];
        let mut res_c1 = [0u64; VECTOR_LEN];

        for i in 0..VECTOR_LEN {
            res_c0[i] = (self.c0[i] * (scalar % MODULUS)) % MODULUS;
            res_c1[i] = (self.c1[i] * (scalar % MODULUS)) % MODULUS;
        }

        Self {
            c0: res_c0,
            c1: res_c1,
        }
    }
}