---
title: "Hawnan Mobile API Inventory"
description: "Inventaris endpoint API yang dipakai aplikasi mobile Flutter Hawnan/MSP, termasuk catatan data yang masih hardcoded, static asset, atau dummy."
category: "Hawnan"
level: "Project"
order: 101
tags: ["hawnan", "flutter", "api", "mobile", "inventory", "documentation"]
updated: "2026-05-28"
---

# Hawnan Mobile API Inventory

Dokumen ini mencatat API yang sudah dipakai oleh aplikasi mobile Flutter Hawnan/MSP berdasarkan inspeksi code pada service layer dan beberapa presentation flow.

Tanggal inspeksi: 2026-05-28.

## Ringkasan Konfigurasi API

Konfigurasi utama berada di `lib/env.dart`, `lib/service_locator_udf.dart`, dan `lib/core/network/dio_interceptor.dart`.

- Base URL aktif: `Env.baseUrl`
- Dev base URL: `https://api-dev.hawnan.id/api/v1`
- Production base URL saat ini juga mengarah ke: `https://api-dev.hawnan.id/api/v1`
- API key: `Env.apiKey`
- HTTP client: `Dio`
- Interceptor otomatis menambahkan header:
  - `Accept: application/json`
  - `Content-Type: application/json`, kecuali request multipart/form-data
  - `API-KEY`
  - `x-device-id`
  - `x-device-os`
  - `x-device-os-version`
  - `x-device-model`
  - `x-app-version`
  - `Authorization: Bearer <token>` jika user login

Catatan: beberapa service masih memakai `${Env.baseUrl}/...`, sementara service lain memakai path relatif seperti `/home`. Keduanya tetap memakai base URL yang sama melalui Dio.

## Auth, Profile, PIN, dan Akun

Source utama: `lib/service/http/auth_service.dart`.

| Method | Endpoint | Dipakai Untuk | Status Data |
| --- | --- | --- | --- |
| POST | `/auth/firebase/verify` | Verifikasi Firebase token untuk login Google/Apple/Firebase dan mendapatkan app token | API |
| GET | `/auth/profile` | Ambil profile user login | API |
| PUT | `/auth/profile` | Update profile user | API |
| POST | `/profile/photo` | Upload foto profile | API, multipart |
| POST | `/auth/refresh-token` | Refresh access token | API |
| POST | `/auth/otp/request` | Request OTP login nomor HP | API |
| POST | `/auth/otp/verify` | Verifikasi OTP nomor HP | API |
| POST | `/auth/otp/resend` | Kirim ulang OTP nomor HP | API |
| POST | `/pin/update` | Create/update PIN transaksi | API |
| POST | `/pin/verify` | Verifikasi PIN transaksi | API |
| POST | `/pin/reset/request` | Request OTP reset PIN | API |
| POST | `/pin/reset/verify-otp` | Verifikasi OTP reset PIN | API |
| POST | `/pin/reset` | Reset PIN | API |
| DELETE | `/user/event-registrations` | Debug cleanup event registration | API, debug/helper |
| DELETE | `/v2/enrollments` | Debug cleanup kajian enrollment | API, debug/helper |
| GET | `/leaderboard` | Leaderboard/activity stats | API |
| GET | `/user/my-leaderboard` | Personal leaderboard/impact summary | API |
| GET | `/settings/{key}` | Ambil setting by key | API |

Yang masih hardcoded/static di area auth:

- Login nomor HP via Firebase email fallback memakai password konstan `hawnanphoneauth`.
- Developer email list masih hardcoded di `AuthService.developerEmails`.

## Home

Source utama: `lib/service/http/home_service.dart`.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/home` | `latitude`, `longitude` | Data beranda: user, prayer overview, community, fundraising, kajian/event, coffee bar, prayer wall, news, dsb | API |

Catatan: response `/home` menjadi sumber utama banyak widget beranda.

## LMS / Al Quran Pembelajaran / Subscription

Source utama: `lib/service/http/subscription_service.dart` dan `lib/service/http/elearning_home_service.dart`.

### Subscription LMS

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/lms/packages` | `type=individual` atau `type=family` | List paket subscription Individual/Family | API |
| GET | `/lms/subscriptions` | - | Cek subscription aktif | API |
| POST | `/lms/premium/register` | `packageCode`, `paymentMethod`, `paymentGateway`, `paymentNote` | Register/beli paket premium LMS | API |

