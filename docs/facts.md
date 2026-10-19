# modu system architecture

![modu architecture](architecture.png)

You can edit the diagram by opening:
https://excalidraw.com/#json=emM27aCyYjIGitOruHnrZ,k6bvx05Aj-GLQ9x1Xdf1zA

## How it works

The user uses the modu app on their phone. The app is made with Expo and React Native, so we can have it on iPhone, Android and also as a PWA if we want. Expo is like a wrapper around React Native, kind of like Vite for web, it gives us the tools to test and build the app.

Everything the app does goes with HTTPS to one server on AWS (EC2 instance). Inside the server everything runs in Docker containers with Docker Compose.

Caddy is the front door. Its the only thing open to the internet, on port 443. It does the HTTPS and sends every request to the backend.

The backend is FastAPI. It checks who the user is, checks that the stuff they ask for is really theirs, and talks with all the other parts.

The AI service has our own models. The body model makes the avatar from the height and weight, the clothes tagger cuts out the clothes and puts the tags and the colour, and the recommender makes the For You feed. Only the backend can talk to it.

MySQL saves the users, clothes, tags, embeddings and the try on jobs. Only the backend can talk to it too.

There is also a small worker that does the try on in the background, so the app dont have to wait. The app just checks every few seconds if the image is ready.

Outside the server we have:

Amazon S3 for the photos. MySQL only saves where each photo is.

Google Sign In for the login, so we dont save any passwords.

Google Gemini Nano Banana for the "Make it real" image. This is the only thing we pay every time we use it, around $0.04 for each image.

Maybe a second AI that checks the image before the user sees it. Right now I propose Claude Haiku but we still need to confirm this cuz its optional, is more like a double check that Nano Banana did the work good.

GitHub Actions runs the tests and the security scans and then deploys every change to the server. Its more safe and its how we show real testing and CI, which Stockd didnt show.

## Why we arent saving photos in the database

Photos are big. One photo from a phone is like 1 to 4 MB, and one row of data is only a few KB. If we have 30 testers with 50 clothes each, thats already more than 4 GB just in photos.

If we put the photos inside MySQL the database gets really big. MySQL tries to keep the data it uses the most in the RAM, so in a server with 4 GB the photos will push the real data out and everything gets slow. Also every image the app shows has to go through the backend, so the backend spends its CPU and RAM just copying images instead of doing the real work, and the backup every night takes minutes instead of seconds.

With S3, MySQL stays small and fast because it only keeps the path of the photo. The app downloads the photos straight from S3 with a link that only works for a few minutes, and the backend makes that link after checking the photo belongs to that user. So the bucket stays private and the backend CPU is free. And if the server breaks the photos are still safe, and the database backup is in S3 too.

## Ports

**Caddy HTTPS:** 443, public, the only way in

**Caddy HTTP:** 80, public, it only sends you to HTTPS

**Backend FastAPI:** 8000, internal

**AI service:** 8001, internal

**MySQL:** 3306, internal

**Expo dev server:** 8081, only on our laptops when we develop

**SSH:** 22, only for the deploys and only with a key

**S3, Google Sign In and Gemini:** 443, HTTPS going out from the server

## Easy to learn workflow of the app

The user taps something in the app, for example "show my clothes", and the app sends a request with HTTPS to our server.

Caddy gets the request on port 443, takes off the HTTPS and sends it as normal HTTP to Uvicorn inside the server. Uvicorn is listening on port 8000, it gets the request and gives it to FastAPI.

FastAPI looks at the route, for example /items, and runs the function for that route. That function checks the user token and that the stuff is theirs, reads or saves in MySQL, and gets a link to the photos in S3. If the route needs AI it calls the AI service on port 8001, for example to make the avatar, tag a piece of clothes or rank the For You feed. If its "Make it real" it saves a job and the worker does it in the background with Gemini.

When the function is done, FastAPI turns the answer into JSON and gives it back to Uvicorn. Uvicorn passes it to Caddy, Caddy wraps it again in HTTPS and sends it back to the app, and the app shows it to the user.

**Short version:** app -> Caddy -> Uvicorn -> FastAPI -> route -> MySQL, S3 or AI if needed -> JSON back -> Caddy -> app

## Hosting options compared on cost

The prices are more or less per month, I checked them this month (October 2026).

**Oracle Cloud Always Free, 2 CPU and 12 GB RAM:** free, but a lot of times you cant create the server because there is no capacity, and they cut the free limits in June 2026 from what I found

**AWS EC2 t4g.medium, 2 CPU and 4 GB RAM:** around $33, free for up to 6 months with the AWS free plan credits of $100 to $200

**AWS EC2 t4g.large, 2 CPU and 8 GB RAM:** around $60, the credits last around 3 months

**Azure for Students B2s, 2 CPU and 4 GB RAM:** around $33, the $100 student credit lasts around 3 months

**Hetzner CAX21, 4 CPU and 8 GB RAM:** it was around €11 but now its not available

**Railway, one service with 4 GB:** around $40 or more

**DigitalOcean:** the student credit finished in August 2026

**Hugging Face Spaces:** Docker apps need a paid plan now

Best option for us is AWS EC2 t4g.medium. Its what Stockd used last year, everything stays in one place with AWS, and the free credits cover it from Alpha to Expo if we open the account when Alpha starts.

Other costs: Gemini is around $0.04 for each "Make it real" image, so more or less $75 for the whole year if we use it a lot. S3 is a few cents per month (around 2 cents per GB per month). The domain is free for one year with the GitHub Student Pack. All the rest is free.

## Stack proposed

**App:** Expo React Native, it can be a PWA too

**Server:** one AWS EC2 instance, t4g.medium, with Docker Compose to separate things in 5 containers: Caddy for HTTPS, the backend with FastAPI, the worker for the try on jobs, the AI service with our models and MySQL. That way when we need to restart something we dont have to restart everything

**Front door:** Caddy with free HTTPS from Let's Encrypt

**Backend:** FastAPI and Uvicorn, with a worker for the try on jobs

**AI service:** our own models, the body model, the clothes tagger with rembg and FashionSigLIP, the recommender, and FAISS for similar items

**Database:** MySQL 8.4

**Photos:** Amazon S3

**Login:** Google Sign In

**Paid AI:** Google Gemini Nano Banana for "Make it real", and maybe a check of the result with Claude Haiku

**CI/CD:** GitHub Actions with tests, security scans and deploy
