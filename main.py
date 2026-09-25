import flet as ft
import csv

def main(page: ft.Page):
    page.title = "دليل الأدوية وجرعات الأطفال"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    medicines = []
    favorites = set()

    # 1. قراءة بيانات الأدوية من CSV
    try:
        with open("app/src/main/assets/eg_drugs.csv", mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # تخطي السطر الأول
            for row in reader:
                if len(row) >= 3:
                    medicines.append({
                        "name": row[0].strip(),
                        "active": row[1].strip(),
                        "price": row[2].strip()
                    })
    except Exception as e:
        print(f"Error loading CSV: {e}")

    # عناصر واجهة البحث
    search_input = ft.TextField(
        label="ابحث باسم الدواء أو المادة الفعالة...",
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: filter_medicines(e.control.value)
    )
    
    results_list = ft.ListView(expand=True, spacing=10)

    def display_list(items):
        results_list.controls.clear()
        for item in items[:40]:  # عرض أول 40 نتيجة لسرعة الأداء
            is_fav = item["name"] in favorites
            results_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(item["name"], size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                                ft.IconButton(
                                    icon=ft.icons.FAVORITE if is_fav else ft.icons.FAVORITE_BORDER,
                                    icon_color=ft.colors.RED if is_fav else ft.colors.GREY,
                                    on_click=lambda e, m=item["name"]: toggle_favorite(m)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"المادة الفعالة: {item['active']}", size=14, color=ft.colors.GREY_800),
                            ft.Text(f"السعر: {item['price']} ج.م", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),
                        ])
                    )
                )
            )
        page.update()

    def filter_medicines(query):
        if not query.strip():
            display_list(medicines)
            return
        q = query.lower()
        filtered = [m for m in medicines if q in m["name"].lower() or q in m["active"].lower()]
        display_list(filtered)

    def toggle_favorite(med_name):
        if med_name in favorites:
            favorites.remove(med_name)
        else:
            favorites.add(med_name)
        filter_medicines(search_input.value or "")

    # 2. حاسبة جرعات الأطفال
    weight_input = ft.TextField(label="وزن الطفل (كجم)", keyboard_type=ft.KeyboardType.NUMBER)
    dose_mg_input = ft.TextField(label="الجرعة المطلوبة (ملجم / كجم / يوم)", keyboard_type=ft.KeyboardType.NUMBER)
    conc_input = ft.TextField(label="تركيز الدواء (ملجم في كل 5 مل)", keyboard_type=ft.KeyboardType.NUMBER)
    calc_result = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800)

    def calculate_dosage(e):
        try:
            w = float(weight_input.value)
            d = float(dose_mg_input.value)
            c = float(conc_input.value)
            
            total_mg_per_day = w * d
            total_ml_per_day = (total_mg_per_day * 5) / c
            dose_per_8h = total_ml_per_day / 3

            calc_result.value = f"الجرعة اليومية الكلية: {total_ml_per_day:.1f} مل/يوم\n(حوالي {dose_per_8h:.1f} مل كل 8 ساعات)"
        except Exception:
            calc_result.value = "يرجى إدخال أرقام صحيحة في جميع الخانات!"
        page.update()

    calc_tab = ft.Column([
        ft.Text("👶 حاسبة جرعات الأطفال الطبية", size=18, weight=ft.FontWeight.BOLD),
        weight_input,
        dose_mg_input,
        conc_input,
        ft.ElevatedButton("حساب الجرعة الدقيقة", icon=ft.icons.CALCULATE, on_click=calculate_dosage),
        ft.Divider(),
        calc_result
    ], spacing=15, padding=10)

    search_tab = ft.Column([search_input, results_list], expand=True)

    # التبويبات الرئيسية
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="البحث عن دواء", icon=ft.icons.MEDICATION, content=search_tab),
            ft.Tab(text="حاسبة الجرعات", icon=ft.icons.CALCULATOR, content=calc_tab),
        ],
        expand=True
    )

    page.add(tabs)
    display_list(medicines)

ft.app(target=main)