Yang masih hardcoded/static di subscription UI:

- Badge promo `Lebih Hemat 50%`.
- Info Family: `Paket family adalah paket yang bisa digunakan untuk 2 - 5 orang sekaligus`.
- List benefit Family di UI:
  - `Berbagi hingga 6 orang`
  - `Nikmati ratusan materi ngaji`
  - `Cek pelafalan dengan AI`
  - `Setor hafalanmu ke Ustandz`
  - `Tanpa Iklan`
- Fallback nama banner subscription: `Sahabat` jika data user lokal belum tersedia.

Harga, durasi, nama paket, kode paket, dan tipe paket berasal dari API `/lms/packages`.

### Pembelajaran LMS

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| POST | `/lms/partner/register` | empty body | Register akses partner SIDAQ/LMS | API |
| POST | `/lms/overview/progress` | empty body | Progress overview pembelajaran | API |
| POST | `/lms/overview/materials` | empty body | Materi overview pembelajaran | API |
| GET | `/lms/material/{materialId}` | `isVideo=false` | Detail materi | API |
| POST | `/lms/material/{materialId}/progress` | `lastPosition`, `card`, `complete` | Update progress materi | API |
| POST | `/lms/mini-quiz/submit` | jawaban quiz | Submit mini quiz | API |
| GET | `/lms/fasih/home` | - | Home Murajaah/Fasih | API |
| POST | `/lms/fasih/start/{id}` | empty body | Start/detail sesi Murajaah | API |
| POST | `/lms/fasih/check/{sessionId}/{itemId}` | `audio` multipart | Submit rekaman Murajaah untuk dicek AI/API | API |
| GET | `/lms/fasih/check-status/{jobId}` | - | Poll status pengecekan Murajaah | API |
| POST | `/lms/fasih/submit/{surahId}` | empty body | Submit completion Murajaah | API |
| POST | `/lms/overview/setor-ayat-levels` | empty body | Overview level Setor Ayat | API |
| POST | `/lms/overview/setor-ayat-surah` | `suraIndex` query | Detail surah Setor Ayat | API |
| GET | `/lms/setor-ayat/{suraIndex}/{ayaIndex}/chat` | - | Chat/detail ayat Setor Ayat | API |
| POST | `/lms/setor-ayat/{suraIndex}/{ayaIndex}/submit` | `audio` multipart | Submit rekaman Setor Ayat | API |

Catatan belum terlihat lengkap di mobile:

- Family invitation/monitoring belum terlihat sebagai endpoint mobile.
- Certificate final/end-to-end belum terlihat sebagai endpoint mobile.
- Unsubscribe/cancel LMS subscription belum terlihat sebagai endpoint mobile.
- Retry aktivasi package LMS belum terlihat sebagai endpoint mobile.

## Payment, Wallet, dan Transaction

Source utama: `lib/service/payment_service/payment_service.dart`, `lib/service/wallet_service/wallet_service.dart`, dan `lib/service/http/zakat_service.dart`.

| Method | Endpoint | Dipakai Untuk | Status Data |
| --- | --- | --- | --- |
| GET | `/payments/payment-transaction-history` | Riwayat transaksi payment gateway | API |
| GET | `/payments/direct-payment/channel-list` | List channel iPaymu/Xendit | API |
| POST | `/payments/direct-payment/charge` | Charge direct payment channel | API |
| GET | `/payments/transaction-status` | Cek status transaksi by `orderId` | API |
| POST | `/payments/charge?method=chargePayment` | General/topup charge | API |
| POST | `/payments/charge?method=chargeInfaqPayment` | Charge infaq | API |
| POST | `/payments/charge?method=chargeEventRegistration` | Charge event registration | API |
| POST | `/payments/charge?method=chargeKajianRegistration` | Charge kajian registration | API |
| POST | `/payments/charge?method=chargeDonationPayment` | Charge donasi/fundraising | API |
| POST | `/payments/charge?method=chargeZakatPayment` | Charge zakat | API |
| POST | `/payments/charge?method=chargeKajianHadiri` | Charge hadiri kajian session | API |
| POST | `/payments/charge` | Pay zakat via MSPay wallet path lama | API |
| GET | `/balance-history` | Riwayat saldo/wallet | API |

External Xendit direct usage di mobile:

