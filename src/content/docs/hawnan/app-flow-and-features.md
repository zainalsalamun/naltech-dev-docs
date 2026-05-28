---
title: "Hawnan App Flow dan Features"
description: "Peta awal alur aplikasi Flutter Hawnan, startup flow, root widget, bottom navigation, arsitektur, service, model, fitur, dan area yang perlu diperiksa."
category: "Hawnan"
level: "Project"
order: 100
tags: ["hawnan", "flutter", "app-flow", "features", "architecture", "documentation"]
updated: "2026-05-28"
---

# Dokumentasi Alur Aplikasi dan Fitur

Dokumen ini dibuat sebagai peta awal untuk developer baru yang melanjutkan project Flutter Hawnan. Isi dokumen berdasarkan inspeksi struktur kode, entry point, service, model, dan presentation layer.

## Ringkasan Project

Hawnan adalah aplikasi Flutter dengan domain utama ibadah, Al Quran, komunitas, kajian/event, donasi/fundraising, wallet/payment, dan POS coffee bar.

Stack utama:

- Flutter/Dart tanpa FVM.
- State management memakai Cubit/Bloc (`flutter_bloc`).
- Dependency injection memakai `get_it` melalui global service locator `sl`.
- HTTP client memakai `Dio` dengan interceptor.
- Local persistence memakai `SharedPreferences` dan ObjectBox.
- Firebase dipakai untuk Auth, Messaging/FCM, dan Crashlytics.
- Generated code memakai Freezed, JSON Serializable, Injectable, dan ObjectBox generator.

File penting:

- `lib/main.dart`: entry point aplikasi.
- `lib/core.dart`: barrel export auto-generated untuk hampir semua file utama.
- `lib/core_package.dart`: export package/dependency umum.
- `lib/service_locator.dart`: registrasi service dan cubit auto-generated.
- `lib/service_locator_udf.dart`: registrasi dependency manual/core seperti Dio, Store, AuthService, HomeService.
- `lib/provider.dart`: daftar BlocProvider global.
- `lib/presentation/main_navigation/main_navigation_view.dart`: bottom navigation dan consent flow.
- `lib/presentation/home/home_view.dart`: halaman beranda utama.

## Alur Startup Aplikasi

1. Aplikasi mulai dari `main()` di `lib/main.dart`.
2. `WidgetsFlutterBinding.ensureInitialized()` dipanggil.
3. Service alarm shalat diinisialisasi melalui `PrayerAlarmService.initialize()`.
4. Firebase diinisialisasi dengan `Firebase.initializeApp()`.
5. Dependency injection disiapkan:
   - `serviceLocatorUDF()` untuk dependency core/manual.
   - `setupServiceLocator()` untuk service dan cubit auto-generated.
6. Crashlytics diaktifkan jika service tersedia.
7. Check-in settings diambil dari API melalui `KajianService.getSettings(group: 'checkin')`, lalu disimpan ke ObjectBox jika cache belum fresh.
8. Orientasi device dikunci portrait.
9. Token auth diverifikasi melalui `AuthService.verifyFirebaseToken()`.
10. Notification service diinisialisasi dan permission diminta.
11. Callback tap FCM diarahkan ke `FcmNotificationRouter`.
12. Jika user sudah login, FCM service diinisialisasi.
13. App dirender melalui `HostAppWidget`, yang menampilkan splash/initializer sebelum masuk ke `MyApp`.

## Alur Root Widget

`MyApp` memasang beberapa provider global:

- `ThemeCubit`
- `LocaleCubit`
- `CommunitySkinCubit`
- daftar provider dari `getAllBlocProviders()`

`MaterialApp` memakai:

- `Nav.navigatorKey` untuk navigasi global.
- `Nav.routeObserver` untuk mendeteksi route lifecycle.
- Locale: `id`, `en`, `ko`.
- Theme light/dark dari `AppTheme`.
- Community skin jika user/community punya konfigurasi warna dan asset khusus.
- `home: _getInitialRoute()`.

Initial route selalu menuju `MainNavigationView`. Jika app dibuka dari notifikasi cold-start, routing notifikasi ditunda sekitar 800ms lalu diproses melalui `FcmNotificationRouter.handleNotificationTap()`.

## Alur Consent Permission

`MainNavigationView` tidak langsung menampilkan home. Ia membungkus konten dengan consent flow:

1. Cek apakah consent lokasi sudah pernah ditampilkan.
2. Jika belum, tampilkan layar izin lokasi.
3. Cek apakah consent notifikasi sudah pernah ditampilkan.
4. Jika belum, tampilkan layar izin notifikasi.
5. Setelah consent selesai, tampilkan main content dengan bottom navigation.

