from datetime import datetime

# === Kelas Produk ===
class Produk:
    def __init__(self, id_produk, nama, harga, stok):
        self.id_produk = id_produk
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def get_info(self):
        return f"[{self.id_produk}] {self.nama} - Harga: Rp {self.harga:,}, Stok: {self.stok}"

# === Kelas Gudang ===
class Gudang:
    def __init__(self):
        self.produk_list = []

    def tambah_produk(self, produk):
        self.produk_list.append(produk)

    def tampilkan_produk(self):
        if not self.produk_list:
            print("Tidak ada produk di gudang.")
            return

        print("\nDaftar Produk di Gudang:")
        for produk in self.produk_list:
            print(produk.get_info())

    def cari_produk(self, id_produk):
        return next((p for p in self.produk_list if p.id_produk == id_produk), None)

    def edit_produk(self, id_produk, nama=None, harga=None, stok=None):
        produk = self.cari_produk(id_produk)
        if not produk:
            print("Produk tidak ditemukan!")
            return False
        
        if nama is not None:
            produk.nama = nama
        if harga is not None:
            produk.harga = harga
        if stok is not None:
            produk.stok = stok
        
        print("Produk berhasil diperbarui!")
        return True

# === Kelas Transaksi ===
class Transaksi:
    def __init__(self):
        self.transaksi_list = []

    def buat_transaksi_multiple(self, gudang):
        """Mencatat beberapa transaksi sekaligus"""
        print("\nInput transaksi multiple (ketik 'selesai' pada ID Produk untuk mengakhiri)")
        
        transaksi_batch = []
        total_nilai = 0
        waktu_transaksi = datetime.now()
        
        while True:
            try:
                print("\nTransaksi baru:")
                id_produk = input("ID Produk: ").strip().upper()
                if id_produk.lower() == 'selesai':
                    break
                
                jumlah = int(input("Jumlah: "))
                if jumlah <= 0:
                    print("Jumlah harus lebih dari 0!")
                    continue
                
                produk = gudang.cari_produk(id_produk)
                if not produk:
                    print("Produk tidak ditemukan!")
                    continue
                
                if produk.stok < jumlah:
                    print(f"Stok tidak cukup! Tersedia: {produk.stok}")
                    continue
                
                total_harga = produk.harga * jumlah
                transaksi_batch.append({
                    "produk": produk,
                    "jumlah": jumlah,
                    "total_harga": total_harga
                })
                total_nilai += total_harga
                
                print(f"Ditambahkan: {jumlah} {produk.nama} = Rp {total_harga:,}")
                
            except ValueError:
                print("Input tidak valid. Masukkan angka untuk jumlah.")
        
        if not transaksi_batch:
            print("Tidak ada transaksi yang diinput.")
            return
        
        # Tampilkan ringkasan transaksi
        print("\nRingkasan Transaksi:")
        for t in transaksi_batch:
            print(f"- {t['jumlah']} {t['produk'].nama} @ Rp {t['produk'].harga:,} = Rp {t['total_harga']:,}")
        print(f"Total Nilai Transaksi: Rp {total_nilai:,}")
        
        # Konfirmasi dan proses transaksi
        konfirmasi = input("\nProses transaksi? (y/n): ").lower()
        if konfirmasi == 'y':
            # Proses semua transaksi
            for t in transaksi_batch:
                produk = t['produk']
                jumlah = t['jumlah']
                
                # Kurangi stok
                produk.stok -= jumlah
                
                # Catat transaksi
                self.transaksi_list.append({
                    "id_produk": produk.id_produk,
                    "nama_produk": produk.nama,
                    "jumlah": jumlah,
                    "total_harga": t['total_harga'],
                    "tanggal": waktu_transaksi
                })
            
            print("Semua transaksi berhasil diproses!")
        else:
            print("Transaksi dibatalkan.")

    def buat_transaksi(self, gudang, id_produk, jumlah):
        """Mencatat single transaksi"""
        produk = gudang.cari_produk(id_produk)
        if not produk:
            print("Produk tidak ditemukan!")
            return

        if produk.stok < jumlah:
            print(f"Stok {produk.nama} tidak mencukupi! Tersedia: {produk.stok}")
            return

        total_harga = produk.harga * jumlah
        produk.stok -= jumlah
        transaksi_detail = {
            "id_produk": produk.id_produk,
            "nama_produk": produk.nama,
            "jumlah": jumlah,
            "total_harga": total_harga,
            "tanggal": datetime.now()
        }
        self.transaksi_list.append(transaksi_detail)
        print(f"Transaksi berhasil! {jumlah} {produk.nama} terjual seharga Rp {total_harga:,}.")

    def tampilkan_transaksi(self):
        if not self.transaksi_list:
            print("Belum ada transaksi.")
            return

        print("\nRiwayat Transaksi:")
        for idx, transaksi in enumerate(self.transaksi_list, start=1):
            print(f"{idx}. {transaksi['tanggal']:%Y-%m-%d %H:%M:%S} - {transaksi['nama_produk']} - Jumlah: {transaksi['jumlah']} - Total: Rp {transaksi['total_harga']:,}")