| Method | Endpoint | Dipakai Untuk | Status Data |
| --- | --- | --- | --- |
| POST | `https://api.xendit.co/v2/invoices` | Create invoice/link Xendit langsung | External API |
| GET | `https://api.xendit.co/v2/invoices/{invoiceId}` | Cek status invoice Xendit langsung | External API |
| POST | `https://api.xendit.co/v3/payment_requests/{gatewayTransactionId}/simulate` | Simulasi payment Xendit sandbox | External API/dev |

Yang masih hardcoded/sensitif:

- Xendit secret key masih hardcoded di mobile pada `PaymentService`.
- Ada TODO di code untuk memindahkan konfigurasi sensitif ke secure config/environment.
- Payment method/type string seperti `DONASI`, `ZAKAT`, `KAJIAN`, `TOPUP`, `INFAQ`, `BUYER`, dan default gateway fallback tertentu masih ditentukan di mobile.
- Reward point banner di payment method masih dummy.

## Quran, Doa, Dzikir, Sholawat

Source utama: `lib/service/http/quran_service.dart`.

| Method | Endpoint / Source | Dipakai Untuk | Status Data |
| --- | --- | --- | --- |
| Local asset | `assets/json/qaraa_surahs.json` | Daftar surah | Static asset |
| Local asset | `assets/json/qaraa_surah_details.json` | Detail ayat/surah | Static asset |
| Local asset | `assets/json/qaraa_mushaf_pages.json` | Quran image/page mode | Static asset |
| Local asset | `assets/json/qaraa_mushaf_highlights.json` | Highlight mushaf/page mode | Static asset |
| POST | `/quran/user/progress` | Simpan progress baca Quran | API |
| GET | `/quran/user/stats` | Statistik user Quran | API |
| GET | `/quran/user/progress` | Ambil progress baca Quran | API |
| GET | `/quran/duas-groups` | Group/category doa | API |
| GET | `/quran/duas` | List doa atau doa by group | API |
| GET | `/quran/dzikir-types` | Tipe/category dzikir | API |
| GET | `/quran/dzikir` | List dzikir by type | API |
| GET | `/quran/sholawat` | List sholawat | API |
| GET | `/quran/user/favorites` | List favorite ayat | API |
| POST | `/quran/user/favorites` | Add favorite ayat | API |
| DELETE | `/quran/user/favorites/{favoriteId}` | Delete favorite ayat | API |
| GET | `/quran/user/bookmarks` | List bookmark ayat | API |
| POST | `/quran/user/bookmarks` | Add bookmark ayat | API |
| DELETE | `/quran/user/bookmarks/{bookmarkId}` | Delete bookmark ayat | API |

Catatan: data teks Quran/surah utama saat ini banyak berasal dari static asset Qaraa, bukan endpoint backend.

## Shalat dan Prayer Wall

Source utama: `lib/service/http/prayer_service.dart` dan `lib/service/http/prayer_time_service.dart`.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/prayer/wall/latest` | - | Doa terbaru di prayer wall | API |
| GET | `/prayer/times` | `date`, `location_id`, `latitude`, `longitude` | Jadwal shalat | API |
| POST | `/prayer/wall` | `text`, `phone`, `dedicatedTo`, `isHambaAllah` | Submit doa | API |
| POST | `/prayer/wall/{prayerId}/amin` | - | Amin doa | API |
| GET | `/prayer-times/today` | `lat`, `lon`, `method` | Jadwal shalat hari ini | API |

Yang masih static/local:

- Alarm shalat disimpan/diatur di local service.
- Nama waktu shalat dan beberapa label display ada di mobile.
- Default method jadwal shalat di `PrayerTimeService` adalah `5` (Kemenag/Indonesia).

## Event

Source utama: `lib/service/http/event_service.dart`.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/events` | `page`, `pageSize`, `categoryId` | List event | API |
| GET | `/events/{eventId}` | - | Detail event | API |
| GET | `/user/event-registrations` | `page`, `pageSize` | Riwayat/my event registration | API |
| GET | `/user/event-registrations/{registrationId}` | - | Detail registration | API |
| GET | `/user/event-registrations/event/{eventId}` | - | Detail registration by event | API |

Catatan: submit/registration event mobile saat ini terlihat lewat payment flow `chargeEventRegistration`, bukan endpoint event registration langsung di service ini.

