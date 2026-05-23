---
title: "Firebase Authentication untuk Pemula"
description: "Tutorial Firebase Authentication di Flutter: setup firebase_auth, register, login, logout, current user, authStateChanges, AuthService, AuthRepository, dan redirect login/home."
category: "Flutter"
level: "Firebase"
order: 70
tags: ["flutter", "firebase", "authentication", "login", "register"]
updated: "2026-05-23"
---

# Firebase Authentication untuk Pemula

Firebase Authentication adalah layanan Firebase untuk mengelola login user. Dengan Firebase Auth, aplikasi bisa memiliki fitur register, login, logout, current user, dan mendeteksi apakah user sedang login atau belum.

Materi ini fokus pada email/password authentication.

Yang akan dipelajari:

- konsep Firebase Auth
- enable Email/Password di Firebase Console
- install package `firebase_auth`
- register user
- login user
- logout
- membaca current user
- mendengarkan auth state
- membuat `AuthService`
- membuat `AuthRepository`
- membuat halaman login dan register sederhana
- redirect login/home
- error umum

---

## 1. Apa Itu Authentication

Authentication adalah proses memastikan siapa user yang sedang memakai aplikasi.

Contoh:

```text
User membuka aplikasi
-> user login dengan email/password
-> Firebase memverifikasi akun
-> aplikasi mendapatkan user
-> aplikasi menampilkan halaman home
```

Jika user belum login:

```text
currentUser == null
```

Jika user sudah login:

```text
currentUser != null
```

Authentication penting sebelum aplikasi punya data per user. Misalnya Task Manager online:

```text
User A hanya melihat task milik User A
User B hanya melihat task milik User B
```

---

## 2. Alur Firebase Auth

Alur register:

```text
User isi email dan password
-> aplikasi memanggil createUserWithEmailAndPassword
-> Firebase membuat akun
-> user otomatis login
-> aplikasi masuk ke Home
```

Alur login:

```text
User isi email dan password
-> aplikasi memanggil signInWithEmailAndPassword
-> Firebase memverifikasi akun
-> jika berhasil, user login
-> aplikasi masuk ke Home
```

Alur logout:

```text
User tekan logout
-> aplikasi memanggil signOut
-> user keluar
-> aplikasi kembali ke Login
```

Alur auth state:

```text
authStateChanges
-> null berarti belum login
-> User berarti sudah login
```

---

## 3. Persiapan Firebase Project

Sebelum kode Flutter, pastikan:

1. Project Flutter sudah terhubung ke Firebase.
2. File `firebase_options.dart` sudah ada.
3. Firebase sudah diinisialisasi di `main.dart`.
4. Email/Password provider sudah diaktifkan di Firebase Console.

Jika belum, ikuti materi:

- [Setup Project Flutter di Firebase Studio](/docs/flutter/setup-flutter-firebase-studio/)

Di Firebase Console:

```text
Authentication
-> Sign-in method
-> Email/Password
-> Enable
-> Save
```

Jika Email/Password belum diaktifkan, register/login akan gagal.

---

## 4. Install Package

Tambahkan package:

```bash
flutter pub add firebase_core
flutter pub add firebase_auth
```

Lalu:

```bash
flutter pub get
```

Import:

```dart
import 'package:firebase_auth/firebase_auth.dart';
```

---

## 5. Inisialisasi Firebase

Contoh `main.dart`:

```dart
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';
import 'app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const MyApp());
}
```

Penjelasan:

- `WidgetsFlutterBinding.ensureInitialized()` wajib sebelum kode async Firebase.
- `Firebase.initializeApp()` menghubungkan app ke Firebase.
- `DefaultFirebaseOptions.currentPlatform` berasal dari `firebase_options.dart`.

---

## 6. Register User

Firebase Auth menyediakan:

```dart
createUserWithEmailAndPassword
```

Contoh:

```dart
Future<UserCredential> register({
  required String email,
  required String password,
}) async {
  return FirebaseAuth.instance.createUserWithEmailAndPassword(
    email: email,
    password: password,
  );
}
```

Dengan error handling:

```dart
Future<UserCredential> register({
  required String email,
  required String password,
}) async {
  try {
    return await FirebaseAuth.instance.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
  } on FirebaseAuthException catch (error) {
    if (error.code == 'weak-password') {
      throw Exception('Password terlalu lemah');
    }

    if (error.code == 'email-already-in-use') {
      throw Exception('Email sudah terdaftar');
    }

    throw Exception(error.message ?? 'Gagal register');
  }
}
```

Error umum saat register:

- `weak-password`: password terlalu lemah
- `email-already-in-use`: email sudah dipakai
- `invalid-email`: format email tidak valid

---

## 7. Login User

Firebase Auth menyediakan:

