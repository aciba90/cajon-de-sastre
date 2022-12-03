#[macro_export]
macro_rules! locate_data {
    ($year:expr, $day:expr ) => {
        concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/data/",
            $year,
            "/day",
            $day,
            ".txt"
        )
    };
}
