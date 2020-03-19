# Thesis Subject: *"A web application with AI bot for Νine Μen's Μorris board game"*

The project's code is in the [web_app_edition folder](https://github.com/JohnPapad/Thesis/tree/master/web_app_edition).  
A [terminal edition](https://github.com/JohnPapad/Thesis/tree/master/terminal_edition) (does not contain online PvP mode) is also included.

### Table of Contents

[Abstract](#abstract)

[Project Summary](#summary)

[Contributors](#contributors)

[Task Separation](#taskSep)

[The Stack](#stack)

[Tools Used](#tools)

[How to install](#install)

[How to run](#run)


<a name="abstract"/>

# Abstract

The purpose of this project is to implement a web application with GUI (Graphical User
Interface) for Nine Men's Morris board game. The user can play in real time, remotely,
against either other users or an AI bot, running on the server side. Additionally, it aims in
studying the minimax decision-making algorithm with an optimization technique, called
Alpha-Beta Pruning, and finding efficient heuristic functions, for the purpose of
implementing the aforementioned AI bot.
The procedure followed, started with the in-depth understanding of the game rules and its
restrictions. Thereafter, the game’s basic logic and its necessary mechanisms
(moving-removing pieces, changing players’ turn, win-lose conditions etc) was
implemented in the python programming language and tested in terminal, without GUI. In
this context, the AI bot was coded and tested for its performance. Afterwards, the web
app’s user interface (front-end) was build using the React JS Library and the server side
(back-end) using the Django Web Framework, integrating the already developed python
code. Finally, the messages’ structure, used by the communication protocols (REST API,
WebSocket), was determined and communication between front and back end was
enabled.
The end result is a user friendly application that works seamlessly on every device
(smartphones, laptops, PCs etc). Players can search for an opponent through the
matchmaking feature. The AI bot performs at a good level, that can win against
experienced players.


<a name="summary"/>

# Project Summary

Nine Men’s Morris Online is a web application for playing the Nine Men’s Morris board
game either against another player or a AI bot, that uses a decision making algorithm. The
overall application is composed of 2 distinguished apps: the front and the back end. The
back-end is developed with python, using the Django Web Framework and the front-end is
developed with JSX and CSS, using the React JS Library. The back-end runs on WSGI
server, whereas the front-end runs on nodeJS server. Due to the RESTful architecture the
2 apps are completely independent from one another, and can be served from different
domains, if desired. They can be also developed, maintained and expanded separately
and even replaced with other web/JS frameworks, such as Spring and Vue JS
respectively; as long as the communication messages’ JSON structure remains the same.
The AI algorithm, is encapsulated in the back-end. PostgreSQL database was used for
normal data storage (e.g users’ info). However, this kind of database would not be efficient
enough for multiple retrieves and insertions, needed during multiple game sessions.
Therefore, redis a in-memory data structure store, was chosen for this particular task.
Apart from standard HTTP requests (GET, PUT etc), a real time bi-directional
communication between front and back end, so that every game action (e.g. placing,
moving pieces) to being executed concurrently, was necessary. So, the websocket
protocol was chosen.



<a name="contributors"/>

# Contributors

[Ioannis Papadopoulos](https://github.com/JohnPapad)

[Rafail Chatzidakis](https://github.com/RafaelChatz)


<a name="taskSep"/>

# Task Separation

## Ioannis Papadopoulos
Worked on implementing the whole UI interface, the front-end part of the project, using the ReactJS framework. Also mainly implemented the AI bot, using the minimax decision-making algorithm with the Alpha-Beta Pruning optimization technique, alongside with efficient heuristic functions.

## Rafail Chatzidakis
Worked on implementing the whole back-end part of the project, which includes the API (Django REST Framework), database (PostgreSQL) and websocket (Django channels) implementation. Also provided assistance on the AI bot part.


<a name="stack"/>

# The Stack

![stack image](thesis_tech_stack.png "The Stack")


<a name="tools"/>


# Tools used

- **React JavaScript Library** (for front-end)
  
  - Router-dom (for routing)
  - reactstrap (for UI)
  - axios (for HTTP requests)
  - Redux (for state management)
  - Immer (for fast and easy state manipulation)
  - Sass (for UI styling)

- **Django REST Framework** (for API)
  - channels (for websockets)
  - CORS headers (to allows in-browser requests to the Django application from other origins)

- **PostgreSQL** (for data storage)
- **Redis** (for efficient data storage and retrieval during games)
- **Docker** (for easy installation and future deployment)


<a name="install"/>

# How to install

Docker and docker-compose must be installed.   
Follow the instructions from the [official docker site](https://docs.docker.com/install/).


<a name="run"/>

# How to run
```docker-compose up --build```