## Kajian dan Kajian Medsos

Source utama: `lib/service/http/kajian_service.dart` dan `lib/service/kajian_medsos_service.dart`.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/kajians` | `page`, `pageSize` | List kajian | API |
| GET | `/kajians/{id}` | - | Detail kajian | API |
| GET | `/kajian-interactions/kajians/{kajianId}/summary` | - | Summary interaction kajian | API |
| GET | `/kajian-interactions/sessions/{sessionId}/summary` | - | Summary interaction session | API |
| POST | `/kajian-sessions/checkin` | `kajianSessionId` | Check-in/hadiri kajian | API |
| GET | `/v2/my-enrollments` | `page`, `pageSize` | My kajian/enrollments | API |
| GET | `/settings` | `group` | Settings, termasuk checkin settings | API |
| GET | `/kajian-interactions/improper-words` | - | Kata terlarang komentar | API |
| POST | `/kajian-interactions/sessions/{sessionId}/comments` | `content`, `imageUrl` | Create comment | API |
| GET | `/kajian-interactions/sessions/{sessionId}/comments` | `page`, `pageSize` | List comments | API |
| GET | `/kajian-interactions/comments/{commentId}/replies` | `page`, `pageSize` | List replies | API |
| POST | `/kajian-interactions/comments/{parentCommentId}/replies` | `content`, `imageUrl` | Create reply | API |
| PUT | `/kajian-interactions/kajians/{kajianId}/reaction` | `reactionType`, `sessionId` | Like/dislike session/kajian | API |

Catatan: beberapa action online link dan QR save masih tercatat TODO di codebase.

## Community

Source utama: `lib/service/http/community_service.dart`.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/communities/search` | `page`, `pageSize`, `search` | Search/list community | API |
| GET | `/communities/joined` | - | List community yang diikuti | API |
| GET | `/communities/my` | - | Community aktif/default user | API |
| POST | `/communities/{communityId}/join` | - | Join community | API |
| POST | `/communities/{communityId}/unjoin` | - | Unjoin community | API |
| PUT | `/communities/switch/{communityId}` | - | Switch active community | API |

Belum terlihat endpoint mobile untuk:

- Challenge community.
- News by community.
- Top 3 community khusus flow baru MSP.

## Fundraising, Donasi, Waqaf, Infaq

Source utama: `lib/service/http/fundraising_service.dart` dan payment service.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/fundraising/programs` | `page`, `pageSize`, `type`, `search` | List program fundraising | API |
| GET | `/fundraising/programs/{programId}` | - | Detail program fundraising | API |
| GET | `/fundraising/programs/{programId}/recent-donors` | - | Donatur terbaru | API |
| POST | `/payments/charge?method=chargeDonationPayment` | metadata donasi | Pembayaran donasi/fundraising | API |
| POST | `/donations/recurring` | `amount`, `frequency`, `executionHour`, `startDate` | Create donasi otomatis | API |
| PATCH | `/donations/recurring/{donationId}` | `amount`, `frequency`, `executionHour`, `endDate` | Update donasi otomatis | API |
| DELETE | `/donations/recurring/{donationId}` | - | Stop donasi otomatis | API |
| GET | `/donations/recurring` | `page`, `pageSize` | History/list donasi otomatis | API |

## Zakat

Source utama: `lib/service/http/zakat_service.dart` dan payment service.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/zakat/programs` | `page`, `pageSize` | List program zakat | API |
| POST | `/payments/charge` | `type=ZAKAT`, `amount`, `paymentGateway=false`, `pin`, `metadata` | Pay zakat via MSPay | API |
| POST | `/payments/charge?method=chargeZakatPayment` | metadata zakat | Pay zakat via payment service flow | API |
| GET | `/zakat/history` | `page` | Riwayat zakat | API |

Yang masih hardcoded/static:

- Kalkulator zakat ada logic/formula di mobile UI.
- Kategori string seperti `PROFESI` dan `MAAL` ditentukan di mobile.

## Coffee Bar / POS

Source utama: `lib/service/coffeebar_service/coffee_bar_service.dart`.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| GET | `/coffeebar/drinks` | `page`, `limit`, `categoryId` | List menu/minuman | API |
| GET | `/coffeebar/categories` | - | Kategori menu | API |
| POST | `/coffeebar/orders` | `tableQrCode`, `items`, `with_infaq`, `infaq_amount` | Create order coffee bar | API |
| GET | `/coffeebar/my-orders` | `page`, `status` | History order user | API |
| GET | `/coffeebar/my-orders/{orderId}` | - | Detail order | API |
| POST | `/payments/charge?method=chargeInfaqPayment` | order/infaq metadata | Pembayaran infaq/order related flow | API |