Permission yang relevan:

- Lokasi: dipakai untuk waktu shalat, arah kiblat, dan lokasi terkait.
- Notifikasi: dipakai untuk pengingat shalat, info event, tilawah, dan pesan/FCM.

## Bottom Navigation

Bottom navigation utama memiliki 5 tab:

| Tab | View | Fungsi |
| --- | --- | --- |
| Beranda | `HomeView` | Dashboard utama, ringkasan ibadah, event, donasi, berita, coffee bar |
| Al Quran | `QuranView` | Quran, statistik baca, bookmark, favorit, doa/dzikir/sholawat |
| Berbagi | `WaqafView` | Donasi, infaq, wakaf, zakat, payment |
| Shalat | `WaktuSalatView` | Jadwal shalat, alarm, kiblat |
| Profil | `ProfileView` | Akun, saldo, riwayat, PIN, reward, logout |

`MainNavigationNotifier.currentIndex` dipakai agar halaman seperti `ProfileView` dan `WaqafView` tahu kapan tab aktif, misalnya untuk start/stop timer refresh saldo.

## Pola Arsitektur

### Presentation Layer

Setiap module umumnya punya pola:

- `{module}_view.dart`
- `{module}_state.dart`
- `{module}_cubit.dart`

Contoh:

- `lib/presentation/login/login_view.dart`
- `lib/presentation/login/login_state.dart`
- `lib/presentation/login/login_cubit.dart`

View bertanggung jawab pada UI dan interaksi user. Cubit mengatur state dan memanggil service. State menyimpan data loading, error, form input, dan response.

### Service Layer

Service berada di `lib/service/`.

Contoh service:

- `AuthService`
- `HomeService`
- `QuranService`
- `FundraisingService`
- `PaymentService`
- `WalletService`
- `EventService`
- `KajianService`
- `PrayerTimeService`
- `FcmService`
- `AppNotificationService`

Service memakai dependency dari `sl`, misalnya:

- `sl<Dio>()`
- `sl<Store>()`
- `sl<SharedPreferences>()`

### Model Layer

Model berada di `lib/model/`, dikelompokkan per domain:

- `auth`
- `home`
- `quran`
- `fundraising`
- `zakat`
- `kajian`
- `event`
- `wallet`
- `payment`
- `prayer`
- `coffeebar`
- `objectbox`

Sebagian besar model memakai Freezed dan JSON Serializable.

## Fitur Yang Sudah Ada

### Auth dan Akun

Fitur yang terlihat sudah tersedia:

- Login email/password.
- Login nomor HP via OTP API.
- Register user.
- Register OTP.
- Forgot password.
- Forgot password OTP.
- Set password baru.
- Complete profile.
- Upload foto profil.
- Logout.
- Hapus akun.
- Create PIN.
- Enter PIN.
- Update PIN.
- Reset PIN.
- Social/Firebase auth support terlihat disiapkan.

File/module terkait:

- `lib/presentation/login/`
- `lib/presentation/register/`
- `lib/presentation/register_otp/`
- `lib/presentation/forgot_password/`
- `lib/presentation/forgot_password_otp/`
- `lib/presentation/forgot_password_new_password/`
- `lib/presentation/complete_profile/`
- `lib/presentation/create_pin/`
- `lib/presentation/enter_pin/`
- `lib/presentation/update_pin/`
- `lib/presentation/reset_pin/`
- `lib/service/http/auth_service.dart`
- `lib/service/pin_service.dart`

### Home / Beranda

Beranda mengambil data dari endpoint `/home` melalui `HomeService`.

Fitur yang terlihat:

- Header tanggal Hijriah dan Masehi.
- Lokasi user.
- Ringkasan waktu shalat.
- Notification badge.
- User info dan avatar.
- Leaderboard/impact summary.
- Komunitas Saya.
- Belajar Al Quran.
- Featured fundraising/program.
- Kajian rutin.
- Event list dengan kategori.
- Coffee & Healthy Bar menu.
- Prayer wall/doa publik.
- Amin doa.
- Create doa.
- News list dan detail.
- Pull to refresh.
- Loading shimmer.
- Timeout loading yang logout dan reset home state.

File/module terkait:

- `lib/presentation/home/home_view.dart`
- `lib/presentation/home/home_cubit.dart`
- `lib/presentation/home/home_state.dart`
- `lib/presentation/home/widget/`
- `lib/service/http/home_service.dart`
- `lib/model/home/`

### Al Quran

Fitur yang terlihat:

