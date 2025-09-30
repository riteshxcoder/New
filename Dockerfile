FROM nikolaik/python-nodejs:python3.10-nodejs20

# Replace old Debian repos with archive repos
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list \
    && sed -i '/security.debian.org/d' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/

# Copy pyproject.toml first
COPY pyproject.toml /app/

# Install dependencies from pyproject.toml
RUN pip install .

# Copy rest of the repo
COPY . /app/

CMD bash start
