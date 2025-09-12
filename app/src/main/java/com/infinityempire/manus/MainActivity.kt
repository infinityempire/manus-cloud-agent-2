package com.infinityempire.manus

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.infinityempire.manus.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.title.text = "Manus Agent — Debug"
    }
}
