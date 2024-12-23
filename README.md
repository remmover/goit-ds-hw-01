# Phone Bot

## 💡 Description
This project is a bot for managing contacts, including:
- Adding contacts.
- Updating existing contacts.
- Searching contacts by name or phone number.
- Displaying all saved contacts.

The bot is written in Python and uses Docker for containerization.

---

## 🔧 How to Run the Project

### 1. **Install Docker**
Ensure Docker is installed and running on your system.
```bash
docker --version
```
If Docker is not installed, download and install it from the [official Docker website](https://www.docker.com/).

---

### 2. **Clone the Project**
Clone the repository or copy the project files to your local directory.

---

### 3. **Build the Docker Image**
1. Navigate to the directory containing the `Dockerfile`.
2. Run the following command to build the image:
   ```bash
   docker build -t phone-bot .
   ```
   - `-t phone-bot`: this is the tag (name) for the image.
   - `.` specifies the current directory.

---

### 4. **Run the Docker Container**
To run the container:
```bash
docker run -it phone-bot
```
- `-it`: runs the container in interactive mode, allowing you to input commands for the bot.

---

### 5. **Interact with the Bot**
Once the container is running, the bot is ready for use. Use the following commands to interact with it:

#### Main Commands:
- `hello`: Responds with “Hello, how can I help you?”.
- `add <name> <phone> [<dd.mm.yyyy>]`: Adds a new contact with the given name, phone number, and optionally, birth date.
- `change <name> <new_phone>`: Updates the phone number of an existing contact.
- `phone <name>`: Displays the phone number for the specified contact.
- `show all`: Shows all saved contacts.
- `help`: Displays a list of available commands.
- `good bye`, `close`, `exit`: Ends the bot’s operation.

---

### 6. **Stop the Container**
To stop the container, press `Ctrl+C` or run the following command:
```bash
docker stop <container_id>
```
To find the `container_id`, use:
```bash
docker ps
```

---

### 7. **View Logs (Optional)**
To view container logs:
```bash
docker logs <container_id>
```

---

## 📋 Requirements
- Python >= 3.12
- Docker
- Poetry for dependency management (used in `pyproject.toml`).

---

## 👤 Author
Ihor Moroz  
Email: ihorm.200323@gmail.com