## Notification dan FCM

Source utama: `lib/service/http/notification_http_service.dart`.

| Method | Endpoint | Query/Payload Utama | Dipakai Untuk | Status Data |
| --- | --- | --- | --- | --- |
| POST | `/notifications/fcm-token` | `token`, `deviceType`, `deviceId` | Register/update FCM token | API |
| DELETE | `/notifications/fcm-token` | `fcm_token` | Remove FCM token logout | API |
| GET | `/notifications` | `page`, `pageSize`, `category` | List notification/message | API |
| GET | `/notifications/unread-count` | - | Count unread notification | API |
| GET | `/notifications/{id}` | - | Detail notification | API |
| PATCH | `/notifications/{id}/read` | - | Mark single notification read | API |
| PUT | `/notifications/read-all` | optional `category` | Mark all notifications read | API |
| DELETE | `/notifications/{id}` | - | Delete notification | API |
| DELETE | `/notifications/bulk-delete` | `ids` | Bulk delete notification | API |

Catatan: routing FCM ke beberapa detail masih ada TODO di router.

## News

Source utama: `lib/service/http/news_service.dart`.

| Method | Endpoint | Dipakai Untuk | Status Data |
| --- | --- | --- | --- |
| GET | `/news/{newsId}/with-likes` | Detail berita + likes | API |
| POST | `/news/{newsId}/likes` | Like berita | API |

Catatan: list news di home berasal dari `/home`; service khusus news saat ini hanya detail/like.

## Reward

Source utama: `lib/presentation/reward/reward_view.dart` dan `lib/presentation/reward/reward_dummy_data.dart`.

Status: masih dummy/static di mobile.

Yang masih dummy:

- Summary reward.
- Leaderboard reward.
- Voucher.
- Badge.
- History reward.
- QR voucher/redeem dummy.

Belum terlihat service/API reward khusus di mobile.

## Static Asset dan Hardcoded Data Penting

Berikut daftar area yang perlu diperhatikan saat membedakan API vs hardcode/static.

| Area | Sumber Static/Hardcoded | Catatan |
| --- | --- | --- |
| Quran core data | `assets/json/qaraa_surahs.json`, `qaraa_surah_details.json`, `qaraa_mushaf_pages.json`, `qaraa_mushaf_highlights.json` | Data Quran utama tidak semuanya dari backend |
| Reward | `RewardDummyData` | Reward belum API-driven |
| Subscription Family benefit | `_FamilyBenefits._items` di `subscription_view.dart` | Benefit belum dari package API |
| Subscription promo badge | `Lebih Hemat 50%` | Belum dari API |
| Subscription Family info | Text 2-5 orang | Belum dari API |
| Payment reward banner | `_getDummyRewardPoints()` | Masih dummy |
| Xendit secret key | `PaymentService._xenditSecretKey` | Tidak aman jika tetap di mobile |
| Phone-as-email password | `hawnanphoneauth` | Fallback Firebase phone login |
| Developer email list | `AuthService.developerEmails` | Hardcoded |
| Form dummy development | `_fillDummyData()` di beberapa form | Hanya aktif debug/developer |
| Zakat calculator | Formula di mobile UI | Bukan API |

## Catatan Implementasi LMS Phase 2 MSP

Yang sudah API-driven di mobile:

- Paket subscription Individual dan Family.
- Cek active subscription.
- Register premium package.
- Overview progress/material LMS.
- Detail/progress materi.
- Mini quiz submit.
- Murajaah/Fasih start, check audio, polling status, submit completion.
- Setor Ayat overview, detail surah, chat/detail ayat, submit audio.

Yang belum terlihat sebagai endpoint mobile:

- Family invitation link.
- Monitoring/kontrol anak oleh orang tua.
- Certificate list/detail/download.
- LMS unsubscribe/cancel subscription.
- Retry push/aktivasi subscription ke SIDAQ.
- Callback handling khusus dari SIDAQ di mobile.
- Admin reporting/package management, karena itu domain panel admin/backend.

