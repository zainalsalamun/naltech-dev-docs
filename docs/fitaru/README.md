# Fitaru

**Fitaru** adalah aplikasi diet santai untuk mencatat makan, olahraga, air minum, berat badan, dan progres tubuh harian secara realistis.

Tagline:

```text
Diet santai, progres tetap jalan.
```

## Project Stack

- Mobile app: Flutter
- Admin CMS: Next.js
- Database/Auth/Storage: Supabase
- API MVP: Next.js Route Handlers

## Repository Structure

```text
.
├── mobile/
├── admin/
├── supabase/
│   ├── migrations/
│   ├── seed/
│   └── policies/
├── packages/
│   ├── api-contracts/
│   └── design-tokens/
└── docs/
    ├── product/
    ├── design/
    ├── api/
    ├── planning/
    └── mockups/
```

## Documentation

Product:

- [Product Document](docs/product/FITARU_PRODUCT_DOCUMENT.md)
- [Wireframe](docs/product/FITARU_WIREFRAME.md)

Design:

- [Design System](docs/design/FITARU_DESIGN_SYSTEM.md)
- [Mobile Dashboard Design](docs/design/FITARU_DASHBOARD_DESIGN.md)
- [Admin CMS Design](docs/design/FITARU_ADMIN_CMS_DESIGN.md)

API and database:

- [Database Schema](docs/api/FITARU_DATABASE_SCHEMA.md)
- [API Endpoints](docs/api/FITARU_API_ENDPOINTS.md)
- [Initial SQL Migration](supabase/migrations/202605180001_initial_schema.sql)

Planning:

- [MVP Backlog](docs/planning/FITARU_MVP_BACKLOG.md)
- [Tech Stack and Project Structure](docs/planning/FITARU_TECH_STACK_AND_PROJECT_STRUCTURE.md)

Mockups:

- [UI Mockup Notes](docs/mockups/FITARU_UI_MOCKUP.md)
- [Mobile Mockup HTML](docs/mockups/fitaru-mockup.html)
- [Mobile Dashboard HTML](docs/mockups/fitaru-dashboard.html)
- [Admin CMS HTML](docs/mockups/fitaru-admin-cms.html)

## Development Roadmap

1. Scaffold admin CMS with Next.js.
2. Scaffold mobile app with Flutter.
3. Setup Supabase project and run migration.
4. Implement auth.
5. Implement mobile dashboard and tracking flows.
6. Implement admin CMS overview and content management.
7. Add RLS policies and smoke tests.