- Dashboard Al Quran.
- Statistik halaman dibaca.
- Terakhir dibaca.
- Favorite ayat/surah.
- Bookmark ayat.
- Quran image/page view.
- Quran surah list.
- Quran detail.
- Mode Quran dengan terjemahan/audio terlihat disiapkan.
- Doa category dan detail.
- Dzikir category dan detail.
- Sholawat category dan detail.
- Subscription banner.
- Last read service via `QuranLastReadService`.

File/module terkait:

- `lib/presentation/quran/`
- `lib/presentation/quran_image/`
- `lib/presentation/quran_detail/`
- `lib/presentation/quran_surah_list/`
- `lib/presentation/quran_favorites/`
- `lib/presentation/quran_bookmarks/`
- `lib/presentation/doa_category_list/`
- `lib/presentation/doa_detail/`
- `lib/presentation/doa_create_form/`
- `lib/presentation/dzikir_category_list/`
- `lib/presentation/dzikir_detail/`
- `lib/presentation/sholawat_category_list/`
- `lib/presentation/sholawat_detail/`
- `lib/service/http/quran_service.dart`
- `lib/service/quran_last_read_service.dart`
- `lib/model/quran/`

### Shalat dan Ibadah Harian

Fitur yang terlihat:

- Jadwal shalat.
- Navigasi tanggal jadwal shalat.
- Detail waktu shalat.
- Pengaturan alarm/pengingat shalat.
- Test adzan.
- Qiblat/kompas.
- Permission lokasi.
- Local prayer cache melalui ObjectBox.

File/module terkait:

- `lib/presentation/waktu_salat/`
- `lib/presentation/waktu_salat_detail/`
- `lib/presentation/qiblat/`
- `lib/service/http/prayer_service.dart`
- `lib/service/http/prayer_time_service.dart`
- `lib/service/prayer_alarm_service.dart`
- `lib/service/prayer_repository.dart`
- `lib/service/local/prayer_local_service.dart`
- `lib/service/compass_service/`
- `lib/model/prayer/`

### Berbagi, Donasi, Waqaf, Infaq, Zakat

Fitur yang terlihat:

- Halaman Berbagi/Waqaf sebagai tab utama.
- Carousel program fundraising.
- Search program.
- Menu Donasi Otomatis.
- Menu Infaq.
- Menu Wakaf.
- Menu Zakat.
- Menu Lainnya.
- Detail program fundraising.
- Recent donors.
- Input nominal/data donasi.
- Zakat list.
- Zakat detail.
- Zakat input.
- Zakat calculator.
- Zakat history.
- Donasi otomatis.
- History donasi otomatis.
- Success page donasi otomatis.

File/module terkait:

- `lib/presentation/waqaf/`
- `lib/presentation/waqaf_detail/`
- `lib/presentation/waqaf_input/`
- `lib/presentation/waqaf_lainnya/`
- `lib/presentation/waqaf_payment_detail/`
- `lib/presentation/zakat/`
- `lib/presentation/zakat_detail/`
- `lib/presentation/zakat_input/`
- `lib/presentation/zakat_calculator/`
- `lib/presentation/zakat_history/`
- `lib/presentation/donasi_otomatis/`
- `lib/service/http/fundraising_service.dart`
- `lib/service/http/zakat_service.dart`
- `lib/model/fundraising/`
- `lib/model/zakat/`

### Payment dan Wallet

Fitur yang terlihat:

- Pilih metode pembayaran.
- iPaymu channel selection.
- Payment waiting page.
- Riwayat transaksi payment gateway.
- Wallet balance.
- Wallet top up.
- Wallet history.
- Payment transaction history model.
- Balance refresh berkala di tab tertentu.

File/module terkait:

- `lib/presentation/payment_method_selection/`
- `lib/presentation/ipaymu_channel_selection/`
- `lib/presentation/payment_waiting/`
- `lib/presentation/riwayat_transaksi_payment_gateway/`
- `lib/presentation/wallet_topup/`
- `lib/presentation/wallet_history/`
- `lib/service/payment_service/payment_service.dart`
- `lib/service/wallet_service/wallet_service.dart`
- `lib/model/payment/`
- `lib/model/payment_method/`
- `lib/model/wallet/`
- `lib/model/ipaymu/`

### Kajian, Event, dan Komunitas

Fitur yang terlihat:

- Event list.
- Event detail.
- Event registration.
- Event registration success.
- Event history.
- My event detail.
- Kajian rutin list.
- Kajian detail.
- Kajian registration.
- My kajian detail.
- My kajian hadiri.
- Kajian medsos.
- Create comment.
- Create reply.
- Community list.
- Community detail.
- Community skin/theme.
- Check-in settings dari API dan ObjectBox.
- FCM topic sync untuk komunitas.

File/module terkait:

