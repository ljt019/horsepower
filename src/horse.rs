use macroquad::prelude::*;

pub struct Horse {
    frames: Vec<Texture2D>,
    current_frame: usize,
    animation_speed: f32,
    animation_timer: f32,
}

impl Horse {
    pub fn new(frames: Vec<Texture2D>) -> Self {
        Self {
            frames,
            current_frame: 0,
            animation_speed: 0.0,
            animation_timer: 0.0,
        }
    }

    pub fn set_speed(&mut self, horsepower: f32) {
        self.animation_speed = (horsepower * 5.0).min(10.0).max(0.0);
    }

    pub fn update(&mut self, dt: f32) {
        if self.animation_speed > 0.0 {
            self.animation_timer += dt * self.animation_speed;
            if self.animation_timer >= 1.0 {
                self.current_frame = (self.current_frame + 1) % self.frames.len();
                self.animation_timer -= 1.0;
            }
        }
    }

    pub fn draw(&self) {
        let scale_factor = 0.6; // Variable to control the scale factor
        let y_offset = 50.0; // Variable to control the Y offset

        let frame = &self.frames[self.current_frame];
        let (frame_width, frame_height) = (frame.width(), frame.height());
        let scaled_width = frame_width * scale_factor;
        let scaled_height = frame_height * scale_factor;
        let (screen_width, screen_height) = (screen_width(), screen_height());
        let x = (screen_width - scaled_width) / 2.2;
        let y = ((screen_height - scaled_height) / 2.0) + y_offset; // Apply Y offset here

        draw_texture_ex(
            frame,
            x,
            y,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(scaled_width, scaled_height)),
                ..Default::default()
            },
        );
    }
}
