class Symbol:
    def __init__(self, name: str, type_: str, scope: str = "global", memory_location: int = None):
        self.name = name  # Değişken adı
        self.type = type_  # 'int' veya 'float'
        self.scope = scope  # Kapsam
        self.memory_location = memory_location  # Simüle edilmiş bellek adresi

    def __repr__(self):
        return f"Symbol(Name: {self.name}, Type: {self.type}, Scope: {self.scope}, Address: {self.memory_location})"


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        # Bellek adreslerini jüriye daha gerçekçi göstermek için 1000'den başlatıyoruz
        self.current_address = 1000

    def insert(self, name: str, type_: str, scope: str = "global") -> bool:
        """
        Sembol tablosuna yeni bir değişken ekler.
        Değişken zaten varsa False döner (İleride duplicate declaration hatası yakalamak için).
        """
        if name in self.symbols:
            return False

        # Yeni sembol nesnesini oluşturup adresi bağlıyoruz
        new_symbol = Symbol(name, type_, scope, self.current_address)
        self.symbols[name] = new_symbol

        # Her değişken için adresi 4 byte ilerletelim (32-bit mimari simülasyonu)
        self.current_address += 4
        return True

    def lookup(self, name: str) -> Symbol:
        """
        Verilen isimde bir değişken tabloda var mı diye bakar.
        Bulursa Symbol nesnesini, bulamazsa None döner (Tanımlanmamış değişken kontrolü için).
        """
        return self.symbols.get(name, None)

    def get_all_symbols(self):
        """
        İleride Tkinter arayüzünde (GUI) tablo olarak gösterebilmek için
        tüm sembolleri bir liste olarak döner.
        """
        return list(self.symbols.values())

    def clear(self):
        """Her yeni derleme simülasyonunda tabloyu sıfırlamak için."""
        self.symbols.clear()
        self.current_address = 1000