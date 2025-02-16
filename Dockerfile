FROM python:3.9

LABEL maintainer="senrhonie@gmail.com"
# Set environment variables to avoid interactive prompts during package installation
# ENV DEBIAN_FRONTEND=noninteractive

# # Update and install Python and other dependencies
# RUN apt-get update && apt-get install -y \
#     python3 \
#     python3-pip \
#     && apt-get clean

# Set the working directory
WORKDIR /prod-app

# Copy all necessary files
COPY qb_live.txt ./qb_live.txt
COPY streaming-data.py ./streaming-data.py
COPY main.py ./main.py
COPY requirements.txt ./requirements.txt
COPY run.sh ./run.sh

# Ensure run.sh has executable permissions
RUN chmod +x ./run.sh

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8501

# Run the script
CMD ["./run.sh"]
# ENTRYPOINT ["sh"]