ARG DOCKER_PYTHON_VERSION
FROM python:${DOCKER_PYTHON_VERSION}

ARG SPHINX_SOURCE_DIR
ARG SPHINX_BUILD_DIR
ARG SPHINX_EXEC_DIR
ARG SPHINX_APP_DIR
ARG SPHINX_SOURCE_DIR_RELATIVE

# Set the environment variables so they are available during build for Makefile
ENV SPHINX_SOURCE_DIR=${SPHINX_SOURCE_DIR}
ENV SPHINX_BUILD_DIR=${SPHINX_BUILD_DIR}

# Install required packages
RUN apt-get update && apt-get install -y make curl

# Set the working directory
WORKDIR ${SPHINX_APP_DIR}

# Copy the project files into the container
COPY ${SPHINX_SOURCE_DIR_RELATIVE} ${SPHINX_APP_DIR}

# Install Python packages via requirements.txt
RUN cd ${SPHINX_EXEC_DIR} && pip install --upgrade pip && pip install -r requirements.txt

# Build the HTML documentation using Sphinx with the defined directories
RUN cd ${SPHINX_EXEC_DIR} && make html

# Expose port 8000 where the HTTP server will run
EXPOSE 8000

# Start a simple HTTP server to serve the built documentation
CMD python -m http.server 8000 --directory "${SPHINX_BUILD_DIR}html/"
