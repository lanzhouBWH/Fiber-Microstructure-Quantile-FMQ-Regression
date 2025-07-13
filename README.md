# Fiber Microstructure Quantile (FMQ) Regression

This repository provides a Dockerized pipeline implementing the *Fiber Microstructure Quantile (FMQ) Regression* model, as proposed in:

Lan, Z., Chen, Y., Rushmore, J., Zekelman, L., Makris, N., Rathi, Y., Golby, A.J., Zhang, F. and O’Donnell, L.J., 2025. Fiber microstructure quantile (FMQ) regression: A novel statistical approach for analyzing white matter bundles from periphery to core. Imaging Neuroscience, 3, p.imag_a_00569. https://doi.org/10.1162/imag_a_00569

The FMQ model enables microstructural statistical analysis for white matter fiber tracts using diffusion MRI data. It estimates quantile-specific effects of clinical or demographic covariates on scalar microstructural measures (e.g., FA), providing a novel statistical approach for analyzing white matter bundles from periphery to core.

This pipeline accepts vtp-format tractography data and subject metadata, and outputs quantile regression coefficient estimates, standard error, and p-values.

---

## Run with Docker (Personal Computer Users)

### 1. 🐳 Install and Pull Docker

If you don’t have Docker installed, follow the instructions for your OS:

- **Mac/Linux**: https://docs.docker.com/desktop/
- **Windows**: https://docs.docker.com/desktop/install/windows-install/

Once Docker is installed, pull the image:

```bash
docker pull lanzhou1126/fmq_regression:latest
```

---

### 2. 📂 Prepare Input and Output Folders

You need two folders:

#### Example input structure:
```
Input/
├── FiberTracts/         # Folder with VTP tractography files (*.vtp)
└── subject_data.csv     # Metadata file used in regression
```

You can use the sample `Input/` provided in this repository.

#### Example output structure (empty to start):
```
Output/
```


---

### 3. 🚀 Run the Analysis via Docker

Run the container using:

```bash
docker run \
  -v /absolute/path/to/Input:/data/input \
  -v /absolute/path/to/Output:/data/output \
  lanzhou1126/fmq_regression:latest \
  --input_dir /data/input \
  --output_dir /data/output \
  --tau_all 0.05,0.1,0.25,0.5,0.75,0.9
```

- Replace paths with full paths on your machine.
- You can modify `tau_all` for different quantile levels.

---

### 4. 📊 Check Output

After the container finishes, check the `Output/` folder. You will see:

```
Output/
└── FMQ_Result.csv     # Quantile regression results
```



## Run with Singularity (Linux HPC Users)

If you're using a high-performance computing (HPC) system that supports [Singularity](https://sylabs.io/singularity/), you can run this Docker image as a Singularity container:

### Step 1: Pull and convert Docker image

```bash
module load singularity
singularity build fmq_regression.sif docker://lanzhou1126/fmq_regression:latest
```

### Step 2: Run the container

```bash
singularity run \
  -B /absolute/path/to/Input:/data/input \
  -B /absolute/path/to/Output:/data/output \
  fmq_regression.sif \
  --input_dir /data/input \
  --output_dir /data/output \
  --tau_all 0.05,0.1,0.25,0.5,0.75,0.9
```

> Note: Replace paths with full directories. `-B` is used to bind host directories into the container.

---

