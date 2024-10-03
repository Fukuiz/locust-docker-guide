# Use the official Locust image as the base image
FROM locustio/locust

# Copy the Locust script into the container
COPY basic_http_post.py /locustfile.py

# Set the default command to run when the container starts
CMD ["locust", "-f", "/locustfile.py"]
