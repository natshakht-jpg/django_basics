"""
Простой веб-сервер для отдачи страницы "Контакты".
На GET-запрос / или /contacts возвращает страницу contacts.html.
На любой другой GET-запрос возвращает кастомную страницу 404.html.
На POST-запрос (отправка формы) выводит данные в консоль в читаемом виде.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote


class MyHandler(BaseHTTPRequestHandler):
    """
    Класс-обработчик HTTP-запросов.
    Содержит методы для обработки GET и POST запросов.
    """

    def do_GET(self):
        """
        Обработчик GET-запросов.
        / или /contacts -> contacts.html
        остальные адреса -> 404.html
        """
        if self.path == '/' or self.path == '/contacts':
            try:
                with open('contacts.html', 'r', encoding='utf-8') as f:
                    html = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, 'Файл contacts.html не найден')
        else:
            # Любой другой адрес — показываем 404.html
            try:
                with open('404.html', 'r', encoding='utf-8') as f:
                    html = f.read()
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, 'Страница не найдена')

    def do_POST(self):
        """
        Обработчик POST-запросов (отправка формы).
        Читает данные из формы, выводит их в консоль в читаемом виде,
        и отправляет браузеру сообщение об успехе.
        """
        # Получаем длину тела запроса
        content_length = int(self.headers.get('Content-Length', 0))

        # Читаем данные из запроса и декодируем в строку
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Выводим данные в терминал (декодируем русские буквы)
        print("Получены данные:", unquote(post_data))

        # Отправляем успешный ответ
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Отправляем простой ответ с ссылкой назад
        self.wfile.write(b'<h1>Form submitted</h1><a href="/">Back</a>')


def run():
    """
    Запускает сервер на localhost, порт 8080.
    Сервер работает до принудительной остановки (Ctrl+C).
    """
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('Сервер запущен на http://localhost:8080')
    print('Для остановки нажмите Ctrl+C')
    httpd.serve_forever()


# Точка входа: если файл запущен напрямую (а не импортирован)
if __name__ == '__main__':
    run()