# === Program Utama ===
def main():
    gudang = Gudang()
    transaksi = Transaksi()

    # Menambahkan beberapa produk ke gudang
    gudang.tambah_produk(Produk("P001", "Palu", 50000, 10))
    gudang.tambah_produk(Produk("S001", "Beras", 12000, 100))
    gudang.tambah_produk(Produk("R001", "Meja", 500000, 5))
    gudang.tambah_produk(Produk("M001", "Air Mineral", 3000, 200))

    while True:
        print("\n==== Sistem Pergudangan ====")
        print("1. Tampilkan Produk di Gudang")
        print("2. Tambah Produk ke Gudang")
        print("3. Edit Produk di Gudang")
        print("4. Catat Transaksi Tunggal")
        print("5. Catat Multiple Transaksi")
        print("6. Tampilkan Riwayat Transaksi")
        print("7. Keluar")

        pilihan = input("Pilih opsi (1-7): ")

        if pilihan == "1":
            gudang.tampilkan_produk()

        elif pilihan == "2":
            try:
                id_produk = input("Masukkan ID Produk: ")
                nama = input("Masukkan Nama Produk: ")
                harga = int(input("Masukkan Harga Produk: "))
                stok = int(input("Masukkan Stok Produk: "))
                gudang.tambah_produk(Produk(id_produk, nama, harga, stok))
                print("Produk berhasil ditambahkan ke gudang.")
            except ValueError:
                print("Input tidak valid. Pastikan harga dan stok berupa angka.")

        elif pilihan == "3":
            gudang.tampilkan_produk()
            try:
                id_produk = input("Masukkan ID Produk yang akan diedit: ")
                print("\nKosongkan input jika tidak ingin mengubah nilai")
                nama_baru = input("Masukkan Nama Produk Baru: ").strip()
                harga_input = input("Masukkan Harga Produk Baru: ").strip()
                stok_input = input("Masukkan Stok Produk Baru: ").strip()

                harga_baru = int(harga_input) if harga_input else None
                stok_baru = int(stok_input) if stok_input else None
                nama_baru = nama_baru if nama_baru else None

                gudang.edit_produk(id_produk, nama_baru, harga_baru, stok_baru)
            except ValueError:
                print("Input tidak valid. Pastikan harga dan stok berupa angka.")

        elif pilihan == "4":
            gudang.tampilkan_produk()
            try:
                id_produk = input("\nMasukkan ID Produk: ")
                jumlah = int(input("Masukkan Jumlah: "))
                transaksi.buat_transaksi(gudang, id_produk, jumlah)
            except ValueError:
                print("Input tidak valid. Pastikan jumlah berupa angka.")

        elif pilihan == "5":
            gudang.tampilkan_produk()
            transaksi.buat_transaksi_multiple(gudang)

        elif pilihan == "6":
            transaksi.tampilkan_transaksi()

        elif pilihan == "7":
            print("Terima kasih telah menggunakan sistem pergudangan.")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih opsi yang tersedia.")

if __name__ == "__main__":
    main()
