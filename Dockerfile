# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres

# Expose the default PostgreSQL port
EXPOSE 5432

RUN apt-get update && \
        apt-mark hold locales && \
        apt-get install -y --no-install-recommends build-essential postgresql-server-dev-$PG_MAJOR git ca-certificates && \
        cd /tmp && \
        git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git && \
        cd pgvector && \
        make clean && \
        make OPTFLAGS="" && \
        make install && \
        mkdir /usr/share/doc/pgvector && \
        cp LICENSE README.md /usr/share/doc/pgvector && \
        rm -r /tmp/pgvector && \
        apt-get remove -y build-essential postgresql-server-dev-$PG_MAJOR && \
        apt-get autoremove -y && \
        apt-mark unhold locales && \
        rm -rf /var/lib/apt/lists/*

# You can also add an initialization script if needed
COPY init.sql /docker-entrypoint-initdb.d/

# No additional commands needed, as the official image already includes a default entrypoint to run PostgreSQL