```dart
signInWithEmailAndPassword
```

Contoh:

```dart
Future<UserCredential> login({
  required String email,
  required String password,
}) async {
  return FirebaseAuth.instance.signInWithEmailAndPassword(
    email: email,
    password: password,
  );
}
```

Dengan error handling:

```dart
Future<UserCredential> login({
  required String email,
  required String password,
}) async {
  try {
    return await FirebaseAuth.instance.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
  } on FirebaseAuthException catch (error) {
    if (error.code == 'user-not-found') {
      throw Exception('User tidak ditemukan');
    }

    if (error.code == 'wrong-password') {
      throw Exception('Password salah');
    }

    if (error.code == 'invalid-email') {
      throw Exception('Format email tidak valid');
    }

    throw Exception(error.message ?? 'Gagal login');
  }
}
```

Catatan:

Beberapa kode error bisa berubah tergantung konfigurasi Firebase, versi package, dan proteksi keamanan. Selalu tampilkan pesan yang aman dan mudah dipahami user.

---

## 8. Logout

Logout:

```dart
Future<void> logout() async {
  await FirebaseAuth.instance.signOut();
}
```

Setelah logout, `authStateChanges()` akan mengirim `null`.

---

## 9. Current User

Membaca user saat ini:

```dart
final user = FirebaseAuth.instance.currentUser;
```

Contoh:

```dart
if (user == null) {
  print('Belum login');
} else {
  print('Sudah login: ${user.email}');
}
```

Data yang sering dipakai:

```dart
user.uid
user.email
user.displayName
user.photoURL
```

Paling penting:

```dart
user.uid
```

`uid` dipakai sebagai identitas unik user. Nanti saat memakai Firestore, `uid` bisa dipakai untuk menyimpan task per user.

---

## 10. Auth State Changes

Untuk mendeteksi user login/logout, gunakan:

```dart
FirebaseAuth.instance.authStateChanges()
```

Contoh:

```dart
Stream<User?> authStateChanges() {
  return FirebaseAuth.instance.authStateChanges();
}
```

Di UI:

```dart
StreamBuilder<User?>(
  stream: FirebaseAuth.instance.authStateChanges(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const CircularProgressIndicator();
    }

    final user = snapshot.data;

    if (user == null) {
      return const LoginPage();
    }

    return const HomePage();
  },
)
```

Penjelasan:

- Jika `user == null`, tampilkan Login.
- Jika `user != null`, tampilkan Home.
- Saat login/logout, UI otomatis berubah.

---

## 11. Membuat AuthService

Buat file:

```text
lib/services/auth_service.dart
```

Isi:

```dart
import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  final FirebaseAuth _auth;

  AuthService({
    FirebaseAuth? auth,
  }) : _auth = auth ?? FirebaseAuth.instance;

  User? get currentUser => _auth.currentUser;

  Stream<User?> authStateChanges() {
    return _auth.authStateChanges();
  }

  Future<UserCredential> register({
    required String email,
    required String password,
  }) async {
    return _auth.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
  }

  Future<UserCredential> login({
    required String email,
    required String password,
  }) async {
    return _auth.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
  }

  Future<void> logout() async {
    await _auth.signOut();
  }

  Future<void> sendPasswordResetEmail(String email) async {
    await _auth.sendPasswordResetEmail(email: email);
  }
}
```

Kenapa dibuat service?

Supaya detail Firebase Auth tidak ditulis langsung di UI.

---

## 12. Membuat AuthRepository

Buat file:

```text
lib/repositories/auth_repository.dart
```

Isi:

```dart
import 'package:firebase_auth/firebase_auth.dart';

import '../services/auth_service.dart';

class AuthRepository {
  final AuthService _authService;

  AuthRepository({
    AuthService? authService,
  }) : _authService = authService ?? AuthService();

  User? get currentUser => _authService.currentUser;

  Stream<User?> authStateChanges() {
    return _authService.authStateChanges();
  }

  Future<void> register({
    required String email,
    required String password,
  }) async {
    try {
      await _authService.register(
        email: email,
        password: password,
      );
    } on FirebaseAuthException catch (error) {
      throw Exception(_mapAuthError(error));
    }
  }

  Future<void> login({
    required String email,
    required String password,
  }) async {
    try {
      await _authService.login(
        email: email,
        password: password,
      );
    } on FirebaseAuthException catch (error) {
      throw Exception(_mapAuthError(error));
    }
  }

  Future<void> logout() async {
    await _authService.logout();
  }

  Future<void> sendPasswordResetEmail(String email) async {
    await _authService.sendPasswordResetEmail(email);
  }

  String _mapAuthError(FirebaseAuthException error) {
    switch (error.code) {
      case 'invalid-email':
        return 'Format email tidak valid';
      case 'weak-password':
        return 'Password terlalu lemah';
      case 'email-already-in-use':
        return 'Email sudah terdaftar';
      case 'user-not-found':
        return 'User tidak ditemukan';
      case 'wrong-password':
        return 'Password salah';
      case 'network-request-failed':
        return 'Koneksi internet bermasalah';
      default:
        return error.message ?? 'Terjadi kesalahan authentication';
    }
  }
}
```

