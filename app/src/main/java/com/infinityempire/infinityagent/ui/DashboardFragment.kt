package com.infinityempire.infinityagent.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.infinityempire.infinityagent.R
import com.infinityempire.infinityagent.databinding.FragmentDashboardBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.IOException

class DashboardFragment : Fragment(R.layout.fragment_dashboard) {
    private var _binding: FragmentDashboardBinding? = null
    private val binding get() = _binding!!

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentDashboardBinding.bind(view)
        binding.btnTestNetwork.setOnClickListener {
            binding.tvNetworkStatus.text = getString(R.string.network_status_idle)
            viewLifecycleOwner.lifecycleScope.launch {
                val ok = withContext(Dispatchers.IO) { testNetwork() }
                binding.tvNetworkStatus.text = if (ok) {
                    getString(R.string.network_status_ok)
                } else {
                    getString(R.string.network_status_fail)
                }
            }
        }
    }

    private fun testNetwork(): Boolean {
        return try {
            val client = OkHttpClient()
            val request = Request.Builder().url("https://www.google.com/generate_204").build()
            client.newCall(request).execute().use { it.isSuccessful }
        } catch (e: IOException) {
            false
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
