import os
import cv2
import numpy as np
import zmq
import time
import logging


class ImagePublisher:
    def __init__(self, address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(address)

    def __del__(self):
        self.socket.close()
        self.context.term()

    def publish_image(self, image):
        _, encoded_image = cv2.imencode('.jpg', image)
        self.socket.send(encoded_image.tobytes())


def generate_random_image(width, height):
    image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return image


def main():
    width, height = 640, 480
    address = os.getenv("PUB_URI", "tcp://*:5555")
    publisher = ImagePublisher(address)

    # Configure logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Log publisher address
    logger.info(f"Image publisher is running on: {address}")

    last_log_time = time.time()
    try:
        while True:
            random_image = generate_random_image(width, height)
            publisher.publish_image(random_image)

            current_time = time.time()
            elapsed_time = current_time - last_log_time

            if elapsed_time > 5:
                last_log_time = current_time
                logger.info("Heartbeat")
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt -- Shutting down")


if __name__ == "__main__":
    main()