- `lib/presentation/event/`
- `lib/presentation/event_detail/`
- `lib/presentation/event_registration/`
- `lib/presentation/event_history/`
- `lib/presentation/my_event_detail/`
- `lib/presentation/kajian_rutin_list/`
- `lib/presentation/kajian_detail/`
- `lib/presentation/kajian_registration/`
- `lib/presentation/my_kajian_detail/`
- `lib/presentation/my_kajian_hadiri/`
- `lib/presentation/kajian_medsos/`
- `lib/presentation/kajian_medsos_create_comment/`
- `lib/presentation/kajian_medsos_create_reply/`
- `lib/presentation/community/`
- `lib/presentation/community_detail/`
- `lib/service/http/event_service.dart`
- `lib/service/http/kajian_service.dart`
- `lib/service/kajian_medsos_service.dart`
- `lib/service/http/community_service.dart`
- `lib/service/checkin_settings_service.dart`
- `lib/model/event/`
- `lib/model/kajian/`
- `lib/model/community/`

### E-Learning / Pembelajaran Quran

Fitur yang terlihat:

- Home pembelajaran.
- E-learning home.
- Detail pembelajaran.
- Detail materi.
- Dashboard setor ayat.
- Setor ayat detail.
- Setor ayat record.
- Dashboard murajaah.
- Murajaah detail.
- My package.

File/module terkait:

- `lib/presentation/elearning_home/`
- `lib/presentation/home_pembelajaran/`
- `lib/presentation/detail_pembelajaran/`
- `lib/presentation/detail_materi/`
- `lib/presentation/dashboard_setor_ayat/`
- `lib/presentation/setor_ayat_detail/`
- `lib/presentation/setor_ayat_record/`
- `lib/presentation/dashboard_murajaah/`
- `lib/presentation/murajaah_detail/`
- `lib/presentation/my_package/`
- `lib/service/http/elearning_home_service.dart`
- `lib/model/learning/`

### POS / Coffee Bar

Fitur yang terlihat:

- POS dashboard.
- POS scan QR.
- POS view.
- POS checkout.
- Coffee bar menu di home.
- Order history.
- Order detail.
- Coffee bar categories/drinks/orders model.

File/module terkait:

- `lib/presentation/pos_dashboard/`
- `lib/presentation/pos_scan/`
- `lib/presentation/pos/`
- `lib/presentation/pos_checkout/`
- `lib/presentation/order_history/`
- `lib/presentation/order_detail/`
- `lib/service/coffeebar_service/coffee_bar_service.dart`
- `lib/model/coffeebar/`
- `lib/model/coffee_bar/`

### Notification dan Message

Fitur yang terlihat:

- FCM initialization.
- FCM topic sync.
- Local notification.
- Notification tap routing.
- Message list.
- Message detail.
- Mark notification as read.
- Notification count refresh di home.

File/module terkait:

- `lib/service/fcm_service/`
- `lib/service/app_notification_service/`
- `lib/service/http/notification_http_service.dart`
- `lib/presentation/message/`
- `lib/model/notification/`

### News

Fitur yang terlihat:

- News list di home.
- News category filter.
- News detail.

File/module terkait:

- `lib/presentation/news_detail/`
- `lib/service/http/news_service.dart`
- `lib/model/news/`

### Reward

Fitur yang terlihat:

- Reward page.
- Summary reward.
- Leaderboard reward.
- Voucher.
- Badge.
- History reward.

Catatan: module reward masih terlihat memakai dummy data dari `RewardDummyData`.

File/module terkait:

- `lib/presentation/reward/reward_view.dart`
- `lib/presentation/reward/reward_dummy_data.dart`

## Area Yang Perlu Diperiksa / Belum Sepenuhnya Selesai

Beberapa bagian masih terlihat punya TODO, dummy, atau placeholder:

- `RewardView` masih memakai `RewardDummyData`.
- `MainNavigationCubit` masih punya TODO load data.
- `CommunityDetailCubit` masih punya TODO load data.
- `WaqafPaymentDetailCubit` masih punya TODO load data.
- `PosScanCubit` masih punya TODO load data.
- `HomeSearchCubit` masih punya TODO load data.
- `TilawahkuCubit` masih punya TODO load data.
- Beberapa route FCM detail masih TODO, misalnya payment detail, fundraising detail, community detail, doa detail.
- Beberapa form punya `_fillDummyData()` untuk kebutuhan development/debug.
- `PaymentService` punya TODO untuk memindahkan konfigurasi sensitif ke secure config/environment.
- `MyEventDetailCubit` punya TODO save QR code to gallery.
- `MyKajianDetailCubit` punya TODO untuk join/open online link.
- `QuranDetailView` punya TODO scroll ke ayat tertentu setelah surah load.

## Cara Membaca Codebase Untuk Developer Baru

