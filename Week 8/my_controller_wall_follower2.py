"""my_controller_wall_follower2 controller."""

# Mengimpor kelas Robot dari modul controller, yang digunakan untuk mengontrol robot
from controller import Robot

def run_robot(robot):
    """Wall-following robot."""

    # Mendapatkan nilai timestep dari dunia simulasi.
    # Timestep adalah interval waktu yang digunakan Webots untuk memperbarui simulasi.
    timestep = int(robot.getBasicTimeStep())
    max_speed = 6.28  # Kecepatan maksimum roda robot (default e-puck).

    # Konfigurasi motor
    # Motor digunakan untuk mengontrol pergerakan roda kiri dan kanan.
    # `getDevice` mengambil perangkat berdasarkan nama yang didefinisikan di Webots.
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    # Set posisi motor ke `inf` agar roda berputar terus menerus.
    # Jika tidak diatur, motor akan mencoba mencapai posisi tertentu (tidak cocok untuk penggerak kontinu).
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)  # Mengatur kecepatan awal motor kiri ke nol.
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)  # Mengatur kecepatan awal motor kanan ke nol.

    # Mengaktifkan sensor jarak (proximity sensors).
    # Sensor ini digunakan untuk mendeteksi keberadaan dinding atau objek di sekitar robot.
    prox_sensors = []  # Membuat daftar kosong untuk menyimpan sensor.
    for ind in range(8):  # Sensor e-puck memiliki 8 proximity sensors (ps0 hingga ps7).
        sensor_name = 'ps' + str(ind)  # Nama sensor sesuai dengan definisi di Webots.
        # Menambahkan setiap sensor ke daftar dan mengaktifkannya dengan timestep.
        prox_sensors.append(robot.getDevice(sensor_name))
        prox_sensors[ind].enable(timestep)

    # Loop utama
    # Loop ini berjalan terus menerus selama simulasi aktif.
    while robot.step(timestep) != -1:
        # Membaca nilai dari semua sensor jarak.
        # Sensor menghasilkan nilai yang lebih besar jika objek lebih dekat.
        for ind in range(8):
            print("ind: {}, val: {}".format(ind, prox_sensors[ind].getValue()))

        # Memproses data dari sensor untuk memutuskan arah gerakan robot.
        # `getValue()` membaca nilai jarak dari masing-masing sensor.
        left_wall = prox_sensors[5].getValue() > 80  # Sensor ps5 (sisi kiri).
        left_corner = prox_sensors[6].getValue() > 80  # Sensor ps6 (sudut kiri).
        front_wall = prox_sensors[7].getValue() > 80  # Sensor ps7 (depan).

        # Default kecepatan: maju lurus.
        left_speed = max_speed
        right_speed = max_speed

        # Logika utama pengendalian robot:
        if front_wall:  # Jika ada dinding di depan (sensor depan mendeteksi objek dekat).
            print("Turn Right in place")  # Log tindakan ke konsol.
            # Robot berbelok kanan di tempat dengan memutar roda kiri maju
            # dan roda kanan mundur.
            left_speed = max_speed
            right_speed = -max_speed
        elif left_wall:  # Jika ada dinding di sisi kiri.
            print("Drive Forward")  # Log tindakan ke konsol.
            # Robot berjalan lurus mengikuti dinding di sisi kiri.
            left_speed = max_speed
            right_speed = max_speed
        elif left_corner:  # Jika terlalu dekat dengan sudut kiri.
            print("Close to the Wall, drive right")  # Log tindakan ke konsol.
            # Robot sedikit berbelok ke kanan untuk menjaga jarak dari dinding.
            left_speed = max_speed
            right_speed = max_speed / 8
        else:  # Jika tidak ada dinding di depan atau di sisi kiri.
            print("Turn Left")  # Log tindakan ke konsol.
            # Robot berbelok ke kiri untuk mencari dinding.
            left_speed = max_speed / 8
            right_speed = max_speed

        # Mengirim perintah ke motor untuk mengatur kecepatan roda.
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

# Bagian ini memastikan program hanya berjalan saat dijalankan langsung, 
# bukan saat diimpor sebagai modul ke program lain.
if __name__ == "__main__":
    # Membuat instance robot dari kelas Robot.
    my_robot = Robot()
    # Menjalankan fungsi utama untuk memulai robot.
    run_robot(my_robot)
