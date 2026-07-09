# ZimTechHub

Zimbabwe's Premier Technology Marketplace and Community Platform

## Features

- **Digital Marketplace** - Sell and buy code, templates, assets, courses
- **Project Showcase** - Display your open source and personal projects
- **Job Board** - Find tech jobs or hire talent
- **Freelance Services** - Offer and hire freelance services
- **Community Feed** - Share updates, code snippets, and discussions
- **Events** - Discover tech meetups, hackathons, and conferences
- **Professional Profiles** - Build your tech portfolio and network

## Tech Stack

- **Backend:** Python 3.13+, Django 5+, Django REST Framework
- **Frontend:** Tailwind CSS, Alpine.js, HTMX
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Cache/Queue:** Redis, Celery
- **Real-time:** Django Channels, WebSockets
- **Payments:** Paynow Zimbabwe, EcoCash, Stripe, PayPal

## Quick Start

1. **Clone and setup:**
```bash
git clone https://github.com/David-C23155849Q/ZimTech-Hub.git
cd ZimTech-Hub
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment variables:**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run migrations:**
```bash
python manage.py makemigrations accounts
python manage.py makemigrations marketplace
python manage.py makemigrations orders
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. **Start development server:**
```bash
python manage.py runserver
```

5. **Start Celery worker:**
```bash
celery -A config.celery worker -l info
```

## Docker Deployment

```bash
docker-compose up --build
```

## Project Structure

```
zimtechhub/
├── apps/
│   ├── accounts/       # Custom user model, authentication
│   ├── profiles/       # User profiles, follows, badges
│   ├── projects/       # Project showcase
│   ├── products/       # Digital marketplace
│   ├── posts/          # Community feed
│   ├── jobs/           # Job board
│   ├── services/       # Freelance marketplace
│   ├── companies/      # Company profiles
│   ├── events/         # Events management
│   ├── reviews/        # Review system
│   ├── wallet/         # User wallets
│   ├── dashboard/      # Seller dashboard
│   ├── api/            # REST API
│   └── core/           # Base models, utilities
├── config/             # Django settings
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── docker/             # Docker configuration
└── requirements.txt
```

## License

MIT License

made by David