import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import re

from scipy.ndimage import gaussian_filter

nametypes = [
    'd_left_cc',
    'd_right_mlo',
    'd_left_mlo',
    'd_right_cc',

    'e_left_cc',
    'e_right_mlo',
    'e_left_mlo',
    'e_right_cc',

    'f_left_cc ',
    'f_right_mlo',
    'f_left_mlo',
    'f_right_cc',

    'g_left_cc ',
    'g_right_mlo',
    'g_left_mlo',
    'g_right_cc',
]


class ImageMetadata():
    def __init__(self, image, path):
        self.image = image
        self.path = path
        self.filename = os.path.basename(path)
        self.BIRAD_TYPE = self._get_birad_type()
        self.side = self._get_side()
        self.orientation = self._get_orientation()

    def _get_side(self):
        left = re.search('left', self.filename)
        if left:
            return 'left'
        elif re.search('right', self.filename):
            return 'right'
        else:
            print('Orientacao invalida')
            exit()

    def _get_orientation(self):
        left = re.search('cc', self.filename)
        if left:
            return 'cc'
        elif re.search('mlo', self.filename):
            return 'mlo'
        else:
            print('Orientacao invalida')
            exit()

    def _get_birad_type(self):
        if self.filename[0] == 'd':
            return 1
        elif self.filename[0] == 'e':
            return 2
        elif self.filename[0] == 'f':
            return 3
        elif self.filename[0] == 'g':
            return 4
        else:
            print('Valor invalido de birad!')
            exit()


def region_growth(image_array, seed_point, threshold):
    # Cria uma máscara vazia
    mask = np.zeros_like(image_array, dtype=np.uint8)

    # Pega as dimensões da imagem
    height, width = image_array.shape

    # Pega as coordendadas da seed
    seed_x, seed_y = seed_point

    # Checa se a seed está nos limites da imagem
    if seed_x < 0 or seed_x >= width or seed_y < 0 or seed_y >= height:
        raise ValueError("Seed fora da imagem")

    # Pega a intensidade do seed point
    seed_intensity = image_array[seed_y, seed_x]

    # Cria uma fila para guardar os pixels a serem processados
    queue = [(seed_x, seed_y)]

    # seta a flag processada para o seed
    processed = np.zeros_like(image_array, dtype=bool)
    processed[seed_y, seed_x] = True
    # Cresimento de região
    while queue:
        x, y = queue.pop(0)

        mask[y, x] = 255
        # Checagem de pixels vizinhos
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                # Checa se o pixel vizinho está nos limites da imagem
                if nx >= 0 and nx < width and ny >= 0 and ny < height:
                    # Checa se os pixels vizinhos não foram processados
                    if not processed[ny, nx]:
                        # Pega a intensidade do pixel vizinho
                        intensity = image_array[ny, nx]
                        # Checa se a diferença de intensidade está abaixo do threshold
                        if abs(int(intensity) - int(seed_intensity)) <= threshold:
                            # Adiciona o pixel vizinho na fila
                            queue.append((nx, ny))
                            # Seta a flag processada para o pixel vizinho
                            processed[ny, nx] = True
    mask[~processed] = 0
    return mask


def otsu(image):
    # Computação do histograma
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 256])
    total_pixels = image.size

    # Calcula a probabilidade de cada nível de intensidade
    prob = hist / total_pixels

    # Calcula a soma cumulativa de probabilidades
    cum_sum = np.cumsum(prob)

    # Calcula a soma cumulativa das intensidades
    cum_intensity = np.cumsum(prob * np.arange(256))

    # Calcula a intensidade da média global
    global_mean = cum_intensity[-1]

    best_threshold = 0
    best_variance = 0

    for t in range(256):
        # Probabilidade de background e foreground
        w0 = cum_sum[t]
        w1 = 1 - w0

        if w0 == 0 or w1 == 0:
            continue

        # Intensidade media de background e foreground
        mean0 = cum_intensity[t] / w0
        mean1 = (global_mean - cum_intensity[t]) / w1

        # Calcula a soma entre a variancia das classes
        between_variance = w0 * w1 * ((mean0 - mean1) ** 2)

        # Checa se a variavel eh um maximo
        if between_variance > best_variance:
            best_variance = between_variance
            best_threshold = t

    # Cria a imagem binarizada
    binary_image = image > best_threshold

    return binary_image


def crop(image):
    return image[30:image.shape[0] - 30, 30:image.shape[1] - 30]


def get_mask(image, image_metadata):
    process_imgs = []
    process_names = []

    dilate_kernel = np.ones((5, 5), np.uint8)
    # otsu
    mask = otsu(image)
    process_imgs.append(mask)
    process_names.append('otsu')

    # dilatacao
    mask = mask.astype(np.uint8) * 255
    mask = cv2.dilate(mask, dilate_kernel, iterations=1)
    process_imgs.append(mask)
    process_names.append('Dilatacao')

    # filtro gaussiano
    mask = gaussian_filter(mask.astype(float), sigma=2)
    process_imgs.append(mask)
    process_names.append('gaussian_filter')

    # erosao
    mask = mask.astype(np.uint8) * 255
    erode_kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, erode_kernel, iterations=2)
    process_imgs.append(mask)
    process_names.append('Erosion')

    # crescimento de regiao
    if image_metadata.side == 'right':
        seed = (mask.shape[1]-20, mask.shape[0]//2)
    else:
        seed = (0, mask.shape[0]//2)

    mask = region_growth(mask, seed, 10)
    process_imgs.append(mask)
    process_names.append('Region Growth')

    return mask  # Image.fromarray(preprocessed)


def process_image(image, url):

    image_metadata = ImageMetadata(image, url)
    # transforma a pil image para np_arr
    image_arr = np.array(image)
    # Crop e resize
    preprocessed = crop(image_arr)
    preprocessed = cv2.resize(preprocessed, (256, 512))
    # Sobreposicao da mascara
    mask = get_mask(preprocessed, image_metadata)
    preprocessed = cv2.bitwise_and(preprocessed, mask)
    return preprocessed
