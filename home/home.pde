/**
 *
 * Home 
 *
 * Reflection on time and change through colors
 * Creates linear animation of pixel values
 * from 4 polaroid images 
 * taken after long absences
 * from home
 * 
 * Maoya Bassiouni
 * September 2011.
 *
 */


PImage img;
int direction = 1;

float position;

void setup() {
  size(1393, 422);
  stroke(255);
  frameRate(22);
  img = loadImage("/Users/maoya/Desktop/polashome/polaall.png");
  img.loadPixels();
  loadPixels();
}

void draw() {
  if (position > img.height-1 || position < 0) { 
    direction = direction * -1; 
  }
    position += (0.3 * direction);  

    int position_ext = int(position) * img.width;
    for (int y  = 0; y < img.height; y++) {
      arrayCopy(img.pixels, position_ext, pixels, y * width, img.width);
    }
    updatePixels();
  
}

