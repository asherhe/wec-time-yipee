import socket

HOST = "127.0.0.1"
PORT = 8800

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        for _ in range(24):
            conn.sendall(b"""\
{
  "random_event": "none",
  "forecast": "not cloudy",
  "loads": [
{ "type": "library", "load": 20 },
{ "type": "lecture_hall", "load": 30 },
{ "type": "student_residence", "load": 50 },
{ "type": "lecture_hall", "load": 20 }],
  "grid_price" : 1.2
}""")
            data = conn.recv(1024)
            print(data)

