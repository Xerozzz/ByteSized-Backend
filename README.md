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
- Login User (18/04/2022)
- Register User (18/04/2022)
- Convert link (18/04/2022)
- Get stats for individual or all link(s) (28/04/2022)
- Generate QR Code (28/04/2022)
- Get all links by a user (28/04/2022)
- Bulk link shortening using CSV (28/04/2022)
- Delete links (28/04/2022)
- Edit links (28/04/2022)
- Download QR code as SVG or PNG (28/04/2022)
- Add tags to links (09/05/2022)

## Pending Features
- Bulk export links (will be done on frontend)
- Export link stats
- Separate stats by dates (Maybe try NoSQL?)
- Get location stats for clicks
- Get device stats for clicks
- Get browser stats for clicks
- Checks for duplicate create links
- Add error handling and validation checks