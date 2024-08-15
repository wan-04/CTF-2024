# Use an alpine python image as the base image:
    FROM python:3.11.8-slim

    # Specify the working directory:
    WORKDIR /app
    
    # Copy relevant files into the docker container:
    COPY . .
    
    # Setup a ctf user
    RUN groupadd -r ctf && useradd -r -m -g ctf ctf
    
    # Give the ctf user permissions to relevant directories
    RUN chmod -R 544 server.py
    RUN chmod 600 requirements.txt
    RUN chown -R ctf:ctf /app
    
    # Change to the ctf-user context
    USER ctf
    
    # Add the required python modules (-> using the ctf-user, because pip warns about issues when running as root...):
    RUN pip install -r requirements.txt
    
    # Command to run the script
    CMD ["python", "/app/server.py"]
    
    # Declare the required port
    EXPOSE 6668/tcp
    