Kenapa perlu repository?

Karena repository menjadi API yang dipakai aplikasi. Jika nanti login pindah ke backend custom, UI/state tidak harus tahu detailnya.

---

## 13. Struktur Folder

Struktur sederhana:

```text
lib/
  main.dart
  app.dart
  services/
    auth_service.dart
  repositories/
    auth_repository.dart
  pages/
    auth_gate.dart
    login_page.dart
    register_page.dart
    home_page.dart
```

Jika memakai state management:

```text
lib/
  providers/
    auth_provider.dart
```

atau:

```text
lib/
  cubits/
    auth_cubit.dart
    auth_state.dart
```

Untuk materi ini, kita mulai dengan `StreamBuilder` agar lebih mudah dipahami.

---

## 14. Membuat AuthGate

`AuthGate` menentukan halaman awal berdasarkan status login.

Buat file:

```text
lib/pages/auth_gate.dart
```

Isi:

```dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../repositories/auth_repository.dart';
import 'home_page.dart';
import 'login_page.dart';

class AuthGate extends StatelessWidget {
  AuthGate({super.key});

  final authRepository = AuthRepository();

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: authRepository.authStateChanges(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        final user = snapshot.data;

        if (user == null) {
          return const LoginPage();
        }

        return const HomePage();
      },
    );
  }
}
```

Penjelasan:

- `authStateChanges()` mendeteksi login/logout.
- Jika user null, tampilkan `LoginPage`.
- Jika user ada, tampilkan `HomePage`.

---

## 15. Pasang AuthGate di main.dart

```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Firebase Auth App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: AuthGate(),
    );
  }
}
```

Sekarang aplikasi akan otomatis memilih Login atau Home.

---

## 16. Membuat LoginPage

Buat file:

```text
lib/pages/login_page.dart
```

Isi:

```dart
import 'package:flutter/material.dart';

import '../repositories/auth_repository.dart';
import 'register_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final authRepository = AuthRepository();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  bool isLoading = false;

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  Future<void> login() async {
    final email = emailController.text.trim();
    final password = passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      showMessage('Email dan password wajib diisi');
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      await authRepository.login(
        email: email,
        password: password,
      );
    } catch (error) {
      showMessage(error.toString());
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  void showMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            controller: emailController,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: passwordController,
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Password',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: isLoading ? null : login,
            child: Text(isLoading ? 'Loading...' : 'Login'),
          ),
          const SizedBox(height: 8),
          TextButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const RegisterPage(),
                ),
              );
            },
            child: const Text('Belum punya akun? Register'),
          ),
        ],
      ),
    );
  }
}
```

Setelah login berhasil, tidak perlu manual navigate ke Home karena `AuthGate` akan menerima auth state baru dan otomatis menampilkan `HomePage`.

---

## 17. Membuat RegisterPage

Buat file:

```text
lib/pages/register_page.dart
```

Isi:

```dart
import 'package:flutter/material.dart';

import '../repositories/auth_repository.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final authRepository = AuthRepository();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final confirmPasswordController = TextEditingController();
  bool isLoading = false;

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> register() async {
    final email = emailController.text.trim();
    final password = passwordController.text.trim();
    final confirmPassword = confirmPasswordController.text.trim();

    if (email.isEmpty || password.isEmpty || confirmPassword.isEmpty) {
      showMessage('Semua field wajib diisi');
      return;
    }

    if (password != confirmPassword) {
      showMessage('Konfirmasi password tidak sama');
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      await authRepository.register(
        email: email,
        password: password,
      );

      if (mounted) {
        Navigator.pop(context);
      }
    } catch (error) {
      showMessage(error.toString());
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  void showMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Register'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            controller: emailController,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: passwordController,
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Password',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: confirmPasswordController,
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Konfirmasi Password',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: isLoading ? null : register,
            child: Text(isLoading ? 'Loading...' : 'Register'),
          ),
        ],
      ),
    );
  }
}
```

Catatan:

Register dengan Firebase biasanya otomatis membuat user login. Jika app memakai `AuthGate`, setelah register berhasil halaman bisa masuk ke Home.

---

## 18. Membuat HomePage

Buat file:

```text
lib/pages/home_page.dart
```

Isi:

