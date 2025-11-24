FROM python:3.10-slim

LABEL maintainer="Zhou <zhou.joe.lan@gmail.com>"
LABEL version="1.0"
LABEL description="Docker image for FMQ regression quantile analysis with compatible pyvista/vtk versions"

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/ ./app/


LABEL maintainer="Zhou (Joe) Lan <zhou.joe.lan@gmail.com>"
LABEL version="1.0"
LABEL description="Fiber microstructure quantile (FMQ) regression for White Matter Analysis"



# Install numpy first so its headers are available
RUN pip install --no-cache-dir numpy==1.24.0

# Now install everything else
RUN pip install --no-cache-dir \
    vtk==9.5.0 \
    pyvista==0.42.3 \
    pandas==2.0.3 \
    scikit-learn==1.6.1 \
    pyqreg==0.4.2 \
    patsy==1.0.1 \
    scipy==1.15.2

ENTRYPOINT ["python", "app/Estimation.py"]