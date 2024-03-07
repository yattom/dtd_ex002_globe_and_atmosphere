import math
import numpy as np
from PIL import Image, ImageDraw


# reference: https://github-nakasho.github.io/astroelec/rayleigh
# recreating formula (23) - (25)

def save_image(image):
    # Save the image to a file
    image.save("image.png")
    print("Image saved successfully.")


class Simulation:
    # 大気の屈折率 n
    ATMOSPHERIC_REFRACTIVITY_INDEX = 1.0003

    # 誘電体球半径 a
    RADIUS_OF_PERCITLE = 1.0e-9  # 1.0 nano meter

    # ナノメートル (nm)
    NANOMETER = 1.0e-9

    # 大気のスケールハイト μ
    ATMOSPHERE_HEIGHT_SCALE = 100.0 * 1000

    # 大気密度(分子数) 常温常圧海面高度 N0
    MOLECULE_COUNT_BASE = 2.6867811e25  # per cubic meter

    @staticmethod
    def relative_perticle_density(altitude):
        '''
        >>> Simulation.relative_perticle_density(0)
        1.0
        >>> Simulation.relative_perticle_density(10 * 1000)
        0.9048374180359595
        >>> Simulation.relative_perticle_density(500 * 1000) < 0.01
        True
        '''
        return math.pow(math.e, -altitude / (Simulation.ATMOSPHERE_HEIGHT_SCALE))

    @staticmethod
    def scattering_cross_section(wavelength):
        '''
        >>> red = 650 * Simulation.NANOMETER
        >>> blue = 470 * Simulation.NANOMETER
        >>> red_scatter = Simulation.scattering_cross_section(red)
        >>> blue_scatter = Simulation.scattering_cross_section(blue)
        >>> red_scatter < blue_scatter
        True
        '''
        n = Simulation.ATMOSPHERIC_REFRACTIVITY_INDEX
        a = Simulation.RADIUS_OF_PERCITLE
        return ((128 * math.pi ** 5 / 3)
                * (((n ** 2 - 1) / (n ** 2 + 2)) ** 2)
                * (a ** 6 / wavelength ** 4))

    @staticmethod
    def light_diminishment(altitude, travel_length, wavelength):
        '''
        >>> red = 650 * Simulation.NANOMETER
        >>> blue = 470 * Simulation.NANOMETER
        >>> red_light = Simulation.light_diminishment(0, 1000 * 1000, red)
        >>> 0.99 < red_light < 1.0
        True
        >>> blue_light = Simulation.light_diminishment(0, 1000 * 1000, blue)
        >>> blue_light < 0.99
        True
        >>> red_light > blue_light
        True
        '''
        sigma = Simulation.scattering_cross_section(wavelength)
        mu = Simulation.ATMOSPHERE_HEIGHT_SCALE
        N0 = Simulation.MOLECULE_COUNT_BASE
        return math.exp(-sigma * mu * N0 * math.pow(math.e, -altitude / mu))



def draw_ray(image):
    draw = ImageDraw.Draw(image)
    light = np.array([255, 255, 255])
    for z in range(500, 0, -10):
        l = light[:]
        l[0] *= Simulation.light_diminishment(z * 1000, 1, 610 * Simulation.NANOMETER)
        l[1] *= Simulation.light_diminishment(z * 1000, 1, 550 * Simulation.NANOMETER)
        l[2] *= Simulation.light_diminishment(z * 1000, 1, 450 * Simulation.NANOMETER)
        draw.rectangle([(z - 10, 0), (z, 100)], tuple(light))


def main():
    image = Image.new(mode='RGB', size=(800, 600))
    draw_ray(image)
    save_image(image)


if __name__=='__main__':
    main()
