import os
import time
import zmq
import logging


def main():
    sub_uri = os.getenv("SUB_URI", "tcp://localhost:5555")
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(sub_uri)
    socket.setsockopt(zmq.SUBSCRIBE, b"")  # Subscribe to all messages

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info("Application started.")

    message_count = 0
    total_time = 0
    total_size = 0
    last_log_time = time.time()

    try:
        while True:
            try:
                message = socket.recv()
                message_size = len(message)

                current_time = time.time()
                elapsed_time = current_time - last_log_time

                message_count += 1
                total_time += elapsed_time
                total_size += message_size

                if elapsed_time >= 5:
                    mean_time = elapsed_time / message_count
                    mean_size = total_size / message_count

                    logger.info(f"Mean time between messages: {mean_time*1000.0:.3f} ms")
                    logger.info(f"Mean message size: {mean_size/1000.0:.2f} kB")

                    message_count = 0
                    total_time = 0
                    total_size = 0
                    last_log_time = current_time

            except zmq.error.Again:
                continue

    except KeyboardInterrupt:
        pass

    socket.close()
    context.term()

    logger.info("Application closed.")


if __name__ == "__main__":
    main()
