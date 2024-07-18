pub struct DataSmoother {
    samples: Vec<f32>,
    window_size: usize,
}

impl DataSmoother {
    pub fn new(window_size: usize) -> Self {
        Self {
            samples: Vec::with_capacity(window_size),
            window_size,
        }
    }

    pub fn add_sample(&mut self, sample: f32) -> f32 {
        if self.samples.len() >= self.window_size {
            self.samples.remove(0);
        }
        self.samples.push(sample);

        // Calculate moving average
        self.samples.iter().sum::<f32>() / self.samples.len() as f32
    }
}
