import os
import time
import threading
import pyautogui
import keyboard
import re
from colorama import init, Fore, Style

init()  # инициализация colorama

f9_notification = "Отредактированный фон сохранен"
f10_notification = "Отредактированный чат сохранен"

def create_render_folder():
    render_path = os.path.join(os.getcwd(), "render")
    if not os.path.exists(render_path):
        os.makedirs(render_path)
        print("Создана папка 'render'.")

create_render_folder()

counter = 1
crop_size = (800, 800)  # Стандартный размер обрезки

def capture_screenshot():
    time.sleep(1)
    screenshot = pyautogui.screenshot()
    return screenshot

def crop_center(image, width, height):
    img_width, img_height = image.size
    left = (img_width - width) // 2
    top = (img_height - height) // 2
    right = left + width
    bottom = top + height
    return image.crop(left, top, right, bottom)

def save_image(image, save_path, counter, prefix="background"):
    filename = f"{prefix}{counter:00}.png"
    file_path = os.path.join(save_path, "render", filename)

    while os.path.exists(file_path):
        counter += 1
        filename = f"{prefix}{counter:00}.png"
        file_path = os.path.join(save_path, "render", filename)

    image.save(file_path)

def clear_background(image, save_path, counter):
    image = image.crop((76, 0, 1104, 373))
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []

    for item in data:
        if item[:3] == (0, 0, 0):
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)

    render_path = os.path.join(os.getcwd(), "render")
    if not os.path.exists(render_path):
        os.makedirs(render_path)
        print("Создана папка 'render'.")

    filename = f"chat{counter:03}.png"
    file_path = os.path.join(render_path, filename)

    while os.path.exists(file_path):
        counter += 1
        filename = f"chat{counter:03}.png"
        file_path = os.path.join(render_path, filename)

    time.sleep(0.5)

    image.save(file_path)

    return file_path

def get_user_size():
    user_input = input("Введите размер обрезки (например, 800x600): ")

    pattern = re.compile(r'^\d{2,4}x\d{2,4}$')
    while not pattern.match(user_input):
        print("Неверный формат. Попробуйте еще раз.")
        user_input = input("Введите размер обрезки (например, 800x600): ")

    width, height = map(int, user_input.split('x'))
    return width, height

def user_input_thread():
    global crop_size
    while True:
        user_input = input()
        if user_input.startswith("/size"):
            try:
                size_params = user_input.split()[1]
                width, height = map(int, size_params.split('x'))
                crop_size = (width, height)
                print(f"Размер обрезки изменен на {width}x{height}")
            except (IndexError, ValueError):
                print(f"{Fore.RED}Неверный формат команды /size. Используйте /size ШИРИНАxВЫСОТА{Style.RESET_ALL}")

input_thread = threading.Thread(target=user_input_thread)
input_thread.daemon = True
input_thread.start()

def main():
    global counter 
    global crop_size  

    print("Clear Screen by Rockfield:\n")
    print(f"{Fore.GREEN}F9 - отредактировать фон{Style.RESET_ALL}")
    print(f"{Fore.GREEN}F10 - отредактировать чат{Style.RESET_ALL}")
    print(f"{Fore.GREEN}/size - изменить  размер обрезки фона{Style.RESET_ALL}")

    while True:
        if keyboard.is_pressed("F9"):
            screenshot = capture_screenshot()
            cropped_image = crop_center(screenshot, crop_size[0], crop_size[1])
            save_image(cropped_image, os.getcwd(), counter)
            counter += 1
            print(f"{f9_notification}")

            time.sleep(2)

        if keyboard.is_pressed("F10"):
            keyboard.press("F6")
            time.sleep(0.1)
            keyboard.release("F6")

            time.sleep(0.1)
            keyboard.write("/ss 2")
            time.sleep(0.1)
            keyboard.press("Enter")
            time.sleep(0.1)

            time.sleep(0.5)

            screenshot = capture_screenshot()

            try:
                processed_image_path = clear_background(screenshot, os.getcwd(), counter)
                print(f"{f10_notification}")

                counter += 1

                keyboard.press("F6")
                time.sleep(0.5)
                keyboard.release("F6") 
                keyboard.write("/ss 0")
                time.sleep(0.1)
                keyboard.press("Enter")
                time.sleep(5)
                keyboard.release("Enter")

            except Exception as e:
                print("Ошибка в процессе обработки:", str(e))

        time.sleep(0.1)

if __name__ == "__main__":
    main()