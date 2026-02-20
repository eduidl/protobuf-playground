use prost::Message;

mod compat {
    include!("gen/compat.rs");
}

fn check_proto2() {
    let msg = compat::Proto2Sample::decode(&[][..]).expect("decode proto2 empty bytes");

    // required int32 req_int = 1;
    assert_eq!(msg.req_int, 0, "proto2 required int32 should decode to type default 0");

    // required Proto2Child req_msg = 2;
    assert!(msg.req_msg.value.is_none(), "proto2 child message should have default value None after empty decode");
    assert_eq!(msg.req_msg.value(), 0, "proto2 child message should have effective value 0 after empty decode");

    // optional int32 opt_int = 3;
    assert!(msg.opt_int.is_none(), "proto2 optional int should be absent after empty decode");
    assert_eq!(
        msg.opt_int(),
        0,
        "proto2 optional int should have effective value 0 after empty decode"
    );

    // optional int32 opt_with_default = 4 [default = 7];
    assert!(msg.opt_with_default.is_none(), "proto2 optional int with default should still be absent after empty decode");
    assert_eq!(
        msg.opt_with_default(),
        7,
        "proto2 optional int with default=7 should have effective value 7"
    );

    // optional Proto2Child opt_msg = 5;
    assert!(msg.opt_msg.is_none(), "proto2 optional message should be absent after empty decode");
    // opt_msg() does not exists

    // repeated int32 rep_int = 6 [packed = false];
    assert!(msg.rep_int.is_empty(), "proto2 repeated int should be empty after empty decode");

    // oneof choice { int32 choice_int = 7; Proto2Child choice_msg = 8; }
    assert!(msg.choice.is_none(), "proto2 oneof should be unselected after empty decode");
}

fn check_proto3() {
    let msg = compat::Proto3Sample::decode(&[][..]).expect("decode proto3 empty bytes");

    // int32 plain_int = 1;
    assert_eq!(msg.plain_int, 0, "proto3 plain int should decode to type default 0");

    // Proto3Child plain_msg = 2;
    assert!(msg.plain_msg.is_none(), "proto3 plain message should be absent after empty decode");

    // optional int32 opt_int = 3;
    assert!(msg.opt_int.is_none(), "proto3 optional int should be absent after empty decode");
    assert_eq!(msg.opt_int(), 0, "proto3 optional int should have effective value 0 after empty decode");

    // optional Proto3Child opt_msg = 5;
    assert!(msg.opt_msg.is_none(), "proto3 optional message should be absent after empty decode");

    // repeated int32 rep_int = 6;
    assert!(msg.rep_int.is_empty(), "proto3 repeated int should be empty after empty decode");

    // oneof choice { int32 choice_int = 7; Proto3Child choice_msg = 8; }
    assert!(msg.choice.is_none(), "proto3 oneof should be unselected after empty decode");
}

fn main() {
    check_proto2();
    check_proto3();
    println!("All Rust/prost compatibility assertions passed.");
}
