# S1E7 - Nave a la Deriva 🚀

[View Challenge](https://makers-challenge.altscore.ai/s1e7)

## Context
Year 2315. You're trapped in a spaceship drifting in deep space. The navigation systems are damaged and energy is running out fast. By sheer luck, you detect an unmanned repair robot approaching on radar. Your only hope is to simulate a distress call for the robot to find and repair your ship.

## The Challenge
Create an API that meets the following requirements:

## Endpoints

- `GET /status` → `{ "damaged_system": "engines" }`
- `GET /repair-bay` → HTML page with `<div class="anchor-point">ENG-04</div>`
- `POST /teapot` → HTTP 418 with `{ "detail": "I'm a teapot" }`
- `GET /healthz` → `{ "status": "ok" }`

## Solution

This project implements a FastAPI that meets the challenge requirements:

### API Endpoints

1. **First Call: GET /status**
   Returns a JSON object with the damaged system:
   ```json
   {
     "damaged_system": "engines"
   }
   ```

2. **Second Call: GET /repair-bay**
   Generates a simple HTML page containing a `<div>` with the class "anchor-point" and the code corresponding to the damaged system.
   
   Example for damaged engine system:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>Repair</title>
   </head>
   <body>
   <div class="anchor-point">ENG-04</div>
   </body>
   </html>
   ```

3. **Third Call: POST /teapot**
   Returns HTTP status code 418 (I'm a teapot).

## Technical Requirements
- Docker
- Docker Compose

## Running the Solution

1. First, start the application in one terminal:

```bash
make build
make up
```

2. In another terminal, run the solution script:

```bash
python summit_solution.py
```

If successful, you should see output similar to:
```
{'first_check_complete': True, 'second_check_complete': True, 'third_check_complete': True}
```

**Important Notes:**
- The `summit_solution.py` script requires the `NGROK_APP_URL` to be updated with your ngrok URL
- Find your ngrok URL at http://localhost:4040 after starting the application
- The URL changes each time you restart the containers

## Deployment with Docker

You can deploy the application using Docker Compose:

```bash
# From this directory
make build
make up
# or directly: docker compose up --build
```

The app will be available at http://localhost:8002 (host) → forwards to container port 8000. Access logs are enabled.

Stop:
```bash
make down
```

## Testing

Tests run inside the Docker container:

```bash
# Build the image (only needed the first time or after dependency changes)
make build

# Run tests
make test
# or with verbose output
make test-verbose
```

## Exposing with ngrok (Optional)

This project includes an `ngrok` service in `docker-compose.yml`.

1. Create a `.env` file from the example and set your token:

```bash
cp .env.example .env
# Edit the .env file and set your ngrok token
```

2. Start the application with ngrok:

```bash
docker compose up --build
```

3. Access the ngrok web interface to get your public URL:

- http://localhost:4040

Notes:
- The app is exposed on host port 8002; ngrok creates an internal tunnel to `nave-a-la-deriva:8000`
- You can also run ngrok directly on your machine: `ngrok http http://localhost:8002`