Urutan yang disarankan:

1. Mulai dari `lib/main.dart`.
2. Baca `lib/service_locator_udf.dart` untuk dependency manual/core.
3. Baca `lib/service_locator.dart` untuk daftar service dan cubit yang diregistrasikan.
4. Baca `lib/provider.dart` untuk provider global.
5. Baca `lib/presentation/main_navigation/main_navigation_view.dart` untuk alur consent dan tab utama.
6. Baca `lib/presentation/home/home_view.dart` dan `lib/presentation/home/home_cubit.dart` untuk memahami dashboard utama.
7. Pilih domain fitur yang sedang dikerjakan, lalu ikuti pola:
   - `presentation/{module}/{module}_view.dart`
   - `presentation/{module}/{module}_cubit.dart`
   - `presentation/{module}/{module}_state.dart`
   - `service/...`
   - `model/...`

## Command Penting

Install dependency:

```bash
flutter pub get
```

Analyze:

```bash
flutter analyze
```

Test:

```bash
flutter test
```

Generate code:

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

Generate module presentation baru:

```bash
dart lib/core/dev/generator/generator.dart nama-module
```

atau:

```bash
sh create.sh nama-module
```

## Catatan Style dan Arsitektur Project

- Jangan akses `Dio`, `LocalStorage`, `Permission`, atau ObjectBox langsung dari presentation jika bisa lewat service.
- Gunakan `Nav.to`, `Nav.back`, dan `Nav.offAll` untuk navigasi.
- Gunakan theme token, jangan hardcode warna shell/background.
- Background halaman harus mengikuti community skin melalui `Theme.of(context).scaffoldBackgroundColor` atau helper `AppTheme`.
- Jika menambah Freezed/ObjectBox/injectable model/service, jalankan build runner.
- Untuk flow submit penting seperti pendaftaran, pembayaran, atau pesanan, tampilkan dialog konfirmasi sebelum submit.
- Untuk bottom sheet, hindari fixed height; gunakan constraints dan aksi utama fixed di bawah.



---

## Rencana Fitur Berikutnya

Bagian ini adalah catatan backlog agar requirement fitur berikutnya tidak tercecer. Status: rencana/PRD awal, belum menjadi konfirmasi implementasi final.

### Jemaah Premium Subscription - MSP

Referensi internal:

- Module: MSP.
- Item List No. 18.
- Overview MSP Summary Google Sheet.

Overview fitur:

- Tambahkan row menu baru di `ProfileView`: **Jemaah Premium**.
- Jemaah Premium akan menjadi dasar formulasi scoring leaderboard berbasis komunitas, contoh tambahan poin `+5`.
- Halaman Jemaah Premium menampilkan pilihan kategori Digital Card: Silver, Gold/Bold, dan Platinum.
- Setiap card memiliki harga, deskripsi, gambar, benefit, total user subscribe, dan total amount terkumpul.
- Contoh pricing awal:
  - Silver: Rp99.000 per bulan.
  - Gold/Bold: Rp199.000 per bulan.
  - Platinum/Premium: Rp399.000 per bulan.
- Pricing harus dinamis dan bisa diatur dari Panel Admin melalui mastering data Digital Card / Jemaah Premium Package.
- Model pembayaran mirip Donasi Otomatis: recurring debit dari saldo MSPay Wallet.
- Jika user unsubscribe, saldo MSPay Wallet tidak terpotong pada periode berikutnya.
- Jika saldo kurang, kirim notifikasi email, mirip logic Donasi Otomatis.
- Setelah subscribe, user mendapatkan kartu e-money fisik yang sudah include saldo dan dikirim via ekspedisi.
- Desain kartu fisik/e-money disiapkan oleh Hawnan Team.
- Benefit per card hanya berupa informasi di aplikasi. Action fulfillment benefit dilakukan offline oleh Hawnan Team dan tidak termasuk sistem aplikasi.
- User bisa upgrade atau downgrade berdasarkan level digital card, contoh Silver100, Gold200, Premium300.

Contoh benefit Silver Digital Card:

- Akses live streaming.
- Akses kajian apps.
- Akses eksklusif webinar.
- Event tahunan offline.
- Terdaftar sebagai orang tua asuh.
- Terdaftar sebagai pendukung penghafal Al Quran.

Kebutuhan Panel Admin:

- Mastering package/card Jemaah Premium.
- Field card: title, description, image, list of benefit, price, counter total subscriber, total amount collected.
- Riwayat subscription.
- Reporting subscription dan amount.
- Menu Pengiriman Kartu untuk pencatatan pengiriman kartu fisik/e-money.

Catatan implementasi mobile:

