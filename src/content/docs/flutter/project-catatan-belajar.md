---
title: "Project 1: Aplikasi Catatan Belajar"
description: "Project Flutter step-by-step untuk membuat aplikasi catatan belajar sederhana dari nol."
category: "Flutter"
level: "Project"
order: 40
tags: ["flutter", "project", "notes", "state", "form"]
updated: "2026-05-20"
---

# Project 1: Aplikasi Catatan Belajar

Project ini adalah latihan pertama setelah memahami Flutter dasar. Tujuannya bukan membuat aplikasi yang rumit, tetapi membiasakan alur kerja Flutter: membuat model, menampilkan list, membaca input, mengubah state, dan memisahkan file.

Fitur yang akan dibuat:

- Menampilkan daftar catatan.
- Menambah catatan baru.
- Menghapus catatan.
- Menampilkan empty state saat catatan kosong.
- Memisahkan kode ke beberapa file.

---

## 1. Target Project

Di akhir project ini, aplikasi punya alur seperti ini:

```text
Home Page
-> melihat daftar catatan
-> tekan tombol tambah
-> isi judul dan isi catatan
-> simpan
-> catatan muncul di daftar
-> bisa hapus catatan
```

Skill yang dilatih:

- `StatefulWidget`
- `TextEditingController`
- `ListView.builder`
- `Navigator`
- `setState`
- model class
- struktur folder sederhana

---

## 2. Struktur Folder

Buat struktur folder seperti ini di dalam `lib/`:

```text
lib/
  main.dart
  models/
    note.dart
  pages/
    note_list_page.dart
    note_form_page.dart
  widgets/
    note_card.dart
```

Penjelasan:

- `models/`: tempat bentuk data aplikasi.
- `pages/`: tempat halaman utama.
- `widgets/`: tempat komponen UI kecil yang bisa dipakai ulang.

---

## 3. Membuat Model Note

Buat file `lib/models/note.dart`.

```dart
class Note {
  final String title;
  final String content;
  final DateTime createdAt;

  const Note({
    required this.title,
    required this.content,
    required this.createdAt,
  });
}
```

Penjelasan:

- `title`: judul catatan.
- `content`: isi catatan.
- `createdAt`: tanggal catatan dibuat.
- Semua property dibuat `final` agar data note tidak berubah sembarangan.

Kenapa memakai class?

Karena data catatan punya bentuk yang jelas. Dibanding memakai Map seperti `{'title': '...'}`, class membuat kode lebih mudah dibaca dan lebih aman.

---

## 4. Setup main.dart

Isi `lib/main.dart`:

```dart
import 'package:flutter/material.dart';

import 'pages/note_list_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Catatan Belajar',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
        ),
        useMaterial3: true,
      ),
      home: const NoteListPage(),
    );
  }
}
```

Penjelasan:

- `MaterialApp` adalah root aplikasi.
- `debugShowCheckedModeBanner: false` menghilangkan label debug.
- `ThemeData` mengatur tema aplikasi.
- `home` diarahkan ke `NoteListPage`.

---

## 5. Membuat Komponen NoteCard

Buat file `lib/widgets/note_card.dart`.

```dart
import 'package:flutter/material.dart';

import '../models/note.dart';

class NoteCard extends StatelessWidget {
  final Note note;
  final VoidCallback onDelete;

  const NoteCard({
    super.key,
    required this.note,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(note.title),
        subtitle: Text(note.content),
        trailing: IconButton(
          icon: const Icon(Icons.delete_outline),
          onPressed: onDelete,
        ),
      ),
    );
  }
}
```

Penjelasan:

- `NoteCard` menerima data `note`.
- `onDelete` adalah callback yang dijalankan saat tombol hapus ditekan.
- `ListTile` cocok untuk item list sederhana.

Kenapa dipisah?

Supaya halaman utama tidak terlalu penuh. Jika nanti desain card berubah, cukup ubah file `note_card.dart`.

---

## 6. Membuat Halaman List Catatan

Buat file `lib/pages/note_list_page.dart`.

