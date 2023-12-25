"""
Модуль для сжатия изображений
"""

from PIL import Image, ImageDraw

from tree import QuadTree


def create_image(quadtree: QuadTree, level: int,
                 borders: bool) -> Image:
    """
    Создает изображение
    :param quadtree: Квадродерево
    :param level: Уровень глубины
    :param borders: Отображение границ
    :return: Сжатое изображение
    """
    image = Image.new('RGB', (quadtree.width, quadtree.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, quadtree.width, quadtree.height), (0, 0, 0))
    leaf_nodes = quadtree.get_leaf_nodes(level)

    for node in leaf_nodes:
        if borders:
            draw.rectangle(node.coordinate_region, node.average_color,
                           outline=(0, 0, 0))
        else:
            draw.rectangle(node.coordinate_region, node.average_color)

    return image


def image_compression(image_path: str, level: int, borders: bool) -> None:
    """
    Метод для сжатия изображения
    :param image_path: Путь до изображения
    :param level: Уровень глубины
    :param borders: Отображение границ
    :param gif: Нужно ли создавать gif изображение
    """
    image = Image.open(image_path)
    quadtree = QuadTree(image)

    file_extension = image_path.split('.')[-1]
    file_name = image_path.split('\\')[-1]

    final_image = create_image(quadtree, level, borders)
    final_image.save(f"pictures\\compressed_{file_name}.{file_extension}")
    print("Изображение успешно сохранено")



