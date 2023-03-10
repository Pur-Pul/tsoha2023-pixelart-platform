[Project specification](documentation/project_specification.md)

[Production server](https://pixel-art.fly.dev/)   
**_NOTE:_** The production server has a problem where it loses connection to the database after a time of inactivity. Therefore it might throw an internal server error the first time a user connects in a while. This is fixed by simply retrying the request.

## Installation
Clone this repository and create a .env file in the root directory.

### Contents of .env:
```bash
DATABASE_URL=<url-to-the-local-database>
SECRET_KEY=<the-secret-key-for-the-database>
```

Create the virtual environment with the following command:
```bash
$ python3 -m venv venv
```

### Activate the virtual environment:  
Linux:
```bash
$ source venv/bin/activate
```
Windows command prompt:
```bash
$ venv\Scripts\activate.bat
```
Windows PowerShell:
```bash
$ venv\Scripts\Activate.ps1
```

The following commands should be run in the venv.

Install requirements by running the following command:
```bash
$ pip install -r requirements.txt
```

Start the program using the following command:
```bash
$ invoke start
```

Pylint can be run with the following command:
```bash
$ invoke lint
```

Testing and coverage report:
```bash
$ invoke test
```

## Functionality
This application is a platform for creating and sharing pixel-art.
### Current features
- Password protected accounts.
- A navigation bar to easily move between pages.
- Pixel-art editor made in javascript.
- The contents of the editor is actively saved to the database, which means the editor can be closed and resumed at any point.
- Artworks in the editor can be saved to the profile at any point.
    - Colors can be selected using sliders for red, green and blue.
    - Features pencil, color-picker tool and undo/redo. (Only one redo-state at the moment)
- Artworks saved to profile are viewable at the users own profile page.
- Artworks saved to profile can be saved as a post with a freely formulated title in the database.
    - Posts are viewable on the /posts -page. 
    - Posts can be liked and disliked. (One vote per user)
    - The /posts -page can be sorted to show: new, old or popular posts. (Popular sorted by the sum of likes and dislikes)
    - A search bar can be used to find posts based on title.
    - Users can leave replies on posts, which are viewable under /post/post-id.
- When artworks are loaded in on the editor, profile and post pages, they are animated to be redrawn in the order the image was drawn, stroke by stroke.

### Potential features to add.
- Replies and votes to other replies.
- Limit number of undo states in the editor to prevent slowdown.
- Increase number of redo states.