```dart
import 'package:flutter/material.dart';

import '../models/note.dart';
import '../widgets/note_card.dart';
import 'note_form_page.dart';

class NoteListPage extends StatefulWidget {
  const NoteListPage({super.key});

  @override
  State<NoteListPage> createState() => _NoteListPageState();
}

class _NoteListPageState extends State<NoteListPage> {
  final List<Note> notes = [];

  Future<void> _openFormPage() async {
    final result = await Navigator.push<Note>(
      context,
      MaterialPageRoute(
        builder: (context) => const NoteFormPage(),
      ),
    );

    if (result == null) return;

    setState(() {
      notes.add(result);
    });
  }

  void _deleteNote(int index) {
    setState(() {
      notes.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Catatan Belajar'),
      ),
      body: notes.isEmpty
          ? const Center(
              child: Text('Belum ada catatan'),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: notes.length,
              itemBuilder: (context, index) {
                final note = notes[index];

                return NoteCard(
                  note: note,
                  onDelete: () => _deleteNote(index),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _openFormPage,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Penjelasan penting:

- `notes` menyimpan daftar catatan di memory.
- `_openFormPage()` membuka halaman form.
- `Navigator.push<Note>` menunggu hasil berupa object `Note`.
- Jika user menyimpan catatan, hasilnya ditambahkan ke `notes`.
- `setState()` membuat UI diperbarui.

---

## 7. Membuat Halaman Form Catatan

Buat file `lib/pages/note_form_page.dart`.

```dart
import 'package:flutter/material.dart';

import '../models/note.dart';

class NoteFormPage extends StatefulWidget {
  const NoteFormPage({super.key});

  @override
  State<NoteFormPage> createState() => _NoteFormPageState();
}

class _NoteFormPageState extends State<NoteFormPage> {
  final titleController = TextEditingController();
  final contentController = TextEditingController();

  @override
  void dispose() {
    titleController.dispose();
    contentController.dispose();
    super.dispose();
  }

  void _saveNote() {
    final title = titleController.text.trim();
    final content = contentController.text.trim();

    if (title.isEmpty || content.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Judul dan isi catatan wajib diisi'),
        ),
      );
      return;
    }

    final note = Note(
      title: title,
      content: content,
      createdAt: DateTime.now(),
    );

    Navigator.pop(context, note);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tambah Catatan'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: titleController,
              decoration: const InputDecoration(
                labelText: 'Judul',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: contentController,
              maxLines: 5,
              decoration: const InputDecoration(
                labelText: 'Isi catatan',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: _saveNote,
                child: const Text('Simpan'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

Penjelasan penting:

- `TextEditingController` digunakan untuk membaca input.
- `dispose()` wajib dipakai untuk membersihkan controller.
- `trim()` menghapus spasi kosong di awal dan akhir teks.
- Jika input kosong, aplikasi menampilkan `SnackBar`.
- `Navigator.pop(context, note)` mengembalikan data ke halaman sebelumnya.

---

## 8. Alur Data Project

Alur ketika user menambah catatan:

```text
User tekan tombol +
-> NoteFormPage dibuka
-> user isi judul dan catatan
-> user tekan Simpan
-> form membuat object Note
-> Navigator.pop mengirim Note ke NoteListPage
-> NoteListPage menerima result
-> result masuk ke List notes
-> setState membuat UI update
```

Ini adalah pola yang sangat sering dipakai di Flutter: halaman A membuka halaman B, halaman B mengembalikan data, lalu halaman A memperbarui state.

---

## 9. Challenge Pengembangan

Setelah versi dasar selesai, lanjutkan dengan challenge berikut:

1. Tampilkan tanggal dibuat di setiap catatan.
2. Tambahkan halaman detail catatan.
3. Tambahkan fitur edit catatan.
4. Tambahkan konfirmasi sebelum hapus.
5. Tambahkan kategori catatan.
6. Tambahkan search catatan.
7. Simpan catatan ke local storage.

Urutan yang disarankan:

```text
delete confirmation
-> detail page
-> edit note
-> search
-> local storage
```

---

## 10. Checklist Selesai Project

Project ini dianggap selesai jika kamu sudah bisa:

- [ ] Membuat model `Note`.
- [ ] Membuat halaman list.
- [ ] Membuat halaman form.
- [ ] Mengirim data antar halaman.
- [ ] Menambahkan data ke `List`.
- [ ] Menghapus data dari `List`.
- [ ] Menampilkan empty state.
- [ ] Memisahkan file berdasarkan tanggung jawab.

Jika checklist ini sudah aman, lanjut ke Project 2: **Task Manager** dengan struktur folder yang lebih rapi, validasi lebih serius, dan local storage.
