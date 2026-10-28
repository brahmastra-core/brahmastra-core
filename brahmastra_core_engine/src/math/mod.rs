use subtle::{Choice, ConstantTimeEq, ConditionallySelectable};

pub fn verify_age_constraint(current_year: u32, birth_year: u32, min_age: u32) -> bool {
    if current_year < birth_year {
        return false;
    }
    (current_year - birth_year) >= min_age
}

pub fn constant_time_eq_slices(a: &[u8], b: &[u8]) -> Choice {
    a.ct_eq(b)
}

pub fn constant_time_select(condition: Choice, a: u8, b: u8) -> u8 {
    u8::conditional_select(&a, &b, condition)
}
