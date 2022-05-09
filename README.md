# Python URL Shorterner


## Installation

Pre-requisites:

- Python

Install dependencies, create the SQLite database and run the flask application

```
  pip install -r requirements.txt
  flask run
```

You can access the application at 127.0.0.1:5000 or <your_domain>:5000.

## Features
- Login User
- Register User
- Convert link
- Get stats for individual or all link(s)
- Generate QR Code
- Get all links by a user
- Bulk link shortening using CSV
- Delete links
- Edit links
- Download QR code as SVG or PNG
- Add tags to links (9/5/2022)

## Pending Features

- Bulk export links
- Export link stats
- Separate stats by dates (Maybe try NoSQL?)
- Get location stats for clicks
- Get device stats for clicks
- Get browser stats for clicks
- Checks for duplicate create links
- Add error handling and validation checks