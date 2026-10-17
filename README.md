# Modu


**A virtual wardrobe and shopping app: scan your clothes, discover real items from Irish and UK shops, try outfits on your own avatar, and buy in one tap.**

DkIT Collaborative Project 2026/27       5-person team

---

## Table of Contents

- [Overview](#-overview)
- [Core Loop](#-core-loop)
- [System Architecture](#️-system-architecture)
- [AI](#-ai)
- [Catalogue](#️-catalogue)
- [Tech Stack](#️-tech-stack)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
- [Testing and Quality](#-testing-and-quality)
- [Contributors](#-contributors)
- [Resources](#-resources)

---

## Overview

Modu connects the clothes you already own with the clothes you might buy. You scan your wardrobe, the app learns your style, shows you real items from Irish and UK shops, and lets you see them on an avatar built from your own measurements before you spend anything.

**Target users (to be confirmed):** 

### Key Highlights

- **Try it on you:** mix your own clothes and saved items on an avatar fitted to your body
- **Your closet, styled:** recommendations built around what you already own
- **Our own models:** body, tagging and recommender models trained and evaluated by the team, not an API wrapper
- **Measured decisions:** every tech choice is backed by a comparison of accuracy, cost and time
- **Enforced security:** ownership tests on every route, CI from day one

---

## Core Loop

The scope is kept narrow on purpose:

1. **Scan your clothes.** Take a photo; Will be stored as personal item.
2. **For You feed.** Real items from Irish and UK shops. Save the ones you like.
3. **Try on.** Mix your own and saved clothes on your avatar. **"Make it real"** turns the outfit into a photoreal image.
4. **Buy.** A link opens the shop's product page.

---

##  System Architecture

**Currently on Development**


1. **App** (`app/`): the user-facing phone app. Talks only to the API.
2. **API** (`api/`): authentication, business logic, database, background jobs. The only component that calls the ML models and paid APIs.
3. **ML** (`ml/`): our own models, plus notebooks, training and evaluation.
4. **Database:** Postgres with pgvector for similarity search over item and outfit embeddings.

Only the API port is exposed. The database and models are internal.

---

## AI

| Model | What it does | Owner |
| --- | --- | --- |
| **Body** | The user types height and weight; a model trained on ANSUR II predicts the remaining measurements, and an Anny (or SMPL-X) body is fitted. The clad-body library (Apache 2.0) can be used here. 
| **Clothes tagging** | Background removal, FashionSigLIP / FashionCLIP tags, k-means colour. User corrections are saved as training data. Test set: a 200-photo closet shot by the team. 
| **Recommender** | Several strategies (closet, similar items, people like you, boards) plus a reranker by price range. Trained on the H&M Kaggle dataset. Hard filters (budget, size) run on the server before ranking. 
| **Try-on** | Free 2D preview on the avatar. "Make it real" uses Nano Banana (the only paid API, about $0.04 per image). 


---

##  Catalogue

**No scraping.** Items come from:

- **H&M Kaggle dataset:** demo and training
- **Affiliate feeds:** Awin (M&S, River Island, Nike), Rakuten (Mango), Vestiaire Collective for second-hand | TBC
- **Share-from-app:** the user shares an item from the H&M or Vinted app into Modu
- **Local shops** that give us permission | TBC 


---

## Tech Stack

Default stack. 

| App | API | Data | AI | DevOps |
| --- | --- | --- | --- | --- |
| Expo (React Native)<br/>Expo SecureStore for tokens | FastAPI (Python)<br/>One router per feature<br/>Alembic migrations | Postgres<br/>pgvector | ANSUR II body model, Anny / SMPL-X<br/>FashionSigLIP / FashionCLIP<br/>H&M recommender<br/>Nano Banana | Docker(TBC) <br/>GitHub Actions CI<br/>Protected `main`, PR reviews |

---

##  Repository Structure

```
Modu/
├── app/        Phone app (Expo / React Native)
├── api/        FastAPI server, database migrations, background jobs
├── ml/         Our models: notebooks, training, evaluation, inference
├── docs/       Architecture, decisions, Scrum, design and testing docs
└── .github/    Pull request and issue templates (CI workflows go here too)
```

Each folder has its own `README.md` with the setup for that component.

---

##  Getting Started

### Prerequisites

- Git
- Node.js LTS (app)
- Python 3.11+ (api, ml)
- Docker Desktop (running the full stack)


---

## Testing and Quality

- **Automated tests and CI from the start.** Tests run on every pull request.
- **Ownership tests:** every API route has a test proving a user cannot read or change another user's data.
- **AI evaluation:** each model is measured on accuracy, cost and time, with results kept in the repo.
- Every pull request explains **how to test it** before it can be reviewed.
- Bugs are reported with the **Bug report** issue template.

---

## Contributors

| Name | Role | GitHub |
| --- | --- | --- |
| Sofia | Project Manager, UI/UX (Figma) | TODO |
| Favour | Lead Frontend, Testing, AI (tagging and recommender) | TODO |
| Harris | Security, Backend | TODO |
| Cheryl | Backend, Database, Mahara | TODO |
| Iker Arza | Testing, Cloud and Deployment, AI (body model) | TODO |

---

## Resources

|  Portfolio (Mahara) |  Figma |  Screencast |  Scrumwise |
| --- | --- | --- | --- |
| TODO | TODO | TODO | TODO |

---


## Acknowledgments

- Dundalk Institute of Technology for project support
- ANSUR II, the H&M Personalized Fashion Recommendations dataset, and the clad-body library (Apache 2.0)
