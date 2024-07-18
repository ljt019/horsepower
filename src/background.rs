use macroquad::prelude::*;

pub struct Background {
    texture: Texture2D,
    x: f32,
    width: f32,
    height: f32,
}

impl Background {
    pub fn new(texture: Texture2D) -> Self {
        let width = texture.width();
        let height = texture.height();
        Self {
            texture,
            x: 0.0,
            width,
            height,
        }
    }

    pub fn update(&mut self, horsepower: f32) {
        let speed = horsepower * 2.0; // Adjust this factor as needed
        self.x = (self.x - speed) % self.width;
        if self.x > 0.0 {
            self.x -= self.width;
        }
    }

    pub fn draw(&self, window_size: Vec2) {
        let scale_factor = window_size.y / self.height;
        let scaled_width = self.width * scale_factor;
        let scaled_height = window_size.y;

        // Draw the main part of the image
        draw_texture_ex(
            &self.texture,
            self.x * scale_factor,
            0.0,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(scaled_width, scaled_height)),
                source: None,
                ..Default::default()
            },
        );

        // Draw the wrapping part of the image
        draw_texture_ex(
            &self.texture,
            (self.x + self.width) * scale_factor,
            0.0,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(scaled_width, scaled_height)),
                source: None,
                ..Default::default()
            },
        );
    }
}
