from django.test import LiveServerTestCase
import numpy as np
from selenium import webdriver
from Screenshot import Screenshot
from datetime import date
import os
import cv2

class ScreenshotTestCase(LiveServerTestCase):
    screenshots_path = f"/home/qroot/Documents/projects/django_screenshot/tests/screenshots/{date.today()}/"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()  # Use appropriate WebDriver here

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # def test_screenshot(self):
    #     self.selenium.get(self.live_server_url)

    #     if not os.path.exists(self.screenshots_path):
    #         os.mkdir(self.screenshots_path)

    #     Screenshot.Screenshot().full_screenshot(
    #         driver=self.selenium,
    #         save_path=self.screenshots_path,
    #         image_name='screenshot.png',
    #         is_load_at_runtime=True,
    #     )

    def test_image_comparison(self):
      self.selenium.get(self.live_server_url)

      if not os.path.exists(self.screenshots_path):
          os.mkdir(self.screenshots_path)

      Screenshot.Screenshot().full_screenshot(
          driver=self.selenium,
          save_path=self.screenshots_path,
          image_name='screenshot.png',
          is_load_at_runtime=True,
      )
      
      # Load the reference image
      reference_image = cv2.imread('/home/qroot/Documents/projects/django_screenshot/tests/screenshots/etalon.png')

      # Load the screenshot image
      screenshot_image = cv2.imread('/home/qroot/Documents/projects/django_screenshot/tests/screenshots/2023-06-07/screenshot.png')

      # Resize the images to have the same dimensions
      reference_image = cv2.resize(reference_image, (screenshot_image.shape[1], screenshot_image.shape[0]))

      # Convert the images to grayscale
      reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
      screenshot_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)

      # Compare the grayscale images
      difference = cv2.absdiff(reference_gray, screenshot_gray)

      # Apply thresholding to convert the difference to binary image
      _, binary_image = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

      # Apply morphological operations to group small differences
      kernel = np.ones((15, 15), np.uint8)
      dilated_image = cv2.dilate(binary_image, kernel, iterations=1)
      eroded_image = cv2.erode(dilated_image, kernel, iterations=1)

      # Find contours of the grouped differences
      contours, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding rectangles around the grouped differences
      for contour in contours:
          (x, y, w, h) = cv2.boundingRect(contour)
          cv2.rectangle(screenshot_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

      # Display or save the result
      cv2.imwrite('/home/qroot/Documents/projects/django_screenshot/tests/screenshots/comparison.png', screenshot_image)



    
