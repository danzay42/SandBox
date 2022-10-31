// // FFI: calling C from Rust
// extern {
//     fn readlink(path: *const u8, buf: *const u8, bufsize: usize) -> i64;
// }
// fn rs_readlink(path: &str) -> Result<String, ...> {
//     let mut r = vec![0u8, 100];
//     if unsafe { readlink(path.as_ptr(), r.as_mut_ptr(), 100) } < 0 {
//         Err(...)
//     } else {
//         Ok(String::from_utf8(r)?)
//     }
// }

// // FFI: calling Rust from C
// #![no_mangle]
// extern fn add(x: u32, y: u32) {x+y}

// // FFI: types
// #[repr(C)]
// struct SigAction {
//     sa_handler: extern fn(c_int),
//     sa_flags: c_int,
//     ...
// }
// extern {
//     fn sig_action(signum: c_int, act: *const SigAction, oldact: *mut SigAction);
// }
// extern fn handler(signal: c_int) {...}
// let act = SigAction {sa_handler: handler, ...}
// unsafe {
//     sig_action(SIGINT, &act, ptr::null_mut())
// }