# Fitaru API Endpoints

Dokumen ini berisi rancangan API endpoint untuk aplikasi mobile Fitaru dan admin CMS.

## API Style

Rekomendasi untuk MVP:

- REST API
- JSON request/response
- Auth menggunakan Bearer token
- Mobile user dan admin memakai role berbeda
- Response error dibuat konsisten

Base URL contoh:

```text
https://api.fitaru.app/v1
```

## Standard Response

Success:

```json
{
  "data": {},
  "meta": {}
}
```

Error:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input belum lengkap.",
    "details": {}
  }
}
```

## Auth

Jika memakai Supabase Auth, sebagian endpoint auth bisa langsung memakai Supabase SDK. Endpoint di bawah ini tetap dicatat sebagai kontrak produk.

### POST /auth/register

Mendaftarkan user baru.

Request:

```json
{
  "email": "raka@email.com",
  "password": "secret123",
  "displayName": "Raka"
}
```

Response:

```json
{
  "data": {
    "userId": "uuid",
    "accessToken": "token"
  }
}
```

### POST /auth/login

Login user.

Request:

```json
{
  "email": "raka@email.com",
  "password": "secret123"
}
```

### POST /auth/logout

Logout user.

### POST /auth/admin/login

Login admin CMS.

Request:

```json
{
  "email": "admin@fitaru.app",
  "password": "secret123"
}
```

## Mobile App Endpoints

## Profile

### GET /me

Mengambil data user yang sedang login.

Response:

```json
{
  "data": {
    "id": "uuid",
    "email": "raka@email.com",
    "profile": {
      "displayName": "Raka",
      "goal": "lose_weight",
      "dietStyle": "relaxed",
      "heightCm": 170,
      "currentWeightKg": 74.8,
      "targetWeightKg": 68
    }
  }
}
```

### PUT /me/profile

Update profil user.

Request:

```json
{
  "displayName": "Raka",
  "gender": "male",
  "birthYear": 1996,
  "heightCm": 170,
  "currentWeightKg": 74.8,
  "targetWeightKg": 68,
  "goal": "lose_weight",
  "dietStyle": "relaxed",
  "activityLevel": "light"
}
```

### GET /me/targets

Mengambil target harian user.

### PUT /me/targets

Update target harian user.

Request:

```json
{
  "waterGlassesTarget": 8,
  "exerciseWeeklyTarget": 3,
  "calorieTarget": null,
  "weighInDays": ["monday", "thursday"],
  "isCalorieTrackingEnabled": false
}
```

## Mobile Dashboard

### GET /dashboard/today

Mengambil ringkasan dashboard hari ini.

Query:

```text
date=2026-05-18
```

Response:

```json
{
  "data": {
    "date": "2026-05-18",
    "consistencyScore": 62,
    "summary": {
      "mealsLogged": 2,
      "mealTarget": 4,
      "waterGlasses": 5,
      "waterTarget": 8,
      "exerciseMinutes": 0,
      "lastWeightKg": 74.8,
      "weeklyWeightChangeKg": -0.4
    },
    "nextAction": {
      "type": "exercise",
      "message": "Belum olahraga hari ini. Jalan 10 menit juga tetap progres."
    },
    "timeline": [
      {
        "type": "meal",
        "time": "08:10",
        "title": "Sarapan",
        "description": "Roti gandum, telur"
      },
      {
        "type": "meal",
        "time": "12:35",
        "title": "Makan siang",
        "description": "Nasi ayam, sayur"
      }
    ]
  }
}
```

## Meal Logs

### GET /meal-logs

Mengambil daftar catatan makan user.

Query:

```text
date=2026-05-18
```

### POST /meal-logs

Membuat catatan makan.

Request:

```json
{
  "foodItemId": null,
  "mealTime": "lunch",
  "foodName": "Nasi ayam, sayur",
  "portionSize": "medium",
  "estimatedCalories": null,
  "photoUrl": null,
  "note": "Porsi nasi setengah",
  "loggedAt": "2026-05-18T12:35:00+07:00"
}
```

### GET /meal-logs/:id

Mengambil detail catatan makan.

### PUT /meal-logs/:id

Update catatan makan.

### DELETE /meal-logs/:id

Menghapus catatan makan.

## Exercise Logs

### GET /exercise-logs

Mengambil daftar catatan olahraga.

Query:

```text
date=2026-05-18
```

### POST /exercise-logs

Membuat catatan olahraga.

Request:

```json
{
  "exerciseItemId": null,
  "exerciseName": "Jalan kaki",
  "durationMinutes": 30,
  "intensity": "medium",
  "estimatedCaloriesBurned": 110,
  "note": "Jalan sore",
  "loggedAt": "2026-05-18T17:20:00+07:00"
}
```

### PUT /exercise-logs/:id

Update catatan olahraga.

### DELETE /exercise-logs/:id

Menghapus catatan olahraga.

## Weight Logs

### GET /weight-logs

Mengambil riwayat berat badan.

Query:

```text
from=2026-05-01&to=2026-05-18
```

### POST /weight-logs

Membuat catatan berat badan.

Request:

```json
{
  "weightKg": 74.8,
  "progressPhotoUrl": null,
  "note": "Tidur agak kurang",
  "loggedAt": "2026-05-18T07:00:00+07:00"
}
```

### DELETE /weight-logs/:id

Menghapus catatan berat badan.

## Water Logs

### GET /water-logs

Mengambil catatan air minum.

Query:

```text
date=2026-05-18
```

### POST /water-logs

Menambah catatan air minum.

Request:

```json
{
  "glasses": 1,
  "loggedAt": "2026-05-18T15:20:00+07:00"
}
```

### DELETE /water-logs/:id

Menghapus catatan air minum.

## Progress

### GET /progress/summary

Mengambil ringkasan progress user.

Query:

```text
period=week
```

Response:

```json
{
  "data": {
    "period": "week",
    "weightChangeKg": -0.4,
    "exerciseSessions": 2,
    "mealLogDays": 5,
    "averageConsistencyScore": 68,
    "insight": "Kamu lebih rapi mencatat makan siang minggu ini."
  }
}
```

### GET /progress/weight-chart

Mengambil data chart berat badan.

Query:

```text
from=2026-05-01&to=2026-05-18
```

## Content

### GET /articles

Mengambil artikel published untuk aplikasi.

Query:

```text
category=makan-santai&page=1&limit=10
```

### GET /articles/:slug

Mengambil detail artikel.

## Reference Data

### GET /food-items

Search database makanan aktif.

Query:

```text
q=nasi&page=1&limit=20
```

### GET /exercise-items

Search database olahraga aktif.

Query:

```text
q=jalan&page=1&limit=20
```

## Feedback

### POST /feedback

Mengirim feedback dari user.

Request:

```json
{
  "type": "suggestion",
  "subject": "Tambah makanan lokal",
  "message": "Tolong tambahkan gado-gado dan soto."
}
```

## Admin CMS Endpoints

Semua endpoint admin wajib memakai admin auth dan role permission.

## Admin Overview

### GET /admin/overview

Mengambil ringkasan dashboard CMS.

Response:

```json
{
  "data": {
    "stats": {
      "totalUsers": 12480,
      "activeUsersToday": 2918,
      "mealLogsToday": 8764,
      "feedbackNew": 37
    },
    "userGrowth": [
      { "date": "2026-05-12", "users": 11800 },
      { "date": "2026-05-13", "users": 11960 }
    ],
    "topFoods": [
      { "name": "Nasi ayam", "logs": 2184 },
      { "name": "Bakso", "logs": 1462 }
    ],
    "recentFeedback": []
  }
}
```

## Admin Users

### GET /admin/users

Daftar user aplikasi.

Query:

```text
q=raka&status=active&page=1&limit=20
```

### GET /admin/users/:id

Detail user.

### PATCH /admin/users/:id/status

Suspend atau reactivate user.

Request:

```json
{
  "status": "suspended"
}
```

## Admin Articles

### GET /admin/articles

Daftar artikel CMS.

Query:

```text
status=draft&category=makan-santai&page=1&limit=20
```

### POST /admin/articles

Buat artikel.

Request:

```json
{
  "categoryId": "uuid",
  "title": "Cara tetap makan nasi saat diet",
  "slug": "cara-tetap-makan-nasi-saat-diet",
  "summary": "Tips makan nasi dengan lebih sadar.",
  "content": "Isi artikel...",
  "thumbnailUrl": null,
  "status": "draft"
}
```

### GET /admin/articles/:id

Detail artikel.

### PUT /admin/articles/:id

Update artikel.

### PATCH /admin/articles/:id/status

Update status artikel.

Request:

```json
{
  "status": "published"
}
```

### DELETE /admin/articles/:id

Archive atau hapus artikel.

## Admin Food Database

### GET /admin/food-items

Daftar makanan.

### POST /admin/food-items

Tambah makanan.

Request:

```json
{
  "name": "Nasi ayam",
  "category": "homemade",
  "defaultPortion": "medium",
  "caloriesPerPortion": 520,
  "proteinG": 24,
  "carbsG": 62,
  "fatG": 18,
  "notes": "Estimasi porsi rumahan",
  "status": "active"
}
```

### PUT /admin/food-items/:id

Update makanan.

### PATCH /admin/food-items/:id/status

Aktif/nonaktif makanan.

## Admin Exercise Database

### GET /admin/exercise-items

Daftar olahraga.

### POST /admin/exercise-items

Tambah olahraga.

Request:

```json
{
  "name": "Jalan kaki",
  "category": "walking",
  "defaultIntensity": "medium",
  "defaultDurationMinutes": 30,
  "caloriesPer30Minutes": 110,
  "notes": "Estimasi untuk intensitas sedang",
  "status": "active"
}
```

### PUT /admin/exercise-items/:id

Update olahraga.

### PATCH /admin/exercise-items/:id/status

Aktif/nonaktif olahraga.

## Admin Notifications

### GET /admin/notifications

Daftar campaign notifikasi.

### POST /admin/notifications

Buat campaign notifikasi.

Request:

```json
{
  "title": "Jangan lupa catat makan siang",
  "message": "Catat dulu, rapinya pelan-pelan.",
  "targetSegment": "no_meal_today",
  "scheduledAt": "2026-05-18T12:00:00+07:00",
  "status": "scheduled"
}
```

### PATCH /admin/notifications/:id/status

Update status campaign.

## Admin Feedback

### GET /admin/feedback

Daftar feedback user.

Query:

```text
status=open&type=suggestion&page=1&limit=20
```

### GET /admin/feedback/:id

Detail feedback.

### PATCH /admin/feedback/:id

Update status dan catatan admin.

Request:

```json
{
  "status": "reviewed",
  "adminNote": "Masuk backlog food database."
}
```

## Admin Settings

### GET /admin/settings

Mengambil konfigurasi aplikasi.

### PUT /admin/settings

Update konfigurasi aplikasi.

## Permissions Matrix

| Endpoint Group | Super Admin | Content Admin | Support Admin |
|---|---:|---:|---:|
| Overview | Yes | Yes | Yes |
| Users | Yes | Read only | Read only |
| Articles | Yes | Yes | No |
| Food Database | Yes | Yes | No |
| Exercise Database | Yes | Yes | No |
| Notifications | Yes | No | No |
| Feedback | Yes | Read only | Yes |
| Settings | Yes | No | No |

## MVP Endpoint Priority

Urutan implementasi API:

1. Auth
2. Profile and targets
3. Mobile dashboard
4. Meal logs
5. Exercise logs
6. Weight logs
7. Water logs
8. Articles
9. Food and exercise reference data
10. Admin overview
11. Admin content management
12. Admin food and exercise database
13. Admin feedback
14. Notifications

## Tahap Berikutnya

Setelah endpoint list ini, tahap berikutnya:

1. Membuat backlog development MVP
2. Membuat struktur project
3. Menentukan tech stack final
4. Membuat prototype mobile app dan admin CMS
5. Membuat Supabase RLS policy
