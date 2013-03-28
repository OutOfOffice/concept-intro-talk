'''

Portrait of John Cage

using a b&w image as a score for sounds

Maoya Bassiouni (December 2011)

'''


from numpy import pi, array, linspace, int16, sin
from scipy.io import wavfile
import Image
import scipy.stats.mstats
import itertools


class Viz(object):
    def __init__(self):
        self.number_gradient = [0, 8, 9, 6, 5, 3, 2, 1]
        self.quantiles = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    def buildArray(self, file):
        return array(Image.open(file))

    def convert_pixel_to_number_gradient(self, pixel):
        x = self.number_gradient[0]
        for i, q in enumerate(self.pixel_quantiles):
            if pixel > q:
                x = self.number_gradient[i]
            else:
                break
        return x

    def write_pixels_to_number_gradient(self, file, out_file):
        f_out = open(out_file, 'a')
        image_array = self.buildArray(file)
        self.pixel_quantiles = scipy.stats.mstats.mquantiles(image_array, prob=self.quantiles)
        for i, line in enumerate(image_array):
            for pixel in line:
                f_out.write('{0}'.format(self.convert_pixel_to_number_gradient(pixel)))
            f_out.write('\r\n')
        f_out.close()


class Sound(object):
    def __init__(self):
        self.chromatic_scale = [440, 466, 494, 523, 554, 587, 622, 659, 698, 740, 784, 831, 880]
        self.major_scale = [0, 440, 494, 554, 587, 659, 740, 831]
        self.viz = Viz()

    def convert_pixel_to_freq(self, pixel):
        x = self.major_scale[0]
        for i, q in enumerate(self.pixel_quantiles):
            if pixel > q:
                x = self.major_scale[i]
            else:
                break
        return x

    def pixel_to_notes(self, pixel, amp=7000.):
        freq = self.convert_pixel_to_freq(pixel)
        notes = sin(2. * pi * freq * self.t) * amp
        return notes.astype(int16)

    def image_to_melody(self, file, note_length, rate=6400):
        image_pixels = list(itertools.chain(*self.viz.buildArray(file)))
        print len(image_pixels)
        self.pixel_quantiles = scipy.stats.mstats.mquantiles(image_pixels, prob=self.viz.quantiles)
        self.t = linspace(0, note_length, note_length * rate)
        melody = map(self.pixel_to_notes, image_pixels)
        return list(itertools.chain(*melody))

    def write_wave_image(self, file, out_file, note_length, rate=6400):
        melody = array(self.image_to_melody(file, note_length, rate=rate))
        print len(melody)
        wavfile.write(out_file, rate, melody)


if __name__ == "__main__":

    import os
    viz = Viz()
    sound = Sound()
    directory = "/Users/maoya/Desktop/OOO/sounds"
    image_file = os.path.joint(directory, "John_Cage.jpg")
    out_file_txt = os.path.joint(directory, "number_gradient.txt")
    out_file_wave = os.path.joint(directory, "john_cage.wav")
    note_length = 0.17
    viz.write_pixels_to_number_gradient(image_file, out_file_txt)
    #sound.write_wave_image(image_file, out_file_wave, note_length, rate=6400)
