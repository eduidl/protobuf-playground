fn main() {
    println!("cargo:rerun-if-changed=../proto/proto2_sample.proto");
    println!("cargo:rerun-if-changed=../proto/proto3_sample.proto");

    let mut config = prost_build::Config::new();
    config.out_dir("src/gen");
    config
        .compile_protos(
            &["../proto/proto2_sample.proto", "../proto/proto3_sample.proto"],
            &["../proto"],
        )
        .expect("failed to compile protos");
}
