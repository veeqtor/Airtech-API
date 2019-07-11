# Set Base image
FROM python:3.7.0-slim

# Set Maintainer
LABEL maintainer="Victor Nwokeocha"

# Python unbuffered env and python dont write byte code variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade and install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Make and cd into a dir to store app source code
RUN mkdir /airtech-api
WORKDIR /airtech-api

# Copy the pipfiles to the work directory.
COPY ./Pipfile /airtech-api
COPY ./Pipfile.lock /airtech-api

# Install dependencies
RUN pipenv install --system --deploy --ignore-pipfile

# Copy all the other files/folders to airtech-api
COPY . /airtech-api

RUN chmod +x /airtech-api/Docker_local/start.sh

# Create a user to run the app on docker
# Necessary for security reasons
RUN useradd -r -u 1234 -U docker-user

# Change the ownership of the working dir to the new user
# and give write access to the folder.
RUN chown -R docker-user:docker-user /airtech-api
RUN chmod 755 /airtech-api

# Switch to the new user
USER docker-user

# Expose port 9000
EXPOSE 9000

# Run the start script.
CMD sh Docker_local/start.sh