- Tambahkan menu di Profile.
- Tambahkan halaman list package/card.
- Tambahkan flow subscribe, unsubscribe, upgrade, dan downgrade.
- Integrasi dengan wallet/MSPay dan scheduler recurring billing.
- Tambahkan history subscription.
- Pastikan flow submit subscription menampilkan dialog konfirmasi sebelum proses pembayaran.

### Jemaah Check-in On Site

Overview fitur:

- User melakukan check-in on site dengan scan QR Code dinamis.
- Saat scan, tampilkan 2 checkbox:
  - Sholat.
  - Visit.
- User boleh memilih salah satu atau keduanya.
- Check-in dapat menjadi bagian dari scoring komunitas/BIPX pada fase berikutnya.

Kebutuhan awal:

- Dynamic QR source dari backend/panel.
- Endpoint submit check-in dengan pilihan aktivitas.
- Riwayat check-in user dan komunitas jika diperlukan.
- Validasi anti duplikasi berdasarkan event/lokasi/waktu sesuai aturan backend.

### Community Screen Enhancement

Tambahan flow di screen komunitas:

- Tampilkan list top 3 komunitas saya.
- Di kanan atas section komunitas saya, tambahkan tombol **Lihat Semua**.
- Tambahkan widget **Challenge Komunitas**:
  - Slider horizontal.
  - Menampilkan image, title, dan date creation.
  - Ambil top 10 challenge.
  - Tambahkan tombol **Lihat Semua** untuk seluruh challenge komunitas yang user ikuti atau tergabung di aplikasi.
- Tambahkan **News Community** di bawah widget Challenge:
  - Bisa circle item atau square item.
  - Slider horizontal.
  - Item bisa diklik masuk ke halaman detail news by community.

Logic Challenge Komunitas:

- Challenge dibuat dari Panel Admin atau Panel Komunitas.
- Contoh challenge: Puasa Senin-Kamis selama 90 hari dengan reward 500 poin.
- Challenge punya durasi, poin, detail item, dan status publish.
- Satu user hanya boleh mengikuti 1 challenge aktif dalam satu waktu.
- Jika user ingin join challenge lain, current challenge harus dicancel dulu atau diselesaikan sesuai durasi.
- Poin challenge diberikan harian berdasarkan cut-off UTC 23:59 selama challenge tidak dicancel.
- Poin masuk ke formulasi BIPX/community scoring.
- User hanya mendapatkan poin jika sudah join challenge dan tergabung dengan komunitas terkait.

Kebutuhan backend/panel:

- CRUD Challenge.
- Publish challenge ke community page.
- Join/cancel challenge.
- Daily point calculation dengan cut-off UTC 23:59.
- Reporting participant, progress, point, dan status.
- CRUD News Community dan detail news.

### Al Quran - Pembelajaran LMS Phase 2 MSP

Referensi internal:

- Item List No. 10.
- Overview Phase 2 MSP Summary Google Sheet.
- Integrasi Third Party SIDAQ/Qaraa.

Overview:

- Pembelajaran Al Quran online terintegrasi dengan API Third Party SIDAQ.
- Flow UI dan logic mengikuti aplikasi SIDAQ mobile dan desain Figma yang akan disiapkan.
- Ada 2 kategori utama:
  - Murajaah.
  - Setor Ayat.
- Ada module class:
  - Hijaiyah.
  - Tahsin.
  - Tajwid.
  - Ujian Kelulusan Akhir.
- Setiap module class memiliki submodule/Bab/Materi.
- Setiap Bab memiliki submateri.
- Module, Bab, dan materi harus dikerjakan berurutan. User tidak boleh lompat materi.
- Sertifikat diterbitkan per module class berdasarkan Uji Pemahaman/Evaluasi.
- Setelah semua module class selesai dan sertifikat per module terbit, user dinyatakan lulus keseluruhan dan mendapatkan sertifikat akhir online.

Verifikasi pembelajaran:

- Murajaah: check/verifikasi setor ayat dan penilaian kelulusan audio diperiksa oleh AI melalui API integrasi.
- Setor Ayat: check/verifikasi setor ayat dan penilaian kelulusan audio diperiksa oleh Ustad/Ustadzah melalui API integrasi.
- Ada ujian drawing, audio/voice, dan multiple choice sesuai API SIDAQ.
- Hasil koreksi Ustad/Ustadzah dapat diterima via callback dari SIDAQ.
- Notifikasi hasil koreksi masuk ke notification list aplikasi MSP.

Membership dan package:

