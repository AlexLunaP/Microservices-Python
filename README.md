# Microservices-Python
My first Microservice-based application using Python.
This app is a** text analyser** that reads a text file and gets relevant statistics such as word frequencies, work length excluding digits and other punctuation marks.

The app consists of 4 microservices that read, analyse, store and display the results on a web.

The app has been developed using the following stack:
  - **Python** for writing the functionalities and **gRPC** for messages between microservices.
  - **Redis** for storing statistics.
  - **Flask** for displaying the results on a web.
  - **Docker** for orchestrating the app.
  - **Postman** and **Prometheus** for testing and metrics analysis.
