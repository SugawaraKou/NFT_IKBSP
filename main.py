from random import choices
import os
from typing import List, Tuple
from PIL import Image


def get_files_from_folder(path: str, with_none: bool = False) -> str:
    '''
    Извлекает все файлы из папки

    :param path:  //TODO
    :param with_none: //TODO
    :returns: //TODO
    '''
    pictures: List[str] = []
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file():
                if entry.name.endswith('.png'):
                    pictures.append(entry.path)
    return pictures


def generate_img(result_img: str, elements: List[Tuple[str, List[int], bool]],
                 elements_for_repainting: List[str], pic_num: str = '') -> None:

    # список выпавших элементов для описания
    desc_items: List[str] = []

    for element in elements:
        name, weights, with_none = element
        items = get_files_from_folder(name, with_none=with_none)
        print(items)
        item = choices(items, weights)[0]
        print(item)

        if item != 'None':
            if name.find('Фон') != -1:
                result_img = item
            else:
                desc_items.append(item)  # записали элемент
                result_img = apply_layer_to_image(result_img, item)  # накладываем слой

    os.rename(result_img, str(pic_num) + result_img)
    make_desc_file(str(pic_num) + result_img, desc_items)


def make_desc_file(picture: str, items: List[str]) -> None:
    '''
    Записывает слои, из которых состоит изображение

    :param picture:  //TODO
    :param items:  //TODO
    :returns: //TODO
    '''
    FILE_EXSTENSION = '.txt'
    # 1.png 1 + '.txt'
    picture_file_txt: str = picture.split('.')[0] + FILE_EXSTENSION
    with open(picture_file_txt, 'w') as file:
        for item in items:
            print(item)
            item_without_num: str = item.split('_')[1]
            item_without_num_and_extension: str = item_without_num.split('.')[0]
            file.write(item_without_num_and_extension + "\n")


def apply_layer_to_image(original_img_path: str, layer_img_path: str, path_to_save: str = '') -> str:
    '''
    Накладывает одно изображение на другое

    :param original_img_path:  //TODO
    :param layer_img_path: //TODO
    :param path_to_save:  //TODO
    :returns: A path for new img
    '''

    IMG_POSTFIX = '_res.png'

    original_img: Image.Image = Image.open(original_img_path).convert("RGBA")
    layer_img: Image.Image = Image.open(layer_img_path).convert("RGBA")

    x, y = layer_img.size

    original_img.paste(layer_img, (0, 0, x, y), layer_img)

    path_to_save = path_to_save if path_to_save else IMG_POSTFIX
    original_img.save(path_to_save)

    return path_to_save


def clear_tmp_files(path: str) -> None:
    '''
    Очистить временные файлы
    '''
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file():
                if entry.name.find('_') != -1:
                    os.remove(entry.path)


# устанавливаем рабочую директорию
os.chdir(os.path.dirname(__file__))


def main(count_of_images):

    probability_wieghts_background = [1, 1, 1]  # вероятности фона
    probability_wieghts_body = [4, 3, 2]  # вероятности тела
    probability_wieghts_acc = [1, 1, 1]  # вероятности аксессуаров

    # (Название папки с элементом рисунка, список вероятностей для каждого элемента, может ли не выпасть элемент)
    elements = [('Фон/', probability_wieghts_background, False), ('Тело/', probability_wieghts_body, False),
                ('Аксессуары/', probability_wieghts_acc, True)]
    # список элементов, которые надо перекрашивать
    elements_for_repainting = []
    # итоговое изображение
    result_img = ''

    for i in range(1, count_of_images + 1):
        generate_img(result_img, elements, elements_for_repainting, i)
        # чистим временные файлы, которые создаются при перекрашивании
        for element in elements_for_repainting:
            clear_tmp_files(element)


if __name__ == '__main__':
    try:
        COUNT_OF_IMAGES = 3
        main(COUNT_OF_IMAGES)
    except KeyboardInterrupt:
        exit()