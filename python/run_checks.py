import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent
GEN_DIR = ROOT / "gen"
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

import proto2_sample_pb2  # type: ignore
import proto3_sample_pb2  # type: ignore


def expect_raises(exc_type: type[BaseException], fn: Callable[[], object]) -> BaseException:
    try:
        fn()
    except exc_type as exc:
        return exc
    except Exception as exc:  # noqa: BLE001
        raise AssertionError(f"Expected {exc_type.__name__}, got {type(exc).__name__}: {exc}") from exc
    raise AssertionError(f"Expected {exc_type.__name__}, but no exception was raised")


def _check_is_empty_message(msg) -> None:
    assert msg.value == 0
    assert msg.HasField("value") is False, "empty message field should be absent after empty parse"


def _check_req_int_proto2(msg) -> None:
    assert msg.req_int == 0, "proto2 required int32 should read type default 0 after empty parse"
    assert msg.HasField("req_int") is False, "proto2 required should be absent after empty parse"


def _check_req_msg_proto2(msg) -> None:
    _check_is_empty_message(msg.req_msg)
    assert msg.HasField("req_msg") is False, "proto2 required message field should be absent after empty parse"


def _check_opt_with_default_proto2(msg) -> None:
    assert msg.opt_with_default == 7, "proto2 optional with [default=7] should read 7 after empty parse"
    assert (
        msg.HasField("opt_with_default") is False
    ), "proto2 optional with default is still absent after empty parse"


def _check_plain_int_proto3(msg) -> None:
    assert msg.plain_int == 0, "proto3 plain int32 should read type default 0 after empty parse"
    exc = expect_raises(ValueError, lambda: msg.HasField("plain_int"))
    assert "non-optional" in str(exc), "proto3 plain scalar HasField error should mention non-optional"


def _check_plain_msg_proto3(msg) -> None:
    _check_is_empty_message(msg.plain_msg)
    assert msg.HasField("plain_msg") is False, "proto3 plain message field should be absent after empty parse"


def _check_opt_int_common(msg, proto: int) -> None:
    assert msg.opt_int == 0, f"proto{proto} optional scalar should read type default 0 after empty parse"
    assert msg.HasField("opt_int") is False, f"proto{proto} optional should be absent after empty parse"


def _check_opt_msg_common(msg, proto: int) -> None:
    _check_is_empty_message(msg.opt_msg)
    assert msg.HasField("opt_msg") is False, f"proto{proto} optional message field should be absent after empty parse"


def _check_rep_int_common(msg, proto: int) -> None:
    assert len(msg.rep_int) == 0, f"proto{proto} repeated should be empty after empty parse"
    expect_raises(ValueError, lambda: msg.HasField("rep_int"))


def _check_choice_int_common(msg, proto: int) -> None:
    assert msg.choice_int == 0, f"proto{proto} oneof int field should read type default 0 after empty parse"
    assert msg.HasField("choice_int") is False, f"proto{proto} oneof int field should be absent after empty parse"


def _check_choice_msg_common(msg, proto: int) -> None:
    _check_is_empty_message(msg.choice_msg)
    assert msg.HasField("choice_msg") is False, f"proto{proto} oneof message field should be absent after empty parse"


def _check_choice_common(msg, proto: int) -> None:
    assert msg.WhichOneof("choice") is None, f"proto{proto} oneof should be unselected after empty parse"
    _check_choice_int_common(msg, proto)  # 7
    _check_choice_msg_common(msg, proto)  # 8


def _check_common(msg, proto: int) -> None:
    _check_opt_int_common(msg, proto)  # 3
    _check_opt_msg_common(msg, proto)  # 5
    _check_rep_int_common(msg, proto)  # 6
    _check_choice_common(msg, proto)  # 7-8


def check_proto2() -> None:
    msg = proto2_sample_pb2.Proto2Sample()
    msg.ParseFromString(b"")

    assert msg.IsInitialized() is False, "proto2 required missing => IsInitialized must be False"

    _check_req_int_proto2(msg)  # 1
    _check_req_msg_proto2(msg)  # 2
    _check_opt_with_default_proto2(msg)  # 4
    _check_common(msg, proto=2)  # 3, 5-8


def check_proto3() -> None:
    msg = proto3_sample_pb2.Proto3Sample()
    msg.ParseFromString(b"")

    assert msg.IsInitialized() is True, "proto3 should always be initialized even if required fields are missing"

    _check_plain_int_proto3(msg)  # 1
    _check_plain_msg_proto3(msg)  # 2

    _check_common(msg, proto=3) # 3, 5-8


def main() -> None:
    check_proto2()
    check_proto3()
    print("All checks passed")


if __name__ == "__main__":
    main()