- Registrasi module Pembelajaran bisa berbayar, free, atau free plus donasi.
- Membership eksklusif untuk aplikasi MSP dan terpisah dari database API SIDAQ.
- Data user yang dikirim ke SIDAQ: email, nama, phone number, dan payload lain sesuai API.
- Sync user MSP ke SIDAQ Core: signup/signin ke SIDAQ Core dari aplikasi MSP.
- Jika aplikasi MSP logout, user juga logout dari SIDAQ Core.
- Ada flag di MSP untuk menandai user sudah signup/signin ke SIDAQ Core.
- Package disediakan oleh SIDAQ, pricing dapat disesuaikan dari Panel Admin MSP.
- Tipe membership:
  - Individu / Pro.
  - Family.
- Durasi subscription awal:
  - 1 bulan / 30 hari.
  - 6 bulan / 180 hari.
  - 12 bulan / 365 hari.
- Pricing awal family dapat disamakan dengan harga SIDAQ app ditambah 5%, lalu bisa diupdate dari Panel Admin.
- Ada Harga Pokok dari SIDAQ dan komisi/fee MSP yang perlu dibahas lanjutan.

Payment dan subscription:

- Payment menggunakan channel core system Hawnan/MSP:
  - MSPay Wallet.
  - Online Payment.
  - VA.
  - QRIS.
  - Channel tersedia lain seperti iPayMu/Xendit.
- SIDAQ menyiapkan API topup balance MSP.
- Saldo balance MSP di SIDAQ memiliki threshold minimum Rp1.000.000.
- Jika saldo MSP kurang dari threshold, kirim notifikasi email.
- User bayar di PG/MSPay MSP, lalu MSP push purchase ke API SIDAQ untuk memotong balance MSP di SIDAQ.
- Data purchase ke SIDAQ membawa id paket, tipe, noreff, iduser, username, dan payload lain sesuai API.
- Jika pembayaran user berhasil tetapi push API SIDAQ gagal:
  - Retry maksimal 2 kali.
  - Interval retry 1 menit.
  - Status paket user di aplikasi: sedang diproses / menunggu aktivasi.
  - Jika tetap gagal, perlu retry manual dari Panel Admin.
  - Selama belum berhasil, paket belum aktif.
- Jika payment gagal:
  - User mendapat feedback pembayaran gagal.
  - Paket tidak aktif dan tidak muncul sebagai paket berhasil dibeli.
- Jika payment gateway pending:
  - Paket belum aktif.
  - User mendapat feedback proses pembayaran sedang berjalan.
  - Setelah callback PG sukses, MSP push API SIDAQ, lalu paket aktif jika push berhasil.
- Notifikasi ke user terkait potongan saldo langganan di-handle oleh MSP.
- Jika user unsubscribe:
  - Cancel subscription di MSP.
  - Push cancel subscription ke API SIDAQ dengan noreff, iduser, username.
  - Due date mengikuti tanggal pembelian dan durasi harian H-1 di sisi MSP.
- Upgrade paket:
  - User bisa upgrade durasi, contoh dari 1 bulan ke 6 bulan.
  - Durasi baru ditambahkan ke sisa periode, contoh total menjadi 7 bulan.
  - Opsi downgrade tidak ada selama paket aktif.
  - Setelah periode selesai, user dapat beli paket durasi lebih rendah.

Cut-off subscription:

- MSP melakukan recurring billing berdasarkan tanggal beli.
- Durasi dihitung harian: 30, 180, atau 365 hari.
- Cut-off MSP di hari H pukul 00:00 atau waktu lain yang ditentukan MSP.
- SIDAQ melakukan cut-off H+1, waktu disesuaikan oleh MSP/SIDAQ.

Family Package Subscription:

- User dapat membeli paket Family dengan pricing berbeda dari Individu/Pro.
- Family memiliki maksimal 5 seat anak + 1 orang tua.
- Orang tua dapat add/remove anak selama seat tersedia.
- Orang tua dapat menunjuk 1 atau 2 anak sebagai admin jika API mendukung.
- Admin family punya privilege menambahkan dan menghapus user biasa sesuai seat tersedia.
- Aplikasi generate invitation link untuk anak.
- Link dapat dishare via WhatsApp, email, dan platform lain.
- Saat link diklik, deep link membuka aplikasi MSP dan menampilkan confirmation layout seperti SIDAQ app.
- Setelah invitation dikonfirmasi, anak mendapat paket Family.
- Jika anak sudah punya paket Pro, aplikasi akan switch/ganti akses ke paket Family atau menampilkan Pro + Family sesuai aturan final API.
- Orang tua mendapat fitur monitoring dan kontrol anak sesuai API SIDAQ:
  - Progress materi.
  - Status kelulusan.
  - Sertifikat.
  - Aktivitas pembelajaran.
