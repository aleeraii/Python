import threading
import socket
import math
import time
import numpy as np
import matplotlib.pyplot as plt

NUM_OF_PORTS = 65535
ports_scanned = [False] * NUM_OF_PORTS
HOST = 'https://www.hackthissite.org/'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def scan_port(port):
    """This function tries to connect to the given port.
    It returns True if can, False otherwise."""
    if port <= 0 or port > NUM_OF_PORTS:
        return
    try:
        s.connect((HOST, port))
        return True
    except:
        return False


def scan_range(start, end):
    ports_scanned[0] = True
    """Scans a range of ports"""
    for port in range(start, end+1):
        if scan_port(port):
            try:
                scan_port(port)
                ports_scanned[port] = True
            except IndexError:
                pass


def threaded_scan(num_of_threads):
    """This functions scans all 65535 ports using the given number of threads.
    Each thread scans almost the same number of ports."""
    ports = []
    ports_per_thread = int(NUM_OF_PORTS / num_of_threads)
    for i in range(num_of_threads + 1):
        x = i * ports_per_thread
        ports.append(x)

    start_port = ports[0] + 1
    end_port = ports[1]
    p = 1
    thread_list = []
    for i in range(num_of_threads):
        t = threading.Thread(target=scan_range, name='thread{}'.format(i), args=(start_port, end_port))
        t.start()
        thread_list.append(t)
        p += 1
        start_port = end_port + 1
        try:
            end_port = ports[p]
        except IndexError:
            pass
    for t in thread_list:
        t.join()


def main():
    """Times how long it takes to scan all ports using different numbers of threads.
    Checks that all ports are scanned in each case."""
    num_of_threads = [1, 2, 3, 4, 5, 10, 20, 30, 50, 100, 500, 1000, 2000, 5000, 10000]
    time_list = []
    for i in num_of_threads:
        start = time.time()
        threaded_scan(i)
        end = time.time()
        time_taken = round(end - start, 2)
        time_list.append(time_taken)
        print("Scanning {0} ports using {1} thread(s): {2} seconds.".format(NUM_OF_PORTS, i, time_taken))
    y_pos = np.arange(len(time_list))
    plt.bar(y_pos, time_list, align='center', alpha=0.5)
    plt.xticks(y_pos, num_of_threads, rotation='vertical', ha="right")
    plt.ylabel("Time")
    plt.xlabel("Threads")
    plt.title("Scanning {0} Ports".format(NUM_OF_PORTS))
    plt.show()

if __name__ == "__main__":
    main()