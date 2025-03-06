
# Trivia Game

## Overview

This project is a multiplayer trivia game built using Python. It consists of a client-server architecture that enables users to connect, login, and play trivia questions while keeping track of scores.

## Features

- User authentication (login/logout).
- Trivia question fetching and answering.
- Score tracking
- High-score leaderboard
- Display logged-in users
- Multi-client support using TCP sockets

## Project Structure

```
Trivia
├── client.py              # Client-side implementation
├── server_skeleton.py     # Server-side implementation (single-client)
├── server_multi_tcp.py    # Server-side implementation (multi-client)
├── chatlib_skeleton.py    # Chat protocol library
```

## Installation & Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/RoyShemTov23/Trivia.git
   cd Trivia
   ```
2. Run the server:
   ```sh
   python server_multi_tcp.py
   ```
3. Run the client:
   ```sh
   python client.py
   ```

## How to Play

1. Start the server.
2. Start the client and log in with a username ("test") and password ("testing").
3. Choose an action from the menu:
   - `p` to play a trivia question
   - `s` to get your score
   - `h` to view the high-score table
   - `l` to list logged-in users
   - `q` to quit the game

## Protocol Details

The project uses a custom chat protocol defined in `chatlib_skeleton.py`. Messages are structured with command headers and data fields separated by delimiters.

## Dependencies

- Python 3.x

## License

This project is licensed under the MIT License.




**Author:** Roy Shem Tov

**GitHub:** [https://github.com/RoyShemTov23/Trivia](https://github.com/RoyShemTov23/Trivia)

**Contact:** [royshemt@gmail.com](mailto:royshemt@gmail.com)

