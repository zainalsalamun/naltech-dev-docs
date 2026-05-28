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

