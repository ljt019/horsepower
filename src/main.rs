mod background;
mod data_smoother;
mod horse;

use background::Background;
use data_smoother::DataSmoother;
use horse::Horse;

use macroquad::prelude::*;
use rodio::{Decoder, OutputStream, Sink, Source};
use rust_embed::RustEmbed;
use std::io::Cursor;
use std::net::UdpSocket;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

#[derive(RustEmbed)]
#[folder = "assets/"]
struct Asset;

const BACKGROUND_SPEED_FACTOR: f32 = 6.0;
const HORSE_SPEED_FACTOR: f32 = 3.5;
const INTERPOLATION_DURATION: f32 = 1.0; // Duration for interpolation in seconds

fn window_conf() -> Conf {
    Conf {
        window_title: "Horsepower".to_owned(),
        fullscreen: true,
        ..Default::default()
    }
}

#[macroquad::main(window_conf)]
async fn main() {
    let socket = UdpSocket::bind("0.0.0.0:3450").expect("Could not bind socket");
    socket
        .set_nonblocking(true)
        .expect("Could not set socket to non-blocking");

    let mut horse_frames: Vec<Texture2D> = Vec::new();

    for i in 0..6 {
        let path = format!("horse/frame_{}.png", i);
        let texture_data = Asset::get(&path).expect("Failed to load horse frame");
        let texture =
            Texture2D::from_file_with_format(texture_data.data.as_ref(), Some(ImageFormat::Png));
        horse_frames.push(texture);
    }

    let background_data =
        Asset::get("background/HorseRace.png").expect("Failed to load background");
    let background_texture =
        Texture2D::from_file_with_format(background_data.data.as_ref(), Some(ImageFormat::Png));

    // Setup rodio
    let (_stream, stream_handle) = OutputStream::try_default().unwrap();
    let sink = Arc::new(Sink::try_new(&stream_handle).unwrap());
    let audio_data = Asset::get("audio/horsegallop.wav").expect("Failed to load audio");
    let source = Decoder::new(Cursor::new(audio_data.data)).unwrap();
    let looped_source = source.repeat_infinite();
    sink.append(looped_source);
    sink.pause(); // Start paused
    sink.set_volume(0.5);

    let mut background = Background::new(background_texture);
    let mut horse = Horse::new(horse_frames);
    let mut data_smoother = DataSmoother::new(5); // Use a window of 5 samples for smoothing

    let mut current_horsepower = 0.0;
    let mut target_horsepower = 0.0;
    let mut interpolation_start_time = Instant::now();

    // Main game loop
    loop {
        let frame_time = get_frame_time();

        let mut buf = [0; 12]; // Increased buffer size to accommodate 3 f32 values
                               // Attempt to read from the socket
        match socket.recv_from(&mut buf) {
            Ok((amt, _src)) => {
                if amt >= 12 {
                    let horsepower = f32::from_le_bytes([buf[0], buf[1], buf[2], buf[3]]);
                    let rpm = f32::from_le_bytes([buf[4], buf[5], buf[6], buf[7]]);
                    let torque = f32::from_le_bytes([buf[8], buf[9], buf[10], buf[11]]);

                    println!(
                        "Received - Horsepower: {}, RPM: {}, Torque: {}",
                        horsepower, rpm, torque
                    );

                    // Update the target horsepower and reset interpolation timer
                    target_horsepower = data_smoother.add_sample(horsepower);
                    interpolation_start_time = Instant::now();
                }
            }
            Err(_) => {
                // Handle other errors or no data
            }
        };

        // Interpolate horsepower
        let elapsed = interpolation_start_time.elapsed().as_secs_f32();
        let t = (elapsed / INTERPOLATION_DURATION).min(1.0);
        current_horsepower = lerp(current_horsepower, target_horsepower, t);

        let window_size = vec2(screen_width(), screen_height());

        // Update background and horse
        background.update(current_horsepower * BACKGROUND_SPEED_FACTOR);
        horse.set_speed(current_horsepower * HORSE_SPEED_FACTOR);

        background.draw(window_size);
        horse.update(frame_time);
        horse.draw();

        // Display horsepower value
        let horsepower_text = format!("Horsepower: {:.2}", current_horsepower);
        let text_dimensions = measure_text(&horsepower_text, None, 30, 1.0);
        draw_text(
            &horsepower_text,
            screen_width() / 2.0 - text_dimensions.width / 2.0,
            40.0,
            30.0,
            BLACK,
        );

        if target_horsepower > 0.0 {
            if sink.is_paused() {
                sink.play();
            }
        } else if !sink.is_paused() {
            thread::sleep(std::time::Duration::from_millis(1500));
            sink.pause();
        }

        next_frame().await;
    }
}

fn lerp(start: f32, end: f32, t: f32) -> f32 {
    start + (end - start) * t
}
