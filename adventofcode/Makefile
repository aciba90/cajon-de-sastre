all: check format lint test

format:
	cargo fmt --all -- --check

lint:
	cargo clippy -- --deny warnings

test:
	cargo test

check:
	cargo check

clean:
	cargo clean

