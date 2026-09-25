package com.example.medicines

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import java.io.BufferedReader
import java.io.InputStreamReader

data class Medicine(val name: String, val activeIngredient: String, val price: String)

class MainActivity : AppCompatActivity() {

    private val medicineList = mutableListOf<Medicine>()
    private val filteredList = mutableListOf<Medicine>()
    private lateinit var adapter: MedicineAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val etSearch = findViewById<EditText>(R.id.etSearch)
        val rvMedicines = findViewById<RecyclerView>(R.id.rvMedicines)

        // تحميل البيانات من ملف الـ CSV
        loadCSVData()

        adapter = MedicineAdapter(filteredList)
        rvMedicines.layoutManager = LinearLayoutManager(this)
        rvMedicines.adapter = adapter

        // البحث عند الكتابة
        etSearch.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                filter(s.toString())
            }
            override fun afterTextChanged(s: Editable?) {}
        })
    }

    private fun loadCSVData() {
        try {
            // فتح ملف الـ CSV المرفوع
            val inputStream = assets.open("medicines.csv")
            val reader = BufferedReader(InputStreamReader(inputStream))
            var line: String? = reader.readLine() // تخطي السطر الأول (العناوين)

            while (reader.readLine().also { line = it } != null) {
                val tokens = line!!.split(",")
                if (tokens.size >= 3) {
                    val medicine = Medicine(
                        name = tokens[0].trim(),
                        activeIngredient = tokens[1].trim(),
                        price = tokens[2].trim()
                    )
                    medicineList.add(medicine)
                }
            }
            reader.close()
            filteredList.addAll(medicineList.take(50)) // عرض أول 50 عنصر لتسريع الواجهة
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun filter(text: String) {
        filteredList.clear()
        if (text.isEmpty()) {
            filteredList.addAll(medicineList.take(50))
        } else {
            val query = text.lowercase()
            for (item in medicineList) {
                if (item.name.lowercase().contains(query) || item.activeIngredient.lowercase().contains(query)) {
                    filteredList.add(item)
                }
            }
        }
        adapter.notifyDataSetChanged()
    }
}
