---
title: "State Management Dasar"
description: "Materi pengantar state management Flutter: local state, shared state, setState, ValueNotifier, dan kapan state perlu dipisah."
category: "Flutter"
level: "Foundation"
order: 35
tags: ["flutter", "state", "setstate", "valuenotifier"]
updated: "2026-05-20"
---

# State Management Dasar

State management adalah cara aplikasi menyimpan, mengubah, dan menampilkan data yang bisa berubah. Di Flutter, UI sangat dekat dengan state. Ketika state berubah, UI perlu diperbarui agar user melihat kondisi terbaru.

Contoh state:

- jumlah counter
- teks input
- daftar catatan
- status loading
- data user login
- filter list
- status task: todo, progress, done

Materi ini dibuat sebagai jembatan sebelum masuk project yang lebih kompleks seperti Task Manager.

---

## 1. Apa Itu State

State adalah data yang memengaruhi tampilan aplikasi.

Contoh sederhana:

```dart
int counter = 0;
```

Jika `counter` ditampilkan di UI:

```dart
Text('$counter')
```

Maka `counter` adalah state. Saat nilainya berubah dari `0` menjadi `1`, tampilan juga harus berubah.

Contoh lain:

```dart
bool isLoading = false;
String selectedCategory = 'Semua';
List<String> notes = [];
```

Ketiganya termasuk state karena bisa memengaruhi apa yang tampil di layar.

---

## 2. Local State

Local state adalah state yang hanya dipakai di satu widget atau satu halaman.

Contoh:

- counter di satu halaman
- password visibility di form login
- selected tab di halaman tertentu
- text input di form tambah catatan

Contoh local state dengan `setState`:

```dart
class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int counter = 0;

  void increment() {
    setState(() {
      counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('$counter'),
        ElevatedButton(
          onPressed: increment,
          child: const Text('Tambah'),
        ),
      ],
    );
  }
}
```

Penjelasan:

- `counter` adalah state.
- `increment()` mengubah state.
- `setState()` memberi tahu Flutter bahwa UI perlu digambar ulang.

Kapan `setState` cukup?

- State hanya dipakai di satu halaman.
- Logika masih sederhana.
- Tidak banyak widget yang butuh data yang sama.
- Project masih kecil atau sedang belajar.

---

## 3. Shared State

Shared state adalah state yang dibutuhkan oleh lebih dari satu widget atau halaman.

Contoh:

- data user login dipakai di banyak halaman
- keranjang belanja dipakai di halaman produk dan halaman checkout
- theme mode dipakai seluruh aplikasi
- daftar task dipakai di halaman list, detail, dan statistik

Jika state mulai dipakai banyak tempat, `setState` di satu halaman sering terasa kurang nyaman.

Contoh tanda state mulai perlu dipisah:

- function tambah/edit/hapus makin banyak di satu halaman
- data perlu dikirim terlalu jauh lewat constructor
- satu file menjadi terlalu panjang
- banyak widget butuh data yang sama
- sulit mencari sumber perubahan data

Pada tahap ini, kamu bisa mulai belajar pola state management seperti `ValueNotifier`, Provider, Riverpod, Bloc, atau Cubit. Untuk pemula, pahami konsepnya dulu sebelum memilih library.

---

## 4. Pola setState yang Rapi

`setState` tidak salah. Yang penting adalah memakainya dengan rapi.

Contoh kurang rapi:

```dart
onPressed: () {
  setState(() {
    tasks.add('Belajar Flutter');
    tasks.sort();
    selectedFilter = 'Semua';
    isLoading = false;
  });
}
```

Lebih rapi jika logika dipisah ke function:

```dart
void addTask(String title) {
  setState(() {
    tasks.add(title);
  });
}
```

Lalu tombol cukup memanggil function:

```dart
ElevatedButton(
  onPressed: () => addTask('Belajar Flutter'),
  child: const Text('Tambah'),
)
```

Keuntungannya:

- `build()` lebih bersih.
- Logika mudah dicari.
- Kode lebih mudah dipindahkan ke controller nanti.

---

## 5. State Loading, Empty, Error, Success

Dalam aplikasi nyata, state bukan hanya data. Ada juga state kondisi.

Contoh saat mengambil data:

```dart
bool isLoading = false;
String? errorMessage;
List<String> items = [];
```

Tampilan bisa dibagi menjadi beberapa kondisi:

```dart
if (isLoading) {
  return const Center(
    child: CircularProgressIndicator(),
  );
}

if (errorMessage != null) {
  return Center(
    child: Text(errorMessage!),
  );
}

if (items.isEmpty) {
  return const Center(
    child: Text('Data masih kosong'),
  );
}

return ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return Text(items[index]);
  },
);
```

Pola ini penting karena user perlu tahu apa yang sedang terjadi:

- aplikasi sedang loading
- data kosong
- terjadi error
- data berhasil tampil

---

## 6. Mengenal ValueNotifier

`ValueNotifier` adalah cara sederhana untuk menyimpan state yang bisa didengarkan oleh UI. Ini bisa menjadi langkah awal sebelum belajar Provider atau Riverpod.

Contoh:

```dart
final counterNotifier = ValueNotifier<int>(0);
```

Mengubah nilainya:

```dart
counterNotifier.value++;
```

Menampilkan di UI:

```dart
ValueListenableBuilder<int>(
  valueListenable: counterNotifier,
  builder: (context, counter, child) {
    return Text('$counter');
  },
)
```

Contoh lengkap:

```dart
class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  final counterNotifier = ValueNotifier<int>(0);

  @override
  void dispose() {
    counterNotifier.dispose();
    super.dispose();
  }

  void increment() {
    counterNotifier.value++;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ValueListenableBuilder<int>(
          valueListenable: counterNotifier,
          builder: (context, counter, child) {
            return Text('$counter');
          },
        ),
        ElevatedButton(
          onPressed: increment,
          child: const Text('Tambah'),
        ),
      ],
    );
  }
}
```

Kapan `ValueNotifier` cocok?

- State masih sederhana.
- Hanya perlu mendengarkan satu nilai atau satu object.
- Ingin memisahkan perubahan state dari `setState`.
- Belum perlu library state management.

---

## 7. Kapan Belajar Provider atau Riverpod

Jangan terburu-buru memakai library state management. Library membantu, tetapi jika konsep state belum paham, library justru terasa membingungkan.

Belajar Provider atau Riverpod ketika:

- data dipakai banyak halaman
- banyak logic tidak cocok lagi disimpan di widget
- butuh dependency injection sederhana
- butuh testing state yang lebih rapi
- project mulai punya banyak fitur

Urutan belajar yang disarankan:

```text
setState
-> pisahkan function state
-> ValueNotifier
-> Provider atau Riverpod
```

Untuk project berikutnya, kita masih bisa memakai `setState` dengan pola yang lebih rapi. Setelah itu baru masuk local storage dan state management yang lebih serius.

---

## 8. Checklist State Management Dasar

Pastikan kamu sudah paham:

- [ ] State adalah data yang memengaruhi UI.
- [ ] Local state cukup dikelola dengan `setState`.
- [ ] Shared state dipakai banyak widget atau halaman.
- [ ] `setState` sebaiknya dipanggil dari function yang jelas.
- [ ] UI perlu menangani loading, empty, error, dan success.
- [ ] `ValueNotifier` bisa dipakai untuk state sederhana.
- [ ] Provider atau Riverpod dipelajari saat project mulai membesar.

Jika checklist ini sudah aman, lanjut ke materi CRUD lokal, filter, dan search.
