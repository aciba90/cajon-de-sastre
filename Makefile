all: format lint test

format:
	cargo fmt --check

lint:
	cargo clippy -- --deny warnings

test:
	cargo test

build:
	cargo build --release

clean:
	cargo clean