- Jika orang tua cancel subscription atau subscription selesai:
  - Seluruh circle/family nonaktif.
  - Akses module anak terkunci.
  - Semua anak/circle otomatis diremove sesuai aturan API.

Sertifikat:

- Sertifikat didapatkan setelah lulus seluruh materi per Bab dan kategori, atau setelah lulus Sertifikat Akhir.
- Sertifikat berupa PDF.
- User dapat view di aplikasi, share, atau print sendiri.
- Sertifikat resmi dari lembaga pendidikan SIDAQ, powered by SIDAQ.
- Template sertifikat menyesuaikan template MSP.

Goal:

- User MSP mendapatkan pembelajaran Al Quran online.
- Ada 2 metode pembelajaran: Murajaah by AI dan Setor Ayat by Ustad/Ustadzah.
- Pembelajaran Bab harus sequential dari awal sampai akhir dan harus lulus sebelum lanjut.
- User mendapatkan sertifikat online resmi yang bisa dicetak.
- Membership memiliki tipe Individu dan Family.
- Family memiliki maksimal 5 seat anak dan fitur monitoring/kontrol anak.
- Panel Admin memiliki menu Pembelajaran untuk package/pricing, membership, transaksi, ujian, sertifikat, reporting, dan user activation.
- SuperAdmin dapat mengaktifkan atau menonaktifkan user tertentu.

Success metric:

- User MSP dapat menggunakan Module Pembelajaran yang flow-nya sama dengan aplikasi SIDAQ.
- Kategori Murajaah dan Setor Ayat berjalan dengan verifikasi sesuai role: AI dan Ustad/Ustadzah.
- Tersedia minimal 3 Bab plus Sertifikat untuk Murajaah dan Setor Ayat.
- Membership terbagi Individu/Pro dan Family.
- Pricing package dapat diupdate via Panel Admin.
- User hanya dapat mengakses module jika subscription aktif.
- Jika subscription tidak aktif, seluruh akses module terkunci.
- Panel Admin memiliki submenu Package/Pricing, Membership, Transaction/Payment, Ujian & Sertifikat, dan Reporting.

Requirement awal:

| Area | User Story / Requirement | Acceptance Criteria | Priority | Note |
| --- | --- | --- | --- | --- |
| UI/UX Figma | Implementasi UI Pembelajaran mengikuti flow aplikasi SIDAQ. | Flow mobile sesuai Figma dan logic SIDAQ. | 1 | Sesuaikan dengan aplikasi SIDAQ. |
| Backend Integrasi SIDAQ | MSP integrasi dengan API SIDAQ untuk membership, payment, module, progress, monitoring, dan certificate. | User MSP bisa signup/signin SIDAQ, beli package, akses module, submit audio, dan menerima status dari callback. | 2 | API collection dari SIDAQ/Qaraa. |
| Membership & Package | Tersedia package Individu/Pro dan Family dengan durasi 30/180/365 hari. | Pricing bisa dikonfigurasi, callback package tersedia, subscription aktif sesuai periode. | 2 | Perlu mapping payload SIDAQ. |
| Payment | Payment MSP berhasil lalu push purchase ke API SIDAQ. | Success, pending, failed, retry, dan manual retry tertangani. | 2 | Perlu idempotency dan noreff yang aman. |
| Learning | Module Murajaah dan Setor Ayat berjalan sequential. | Materi berikutnya terkunci sampai materi sebelumnya lulus. | 3 | Murajaah by AI, Setor Ayat by Ustad/Ustadzah. |
| Family | Orang tua bisa mengelola anak dan monitoring progress. | Invitation link, add/remove, seat limit, dan lock access berjalan. | 3 | Butuh deep linking. |
| Mobile App | Mobile MSP menyesuaikan flow aplikasi SIDAQ. | UI dan navigasi sesuai Figma/SIDAQ. | 3 | Integrasi penuh API SIDAQ. |
| Panel Admin | Tambahkan menu Pembelajaran. | Ada Package/Pricing, Membership, Transaction/Payment, Ujian & Sertifikat, Reporting, retry action, active/inactive user. | 4 | Menyesuaikan kebutuhan backend dan mobile. |

Open questions / perlu dipastikan:

- Nama final tier Jemaah Premium: Bold atau Gold.
- Apakah upgrade/downgrade Jemaah Premium berlaku prorate atau mulai periode berikutnya.
- Detail payload API SIDAQ untuk signup/signin, purchase package, cancel subscription, callback correction, certificate, dan family invitation.
- Skema idempotency untuk retry push purchase ke SIDAQ.
- Waktu final cut-off subscription MSP dan SIDAQ.
- Bentuk final scoring BIPX/community leaderboard.
- Flow admin pengiriman kartu e-money: status, ekspedisi, resi, dan notifikasi user.