```dart
import 'package:flutter/material.dart';

import '../repositories/auth_repository.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final authRepository = AuthRepository();
    final user = authRepository.currentUser;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            onPressed: () async {
              await authRepository.logout();
            },
            icon: const Icon(Icons.logout),
          ),
        ],
      ),
      body: Center(
        child: Text('Login sebagai: ${user?.email ?? '-'}'),
      ),
    );
  }
}
```

Setelah logout, `AuthGate` akan membaca user `null` dan menampilkan `LoginPage`.

---

## 19. Password Reset

Tambahkan di `AuthRepository` sudah ada:

```dart
Future<void> sendPasswordResetEmail(String email) async {
  await _authService.sendPasswordResetEmail(email);
}
```

Contoh pemakaian:

```dart
Future<void> forgotPassword() async {
  final email = emailController.text.trim();

  if (email.isEmpty) {
    showMessage('Isi email terlebih dahulu');
    return;
  }

  try {
    await authRepository.sendPasswordResetEmail(email);
    showMessage('Link reset password dikirim ke email');
  } catch (error) {
    showMessage(error.toString());
  }
}
```

Button:

```dart
TextButton(
  onPressed: forgotPassword,
  child: const Text('Lupa password?'),
)
```

---

## 20. Validasi Form

Validasi minimal:

```dart
bool isValidEmail(String email) {
  return email.contains('@') && email.contains('.');
}
```

Contoh:

```dart
if (!isValidEmail(email)) {
  showMessage('Format email tidak valid');
  return;
}

if (password.length < 6) {
  showMessage('Password minimal 6 karakter');
  return;
}
```

Untuk aplikasi production, validasi bisa dibuat lebih rapi memakai `Form`, `TextFormField`, dan validator.

---

## 21. Task per User

Setelah user login, kita bisa memakai `uid`.

```dart
final uid = FirebaseAuth.instance.currentUser?.uid;
```

Nanti saat memakai Firestore, struktur data bisa seperti:

```text
users/{uid}/tasks/{taskId}
```

Artinya:

- setiap user punya collection task sendiri
- user A tidak bercampur dengan user B
- security rules bisa dibuat berdasarkan `request.auth.uid`

Ini alasan kenapa Firebase Auth sebaiknya dipelajari sebelum Firestore CRUD.

---

## 22. Error Umum

### Email/Password belum diaktifkan

Solusi:

```text
Firebase Console
-> Authentication
-> Sign-in method
-> Enable Email/Password
```

### Firebase belum diinisialisasi

Pastikan:

```dart
await Firebase.initializeApp(
  options: DefaultFirebaseOptions.currentPlatform,
);
```

dipanggil sebelum `runApp`.

### firebase_options.dart tidak ditemukan

Jalankan:

```bash
flutterfire configure
```

### Password terlalu lemah

Firebase biasanya membutuhkan password minimal 6 karakter untuk email/password.

### currentUser null padahal baru buka app

Gunakan `authStateChanges()` untuk mendengarkan status auth. Jangan hanya mengandalkan `currentUser` terlalu awal saat aplikasi baru start.

---

## 23. Checklist Firebase Auth

Pastikan sudah selesai:

- [ ] Firebase project sudah dibuat.
- [ ] Flutter sudah terhubung ke Firebase.
- [ ] `firebase_options.dart` sudah ada.
- [ ] `firebase_core` sudah dipasang.
- [ ] `firebase_auth` sudah dipasang.
- [ ] Email/Password provider sudah diaktifkan.
- [ ] Firebase sudah diinisialisasi di `main.dart`.
- [ ] Bisa register user.
- [ ] Bisa login user.
- [ ] Bisa logout.
- [ ] Bisa membaca current user.
- [ ] Bisa memakai `authStateChanges`.
- [ ] Ada `AuthService`.
- [ ] Ada `AuthRepository`.
- [ ] Ada `AuthGate`.
- [ ] Login berhasil masuk Home.
- [ ] Logout kembali ke Login.

Jika checklist ini aman, kamu siap masuk **Cloud Firestore CRUD**.

---

## 24. Lanjutan Setelah Ini

Materi berikutnya:

1. Cloud Firestore Dasar.
2. Firestore CRUD.
3. Task Manager online per user.
4. Security Rules dasar.
5. Firebase Storage untuk upload file/gambar.

Urutan yang disarankan:

```text
Firebase Auth
-> Firestore CRUD
-> Task per user
-> Security Rules
```

---

## Referensi Resmi

- [Get started with Firebase Authentication on Flutter](https://firebase.google.com/docs/auth/flutter/start)
- [Authenticate with Firebase using Password-Based Accounts on Flutter](https://firebase.google.com/docs/auth/flutter/password-auth)
- [Manage Users in Firebase Authentication](https://firebase.google.com/docs/auth/flutter/manage-users)
- [FlutterFire Authentication usage](https://firebase.flutter.dev/docs/auth/usage)
